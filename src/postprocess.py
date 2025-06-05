"""
Decodificación mínima de YOLOv8-Pose (adaptar si cambiaron tus capas finales).

Suponemos:
  – output0: bounding‐boxes  Nx6   [x,y,w,h,obj_conf,class_conf]
  – output1: keypoints      Nx(17×3) = Nx51  [x,y,score] por punto
  – output2: (opcional) mask / heatmap – lo ignoramos

Si tus shapes son distintos rellena TODOs.
"""

import numpy as np
import cv2

# ──────────────────────────────────────────────────────────────
def decode(outputs, conf_thres=0.3):
    boxes_raw, kpts_raw, *_ = outputs
    boxes = []   # lista de (bbox, kpts)
    for bb, kp in zip(boxes_raw, kpts_raw):
        if bb[4] < conf_thres:
            continue
        x, y, w, h = bb[:4]
        bbox = np.array([x - w / 2, y - h / 2, x + w / 2, y + h / 2]).astype(int)
        # keypoints
        kpts = kp.reshape(-1, 3)           # (17,3)
        boxes.append((bbox, kpts))
    return boxes

# ──────────────────────────────────────────────────────────────
def draw(frame, boxes_kpts, color=(0, 255, 0)):
    for bbox, kpts in boxes_kpts:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        for x, y, conf in kpts:
            if conf > 0.1:
                cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)
