import enum

from oak_cli.evaluation.addons.flops.main import (
    EvaluationRunFLOpsProjectStage,
    FLOpsExclusiveCSVKeys,
    FLOpsTrainedModelCSVKeys,
)
from oak_cli.evaluation.resources.main import ResourcesCSVKeys

TIME_START_KEY = ResourcesCSVKeys.TIME_SINCE_START.value
RUN_ID_KEY = ResourcesCSVKeys.EVALUATION_RUN_ID.value
STAGE_KEY = FLOpsExclusiveCSVKeys.FLOPS_PROJECT_STAGE.value
NUMBER_OF_TOTAL_STAGES = len(list(EvaluationRunFLOpsProjectStage))


CPU_KEY = ResourcesCSVKeys.CPU_USAGE.value
MEMORY_KEY = ResourcesCSVKeys.MEMORY_USAGE.value


DISK_START_KEY = ResourcesCSVKeys.DISK_SPACE_CHANGE_SINCE_START.value
DISK_LAST_KEY = ResourcesCSVKeys.DISK_SPACE_CHANGE_SINCE_LAST_MEASUREMENT.value


NETWORK_START_RECEIVED_KEY = ResourcesCSVKeys.NETWORK_RECEIVED_SINCE_START.value
NETWORK_START_SENT_KEY = ResourcesCSVKeys.NETWORK_SENT_SINCE_START.value
NETWORK_START_KEYS = [NETWORK_START_RECEIVED_KEY, NETWORK_START_SENT_KEY]

NETWORK_LAST_RECEIVED_KEY = ResourcesCSVKeys.NETWORK_RECEIVED_COMPARED_TO_LAST_MEASUREMENT.value
NETWORK_LAST_SENT_KEY = ResourcesCSVKeys.NETWORK_SENT_COMPARED_TO_LAST_MEASUREMENT.value
NETWORK_LAST_KEYS = [NETWORK_LAST_RECEIVED_KEY, NETWORK_LAST_SENT_KEY]


ACCURACY_KEY = FLOpsTrainedModelCSVKeys.ACCURACY.value
LOSS_KEY = FLOpsTrainedModelCSVKeys.LOSS.value
TRAINED_MODEL_RUN_ID_KEY = FLOpsTrainedModelCSVKeys.EVALUATION_RUN.value


class Cluster(enum.Enum):
    CLUSTER_A = "cluster_a"
    CLUSTER_B = "cluster_b"


NODE_KEY = "Node"
NODE_ROOT = "root"
NODE_CLUSTER_A = Cluster.CLUSTER_A.value
NODE_CLUSTER_B = Cluster.CLUSTER_B.value
