import numpy as np
import time
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "../..")))


from data import create_operators,transform
from postprocess import build_post_process
from utility import create_predictor

class OpenOCRDet(object):
    def __init__(self):
        self.det_algorithm = "DB"

        pre_process_list = [
            {
                "DetResizeForTest": {
                    "limit_side_len": 960.,
                    "limit_type": "max",
                }
            },
            {
                "NormalizeImage": {
                    "std": [0.229, 0.224, 0.225],
                    "mean": [0.485, 0.456, 0.406],
                    "scale": "1./255.",
                    "order": "hwc",
                }
            },
            {"ToCHWImage": None},
            {"KeepKeys": {"keep_keys": ["image", "shape"]}},
        ]

        postprocess_params = {
            "name": "DBPostProcess",
            "thresh": 0.3,
            "box_thresh": 0.6,
            "max_candidates": 1000,
            "unclip_ratio": 1.5,
            "use_dilation": False,
            "score_mode": "fast",
            "box_type": "quad"
        }

        self.preprocess_op = create_operators(pre_process_list)
        self.postprocess_op = build_post_process(postprocess_params)

        (
            self.predictor,
            self.input_tensor,
            self.output_tensors,
            self.config,
        ) = create_predictor("det")

        self.preprocess_op = create_operators(pre_process_list)

    def __call__(self, img):
        dt_boxes, elapse = self.predict(img)
        return dt_boxes, elapse
    

    def predict(self, img):

        ori_im = img.copy()
        data = {"image": img}

        st = time.time()
        data = transform(data, self.preprocess_op)
        img, shape_list = data
        if img is None:
            return None, 0
        img = np.expand_dims(img, axis=0)
        shape_list = np.expand_dims(shape_list, axis=0)
        img = img.copy()

        self.input_tensor.copy_from_cpu(img)
        self.predictor.run()
        outputs = []
        for output_tensor in self.output_tensors:
            output = output_tensor.copy_to_cpu()
            outputs.append(output)

        preds = {"maps":outputs[0]}
        post_result = self.postprocess_op(preds, shape_list)
        dt_boxes = post_result[0]["points"]

        dt_boxes = self.filter_tag_det_res(dt_boxes, ori_im.shape)

        et = time.time()
        return dt_boxes, et - st
    
    def filter_tag_det_res(self, dt_boxes, image_shape):
        img_height, img_width = image_shape[0:2]
        dt_boxes_new = []
        for box in dt_boxes:
            if type(box) is list:
                box = np.array(box)
            box = self.order_points_clockwise(box)
            box = self.clip_det_res(box, img_height, img_width)
            rect_width = int(np.linalg.norm(box[0] - box[1]))
            rect_height = int(np.linalg.norm(box[0] - box[3]))
            if rect_width <= 3 or rect_height <= 3:
                continue
            dt_boxes_new.append(box)
        dt_boxes = np.array(dt_boxes_new)
        return dt_boxes
    
    def order_points_clockwise(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        tmp = np.delete(pts, (np.argmin(s), np.argmax(s)), axis=0)
        diff = np.diff(np.array(tmp), axis=1)
        rect[1] = tmp[np.argmin(diff)]
        rect[3] = tmp[np.argmax(diff)]
        return rect
    
    def clip_det_res(self, points, img_height, img_width):
        for pno in range(points.shape[0]):
            points[pno, 0] = int(min(max(points[pno, 0], 0), img_width - 1))
            points[pno, 1] = int(min(max(points[pno, 1], 0), img_height - 1))
        return points