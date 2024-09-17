from enum import Enum


class SAM_TYPE(Enum):
    EfficientVit = "efficientvit"
    MobileSAM = "mobilesam"


class DETECTOR_TYPE(Enum):
    GrouningDINO = "grounding_dino"
