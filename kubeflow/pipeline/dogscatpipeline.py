import kfp
import kfp.components as comp
from kfp import dsl
from kfp.v2.components.experimental.base_component import BaseComponent
from kfp.v2.components.experimental.pipeline_task import PipelineTask

from kfserving.models. import component import serving_op