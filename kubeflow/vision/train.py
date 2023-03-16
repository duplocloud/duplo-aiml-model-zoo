import pathlib
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import os

# map to external drive
MAPPED_PATH = os.getenv("MAPPED_PATH", default = "../data")

# all data is within this folder ../data
data_root_path = pathlib.Path(MAPPED_PATH)
data_dir = f"{data_root_path}/images"
models_dir = f"{data_root_path}/models"
training_information_dir = f"{data_root_path}/training_information"

model_name="MobileNetV3(small)"
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
seed = 123
EPOCHS = 50  # 1000

def train_model(preprocess_input, base_model, model_name, train_dataset, validation_dataset, num_classes, img_shape,
                data_augmentation, class_names, epochs):

    model_original_path = f"{models_dir}/{model_name}_original.h5" # do not overwrite for now
    model_path = f"{models_dir}/{model_name}.h5"

    try:
        model = tf.keras.models.load_model(model_original_path)
        model.summary()
    except Exception as e:
        print(e)

        image_batch, label_batch = next(iter(train_dataset))
        feature_batch = base_model(image_batch)
        print(f"Feature batch shape: {feature_batch.shape}")

        base_model.trainable = False
        base_model.summary()

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        feature_batch_average = global_average_layer(feature_batch)
        print(f"Feature batch average shape: {feature_batch_average.shape}")

        prediction_layer = tf.keras.layers.Dense(num_classes)
        prediction_batch = prediction_layer(feature_batch_average)
        print(f"Prediction batch shape: {prediction_batch.shape}")

        inputs = tf.keras.Input(shape=img_shape)
        x = data_augmentation(inputs)
        x = preprocess_input(x)
        x = base_model(x, training=False)
        x = global_average_layer(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        outputs = prediction_layer(x)
        model = tf.keras.Model(inputs, outputs)

        base_learning_rate = 0.0001
        model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=base_learning_rate),
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
        model.summary()
        print(f"Length of trainable variables in the model: {len(model.trainable_variables)}")  # 훈련 가능한 객체 수를 확인한다.

        loss0, accuracy0 = model.evaluate(validation_dataset)
        print(f"initial loss: {loss0}")
        print(f"initial accuracy: {accuracy0}")

        early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                      patience=10)
        history = model.fit(train_dataset, epochs=epochs, validation_data=validation_dataset,
                            callbacks=[early_stop])

        base_model.trainable = True
        print(f"Number of layers in the base model: {len(base_model.layers)}")

        fine_tune_at = 100
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

        model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      optimizer=tf.keras.optimizers.RMSprop(learning_rate=base_learning_rate / 10),
                      metrics=["accuracy"])
        model.summary()
        print(f"Length of trainable variables in the model: {len(model.trainable_variables)}")  # 훈련 가능한 객체 수를 확인한다.

        history_fine = model.fit(train_dataset, epochs=epochs, initial_epoch=history.epoch[-1],
                                 validation_data=validation_dataset, callbacks=[early_stop])  # 미세 조정된 모델로 훈련을 계속한다.
        initial_epochs = history.epoch[-1]
        # overwrite
        model.save(model_path)
        acc = history.history["accuracy"] + history_fine.history["accuracy"]
        val_acc = history.history["val_accuracy"] + history_fine.history["val_accuracy"]
        loss = history.history["loss"] + history_fine.history["loss"]
        val_loss = history.history["val_loss"] + history_fine.history["val_loss"]

        plt.figure(figsize=(9, 9))
        plt.subplot(2, 1, 1)
        plt.plot(acc, label="Training Accuracy")
        plt.plot(val_acc, label="Validation Accuracy")
        plt.plot([initial_epochs - 1, initial_epochs - 1], plt.ylim(), label="Start Fine Tuning")
        plt.legend(loc="lower right")
        plt.ylabel("Accuracy")
        plt.xlabel("epoch")
        plt.title(f"{model_name} Training and Validation Accuracy")
        plt.subplot(2, 1, 2)
        plt.plot(loss, label="Training Loss")
        plt.plot(val_loss, label="Validation Loss")
        plt.plot([initial_epochs - 1, initial_epochs - 1], plt.ylim(), label="Start Fine Tuning")
        plt.legend(loc="upper right")
        plt.ylabel("Cross Entropy")
        plt.title(f"{model_name} Training and Validation Loss")
        plt.xlabel("epoch")
        plt.tight_layout()
        plt.savefig(f"{training_information_dir}/3_{model_name}_history.png")
        plt.close()

    loss, accuracy = model.evaluate(validation_dataset)
    print(f"Validation loss: {loss}")
    print(f"Validation accuracy: {accuracy}")

    image_batch, label_batch = validation_dataset.as_numpy_iterator().next()
    predictions = model.predict_on_batch(image_batch)
    predictions = tf.nn.softmax(predictions)
    print(f"Predictions:\n{predictions.numpy()}")
    print(f"Labels:\n{label_batch}")

    plt.figure(figsize=(9, 9))
    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.imshow(image_batch[i].astype("uint8"))
        plt.title(
            f"{class_names[np.argmax(predictions[i])]} {100 * np.max(predictions[i]):.2f}% ({class_names[label_batch[i]]})")
        plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{training_information_dir}/4_{model_name}_predictions.png")
    plt.close()

    return model

train_dataset = image_dataset_from_directory(data_dir, validation_split=0.2, subset="training", seed=seed,
                                             image_size=IMG_SIZE, batch_size=BATCH_SIZE)

validation_dataset = image_dataset_from_directory(data_dir, validation_split=0.2, subset="validation", seed=seed,
                                                  image_size=IMG_SIZE, batch_size=BATCH_SIZE)

class_names = train_dataset.class_names
print(f"Class names: {class_names}")

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])

IMG_SHAPE = IMG_SIZE + (3,)
num_classes = len(class_names)

train_model(
    tf.keras.applications.mobilenet.preprocess_input,
    tf.keras.applications.MobileNet(alpha=0.25, input_shape=IMG_SHAPE, include_top=False, weights='imagenet'),
    model_name,
    train_dataset,
    validation_dataset,
    num_classes,
    IMG_SHAPE,
    data_augmentation,
    class_names,
    EPOCHS
)