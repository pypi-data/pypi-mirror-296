import numpy as np
import matplotlib.pyplot as plt

from ovsegmentation.knowledge_mapping.processors.types import SAM_TYPE
from ovsegmentation.knowledge_mapping.processors.sam_models import (
    MobileSamModel,
)
from typing import Any


def show_anns(anns) -> None:
    """Show the annotations
    Args:
        anns: Annotations
    """
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones(
        (
            sorted_anns[0]["segmentation"].shape[0],
            sorted_anns[0]["segmentation"].shape[1],
            4,
        )
    )
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann["segmentation"]
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)


def create_sam_model(
    model_name, version: str, mode: str, device, weights_path, **kwargs
):
    """Create the SAM model
    Args:
        model_name (str): Name of the model
        version (str): Version of the model
        mode (str): Mode for generator (SegEvery) or predictor (SegAny)
        device (torch.device): device to run the model
    Returns:
        SAM model
    """
    if model_name == SAM_TYPE.MobileSAM:
        model = MobileSamModel(
            model_name,
            version,
            mode,
            device,
            weights_path,
            **kwargs,
        )
    else:
        raise ValueError(
            f"model {model_name} is not supported, supported models: {SAM_TYPE}"
        )
    return model


class SAM(object):
    """Class for Segmentation using models based on SAM"""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        mode: str,
        device,
        weights_path: str = "weights",
        **kwargs,
    ):
        """Initialize the SAM Classs
        Args:
            model_name (str): Name of the model
            model_version (str): Version of the model
            mode (str): mode for generation (SegEvery) or prediction (SegAny)
            device (torch.device): device to run the model
        """
        self.model_name = model_name
        self.model_version = model_version
        self.device = device
        self.weights_path = weights_path
        self.mode = mode

        self.model = create_sam_model(
            self.model_name,
            self.model_version,
            self.mode,
            self.device,
            self.weights_path,
            **kwargs,
        )

    def process(self, img, prompt: Any = None, id: int = 0):
        """Process data using the SAM model
        Args:
            img: Image to process
            id: Id of the image
        Returns:
            mask: Mask of the image
            xyxy: Bounding box of the image
            conf: Confidence of the image
        """
        raw_image = np.array(img)
        H, W, _ = raw_image.shape
        if self.mode == "generator":
            res = self.model.generate(raw_image)
        elif self.mode == "predictor":
            res = self.model.predict(raw_image, prompt)
        else:
            raise ValueError(f"Not supported SAM mode = {self.mode}")
        print(
            f"[DEBUG] {self.model_name} - {self.model_version} - {self.mode} >>> len(res): {len(res)}"
        )

        mask = []
        xyxy = []
        conf = []
        for r in res:
            mask.append(r["segmentation"])
            r_xyxy = r["bbox"].copy()

            if (
                self.model_name == SAM_TYPE.EfficientVit
                or self.model_name == SAM_TYPE.MobileSAM
                and self.model_version == "v1"
            ):
                # Convert from xyhw format to xyxy format
                r_xyxy[2] += r_xyxy[0]
                r_xyxy[3] += r_xyxy[1]

            xyxy.append(r_xyxy)
            conf.append(r["predicted_iou"])
        mask = np.array(mask)
        xyxy = np.array(xyxy)
        conf = np.array(conf)
        return mask, xyxy, conf
