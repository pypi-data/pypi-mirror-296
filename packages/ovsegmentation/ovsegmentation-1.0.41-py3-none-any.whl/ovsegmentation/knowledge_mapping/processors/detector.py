from ovsegmentation.knowledge_mapping.processors.types import DETECTOR_TYPE
from ovsegmentation.knowledge_mapping.processors.detector_models import (
    GroundingDINOModel,
)


def create_detector_model(model_name, version: str, device, weights_path, **kwargs):
    """Create the object detector model
    Args:
        model_name (str): Name of the model
        version (str): Version of the model
        device (torch.device): device to run the model
    Returns:
        SAM model
    """
    if model_name == DETECTOR_TYPE.GrouningDINO:
        model = GroundingDINOModel(model_name, version, device, weights_path, **kwargs)
    else:
        raise ValueError(
            f"model {model_name} is not supported, supported models: {DETECTOR_TYPE}"
        )
    return model


class Detector(object):
    """Class for processing image and getting detections"""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        device: str = "cuda",
        weights_path: str = "weights",
        **kwargs,
    ):
        """Initializes the Detector class
        Args:
            model_name (str): Name of the model
            model_version (str): Version of the model
            device (torch.device): device to run the model
        """
        self.model_name = model_name
        self.model_version = model_version
        self.device = device
        self.weights_path = weights_path

        self.model = create_detector_model(
            self.model_name,
            self.model_version,
            self.device,
            self.weights_path,
            **kwargs,
        )

    def detect_objects(self, image, prompt):
        """Encode all objects in the bounding boxes.
        Args:
            image (PIL.Image.Image): input image
            prompt (str): text prompt
        Returns:
            boxes (torch.tensor): detection's boxes tensor
            logits (torch.tensor): detection confidence scores tensor
            phrases (List(str)): list of class labels
        """
        boxes, logits, phrases = self.model.detect_objects(image, prompt)

        return boxes, logits, phrases
