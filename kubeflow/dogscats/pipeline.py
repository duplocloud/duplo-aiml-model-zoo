import kfp
import kfp.components as comp


dogscats_train_op = comp.load_component_from_file('component.yaml')


def dogscats_train_pipeline():
    _ = dogscats_train_op()


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(dogscats_train_pipeline, 'dogscats-pipeline.yaml')
