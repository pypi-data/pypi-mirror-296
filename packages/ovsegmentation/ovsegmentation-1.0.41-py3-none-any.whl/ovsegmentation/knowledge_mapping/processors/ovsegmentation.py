import torch
import numpy as np
import os
import sys
import warnings

warnings.filterwarnings("ignore")
BASE_PATH = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH + "/knowledge_mapping/third_party/mobilesam")
sys.path.append(BASE_PATH + "/knowledge_mapping/third_party/mobilesam/MobileSAMv2")
sys.path.append(BASE_PATH + "/knowledge_mapping/third_party/GroundingDINO")

from ovsegmentation.knowledge_mapping.processors.types import SAM_TYPE, DETECTOR_TYPE
from ovsegmentation.knowledge_mapping.processors.sam import SAM
from ovsegmentation.knowledge_mapping.processors.detector import Detector
from typing import Dict, Any

import supervision as sv
from PIL import Image
import matplotlib.pyplot as plt
from supervision.draw.color import ColorPalette
import dataclasses
import open3d as o3d


def get_waypoint(depth_image, mask, params, transform_matrix):
    intrinsics = o3d.camera.PinholeCameraIntrinsic(
        width=params["width"],
        height=params["height"],
        fx=params["intrinsics"]["fx"],
        fy=params["intrinsics"]["fy"],
        cx=params["intrinsics"]["cx"],
        cy=params["intrinsics"]["cy"],
    )
    tmp = mask.copy().astype("int")
    tmp[mask != 0] = depth_image[mask != 0]
    depth = o3d.geometry.Image(np.asarray(tmp, dtype=np.uint16))
    pcd = o3d.geometry.PointCloud.create_from_depth_image(
        depth=depth,
        intrinsic=intrinsics,
        depth_scale=params["depth_scale"],
        stride=1,
    )
    if transform_matrix is not None:
        pcd.transform(transform_matrix)
    # pcd_centroid = pcd.get_center() # mean
    pcd_centroid = np.median(np.asarray(pcd.points), axis=0)  # median
    return pcd_centroid


class OVSegmentation:
    def __init__(self, detector: Detector, segmenter: SAM) -> None:
        """_summary_

        Args:
            detector (Detector): object detection model
            segmenter (SAM): segment anything model
        """
        self.detector = detector
        self.segmenter = segmenter

    def generate_masks(self, input_data: Dict[str, Any]):
        image: np.ndarray = Image.fromarray(input_data["image"])
        mask, xyxy, conf = self.segmenter.process(image)
        results = {
            "mask": np.array(mask),
            "bbox": np.array(xyxy),
            "mask_confidence": np.array(conf),
            "class_label": None,
            "waypoint": None,
        }
        return results

    def get_detections(self, input_data: Dict[str, Any], detect_most_confident=False):
        if self.segmenter.mode == "generator":
            return self.generate_masks(input_data)

        image: np.ndarray = Image.fromarray(input_data["image"])
        prompt_ovd = input_data["text"]
        depth_image = input_data["depth"]
        intrinsics = input_data["intrinsics"]
        transform_matrix = input_data["tf"]

        boxes, logits, class_labels = self.detector.detect_objects(image, prompt_ovd)
        # classes = list(set(prompt_ovd.split(".")))
        # print(f"[OV-DETECTOR]:\n boxes:{boxes}\n logits:{logits}\n class_labels:{class_labels}")
        if boxes.numel() != 0:
            mask, xyxy, conf = self.segmenter.process(image, boxes)
            # print(f"[SAM]:\n mask:{mask}\n xyxy:{xyxy}\n conf:{conf}")
            # convert to detections
            detections = sv.Detections(
                xyxy=boxes.to(int).detach().cpu().numpy(),
                confidence=logits.detach().cpu().numpy(),
                class_id=np.array([n for n, cl in enumerate(class_labels)]),
                mask=mask,
            )

            if detect_most_confident:
                # assumed we have only one class to detect
                # select from detections most confident object
                # get 3d waypoint
                idx = np.argmax(detections.confidence)
                mask = detections.mask[idx]
                waypoint = get_waypoint(depth_image, mask, intrinsics, transform_matrix)
                # print(f"[WAYPOINT]:\n {waypoint}")

                results = {
                    "mask": np.array([detections.mask[idx]]),
                    "bbox": np.array([detections.xyxy[idx]]),
                    "detection_confidence": np.array([detections.confidence[idx]]),
                    "class_label": [class_labels[idx]],
                    "waypoint": np.array([waypoint]),
                }
            else:
                waypoints = []
                for i in range(len(detections.mask)):
                    waypoint = get_waypoint(
                        depth_image, detections.mask[i], intrinsics, transform_matrix
                    )
                    waypoints.append(waypoint)
                results = {
                    "mask": np.array(detections.mask),
                    "bbox": np.array(detections.xyxy),
                    "detection_confidence": np.array(detections.confidence),
                    "class_label": class_labels,
                    "waypoint": np.array(waypoints),
                }
        else:
            results = {
                "mask": None,
                "bbox": None,
                "detection_confidence": None,
                "class_label": None,
                "waypoint": None,
            }
        return results


def visualize(
    image: np.ndarray,
    res: Dict[str, Any],
    instance_random_color: bool = False,
    draw_bbox: bool = True,
):
    """Annotate the image with the detection results.
    Args:
        image (np.ndarray): input image
        detections: detection results
        instance_random_color (bool): flag to generate random
        colors for each segmentation
        draw_bbox (bool): flag to draw bounding boxes
    """
    box_annotator = sv.BoxAnnotator(
        color=ColorPalette.default(),
        text_scale=0.3,
        text_thickness=1,
        text_padding=2,
    )
    mask_annotator = sv.MaskAnnotator(color=ColorPalette.default())
    labels = None
    if res["class_label"]:
        classes = list(set(res["class_label"]))
        class_to_id = {cls: idx for idx, cls in enumerate(classes)}
        id_to_class = {value: key for key, value in class_to_id.items()}
        detections = sv.Detections(
            xyxy=res["bbox"],
            confidence=res["detection_confidence"],
            class_id=np.array([class_to_id[cls] for cls in res["class_label"]]),
            mask=res["mask"],
        )

        labels = [
            f"{id_to_class[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, _ in detections
        ]
    else:
        detections = sv.Detections(
            xyxy=res["bbox"],
            confidence=res["mask_confidence"],
            class_id=None,
            mask=res["mask"],
        )

    if instance_random_color:
        detections = dataclasses.replace(detections)
        detections.class_id = np.arange(len(detections))

    annotated_image = mask_annotator.annotate(scene=image.copy(), detections=detections)

    if draw_bbox:
        if labels:
            annotated_image = box_annotator.annotate(
                scene=annotated_image, detections=detections, labels=labels
            )
        else:
            annotated_image = box_annotator.annotate(
                scene=annotated_image, detections=detections
            )
    return annotated_image, labels


def build_segmentator(weights_path="weights"):
    args = {
        "sam": {
            "sam_type": SAM_TYPE.MobileSAM,
            "sam_version": "v1",
            "sam_mode": "predictor",
            "v2_inference_type": "torch",
            "kwargs": {},
        },
        "detector": {
            "detector_type": DETECTOR_TYPE.GrouningDINO,
            "model_version": "SwinT",
            "kwargs": {},
        },
        "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    }
    if (
        args["sam"]["sam_version"] == "v2"
        and args["sam"]["v2_inference_type"] == "torch"
        and args["sam"]["sam_mode"] == "generator"
    ):
        raise ValueError(
            "v2 torch model does not support generator mode. Please change to trt inference type or to v1 version"
        )
    detector = None
    if args["detector"] is not None:
        detector = Detector(
            model_name=args["detector"]["detector_type"],
            model_version=args["detector"]["model_version"],
            device=args["device"],
            weights_path=weights_path,
            **args["detector"]["kwargs"],
        )
    segmenter = SAM(
        model_name=args["sam"]["sam_type"],
        model_version=args["sam"]["sam_version"],
        mode=args["sam"]["sam_mode"],
        device=args["device"],
        weights_path=weights_path,
        v2_inference_type=args["sam"]["v2_inference_type"],
        **args["sam"]["kwargs"],
    )

    return OVSegmentation(detector, segmenter)
