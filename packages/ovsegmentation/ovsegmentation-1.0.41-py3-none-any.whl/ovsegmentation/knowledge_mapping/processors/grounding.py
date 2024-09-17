import os
import gzip
import pickle
import logging
import dataclasses
import numpy as np
import supervision as sv
from ovsegmentation.knowledge_mapping.utils import TimeProfiler
from ovsegmentation.knowledge_mapping.processors.sam import SAM
from supervision.draw.color import ColorPalette
from ovsegmentation.knowledge_mapping.processors.types import SAM_TYPE
import cv2


class Grounder(object):
    """Grounder class to ground the objects in the image"""

    def __init__(
        self,
        classes,
        cache_dir: str,
        device,
        sam_type: SAM_TYPE = SAM_TYPE.EfficientVit,
        sam_version: str = "l0",
        sam_mode: str = "generator",
        vlm_model=None,
        prompt: str = None,
        visualize: bool = False,
        **kwargs,
    ):
        """Initialize the Grounder
        Args:
            classes (List[str]): list of classes
            cache_dir (str): cache directory to save the grounding results
            device (torch.device): device to run the model
            sam_type (SAM_TYPE): SAM model type
            sam_version (str): SAM model version
            sam_mode (str): SAM mode for masks generation:
                generator (SegEvery) or predictor (SegAny)
            vlm_model (VLM): VLM model
            prompt (str): text prompt
            visualize (bool): flag to visualize the grounding results
        """
        self.sam = SAM(
            model_name=sam_type,
            model_version=sam_version,
            mode=sam_mode,
            device=device,
            **kwargs,
        )
        self.vlm = vlm_model
        self.visualize = visualize
        self.classes = classes
        self.prompt = prompt
        self.profiler = TimeProfiler()
        if self.visualize:
            self.box_annotator = sv.BoxAnnotator(
                color=ColorPalette.DEFAULT,
                text_scale=0.3,
                text_thickness=1,
                text_padding=2,
            )
            self.mask_annotator = sv.MaskAnnotator(color=ColorPalette.DEFAULT)
        self.cache_dir = cache_dir

    def process(self, img, idx: int):
        """Process the image and return the detections
        Args:
            img (PIL.Image.Image): input image
            idx (int): image index
        Returns:
            dict: dictionary containing the detections and the visualized image
        """
        with self.profiler.measure("Grounder.process"):
            mask, xyxy, conf = self.sam.process(img)
        with self.profiler.measure("Grounder.convert_to_detections"):
            detections = sv.Detections(
                xyxy=xyxy,
                confidence=conf,
                #  Right now, we have only one class ["item"]
                class_id=np.zeros_like(conf).astype(int),
                mask=mask,
            )
        with self.profiler.measure("Grounder.vlm_encoding"):
            image_feats, text_feats = self.vlm.encode_bboxes(
                img, detections=detections, prompt=self.prompt, classes=self.classes
            )

        annotated_image = None

        if self.visualize:
            annotated_image = self._visualize(np.array(img), detections)

        # ---------
        # tmp for DEBUG
        if self.visualize:
            annotated_image = self._visualize(
                image=np.array(img),
                detections=detections,
                instance_random_color=True,
                draw_bbox=False,
            )
            save_path = os.path.join(self.cache_dir, "grounding_results_annotated")
            print(f"save_path: {save_path}")
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cv2.imwrite(
                f"{save_path}/{str(0 + int(idx)).zfill(6)}_annotated_{self.sam.model_name.value}_{self.sam.model_version}.png",
                annotated_image[0],
            )
            print(f"text_feats: {text_feats}")
        # ---------

        results = {
            "id": idx,
            "xyxy": detections.xyxy,
            "confidence": detections.confidence,
            "class_id": detections.class_id,
            "mask": detections.mask,
            "classes": self.classes,
            "image_feats": image_feats,
            "text_feats": text_feats,
            "annotated_image": annotated_image,
        }

        save_results_folder = os.path.join(self.cache_dir, "grounding_results")
        if not os.path.exists(save_results_folder):
            os.makedirs(save_results_folder)

        try:
            with gzip.open(
                os.path.join(save_results_folder, idx + ".pkl.gz"), "wb"
            ) as f:
                pickle.dump(results, f)
                print(f"Saved grounding results for {idx}")
        except Exception as e:
            logging.error(
                f"Failed to save grounding results for {idx}.\n \
                due to {e}"
            )
            assert False
        return results

    def _visualize(
        self,
        image: np.ndarray,
        detections: sv.Detections,
        instance_random_color: bool = False,
        draw_bbox: bool = True,
    ):
        """Annotate the image with the detection results.
        Args:
            image (np.ndarray): input image
            detections (sv.Detections): detection results
            instance_random_color (bool): flag to generate random
            colors for each segmentation
            draw_bbox (bool): flag to draw bounding boxes
        """
        labels = [
            f"{self.classes[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, _, _ in detections
        ]

        if instance_random_color:
            detections = dataclasses.replace(detections)
            detections.class_id = np.arange(len(detections))

        annotated_image = self.mask_annotator.annotate(
            scene=image.copy(), detections=detections
        )

        if draw_bbox:
            annotated_image = self.box_annotator.annotate(
                scene=annotated_image, detections=detections
            )
        return annotated_image, labels
