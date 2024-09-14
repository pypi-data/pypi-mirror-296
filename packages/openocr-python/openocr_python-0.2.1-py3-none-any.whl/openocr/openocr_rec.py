import numpy as np
import math
import time
import os
import sys
import cv2

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "../..")))

from postprocess import build_post_process
from utility import create_predictor

class OpenOCRRec(object):
    def __init__(self):
        self.rec_image_shape = [3, 48, 320]
        self.rec_batch_num = 6
        self.rec_algorithm = "SVTR_LCNet"

        current_dir = os.path.dirname(__file__)

        postprocess_params = {
            "name": "CTCLabelDecode",
            "character_dict_path": os.path.join(current_dir,"doc/ppocr_keys_v1.txt"),
            "use_space_char": True,
        }

        self.postprocess_op = build_post_process(postprocess_params)
        self.postprocess_params = postprocess_params

        (
            self.predictor,
            self.input_tensor,
            self.output_tensors,
            self.config,
        ) = create_predictor("rec")

        self.return_word_box = False

    def __call__(self,img_list):
        img_num = len(img_list)
        # Calculate the aspect ratio of all text bars
        width_list = []
        for img in img_list:
            width_list.append(img.shape[1] / float(img.shape[0]))

        indices = np.argsort(np.array(width_list))
        rec_res = [["", 0.0]] * img_num
        batch_num = self.rec_batch_num
        st = time.time()

        for beg_img_no in range(0, img_num, batch_num):
            end_img_no = min(img_num, beg_img_no + batch_num)
            norm_img_batch = []
            imgC, imgH, imgW = self.rec_image_shape[:3]
            max_wh_ratio = imgW / imgH
            wh_ratio_list = []
            for ino in range(beg_img_no, end_img_no):
                h, w = img_list[indices[ino]].shape[0:2]
                wh_ratio = w * 1.0 / h
                max_wh_ratio = max(max_wh_ratio, wh_ratio)
                wh_ratio_list.append(wh_ratio)
            for ino in range(beg_img_no, end_img_no):
                norm_img = self.resize_norm_img(
                    img_list[indices[ino]], max_wh_ratio
                )
                norm_img = norm_img[np.newaxis, :]
                norm_img_batch.append(norm_img)
            norm_img_batch = np.concatenate(norm_img_batch)
            norm_img_batch = norm_img_batch.copy()

            self.input_tensor.copy_from_cpu(norm_img_batch)
            self.predictor.run()
            outputs = []
            for output_tensor in self.output_tensors:
                output = output_tensor.copy_to_cpu()
                outputs.append(output)

            if len(outputs) != 1:
                preds = outputs
            else:
                preds = outputs[0]

            rec_result = self.postprocess_op(
                    preds,
                    return_word_box=self.return_word_box,
                    wh_ratio_list=wh_ratio_list,
                    max_wh_ratio=max_wh_ratio,
                )
            for rno in range(len(rec_result)):
                rec_res[indices[beg_img_no + rno]] = rec_result[rno]

        return rec_res, time.time() - st
    

    def resize_norm_img(self, img, max_wh_ratio):
        imgC, imgH, imgW = self.rec_image_shape

        assert imgC == img.shape[2]
        imgW = int((imgH * max_wh_ratio))
        h, w = img.shape[:2]
        ratio = w / float(h)
        if math.ceil(imgH * ratio) > imgW:
            resized_w = imgW
        else:
            resized_w = int(math.ceil(imgH * ratio))
        resized_image = cv2.resize(img, (resized_w, imgH))
        resized_image = resized_image.astype("float32")
        resized_image = resized_image.transpose((2, 0, 1)) / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((imgC, imgH, imgW), dtype=np.float32)
        padding_im[:, :, 0:resized_w] = resized_image
        return padding_im
