#!/usr/bin/env python3

import numpy as np
import sort as st
from utils import IOU

class FrameWorker():
    def __init__(self, maxpred, maxunm, iou) -> None:
        self.cameras = {}
        self.maxpred, self.maxunm, self.iou = maxpred, maxunm, iou,


    def add_tracker(self, id):
        self.cameras[id] = st.Sort(max_age=self.maxunm, min_hits=1, iou_threshold=self.iou)

    def frame_processing(self, frame):
        items_default = frame.get('items')
        if items_default:
            cam_id = frame.get('camera')["id"]

            if cam_id not in self.cameras:
                self.add_tracker(cam_id)

            mot_tracker = self.cameras[cam_id]

            track_boxes = []
            for item in items_default:
                score = item["prob"]
                x, y, w, h = item["bbox"]
                bbox_body = [x, y, x+w, y+h, score]
                track_boxes.append(bbox_body)
        
            track_boxes = np.array(track_boxes)
            if len(track_boxes) != 0:
                tracker = mot_tracker.update(track_boxes)
            else:
                tracker = mot_tracker.update(np.empty((0, 5)))



            tracker = tracker.round(3)

            while tracker:
                track = tracker.pop()
                for i in range(len(items_default)):
                    if track[0:4] == items_default[i]:
                        items_default[i]["id"] = str(int(track[4]))
                        items_default.pop(i)
                        break


            # for item, track in zip(items_default, tracker):
            #     item["id"] = str(int(track[4]))

            frame.update({'items': items_default})
            self.cameras[cam_id] = mot_tracker