import kfp
import kfp.components as comp
from typing import NamedTuple
from kfp.components import func_to_container_op, InputPath, OutputPath

dogscats_train_op = comp.load_component_from_file('component.yaml')


def dogscats_train_pipeline(MAPPED_PATH: str):
    _ = dogscats_train_op()
    return f"/{MAPPED_PATH}/models/MobileNetVDogsCats.h5"

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(dogscats_train_pipeline, 'dogscats-pipeline.yaml')
