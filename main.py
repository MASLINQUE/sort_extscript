#!/usr/bin/env python3

import logging
import sys
import json
from framework import FrameWorker
import argparse
import traceback

# from distutils.util import strtobool
logging.basicConfig(filename = 'errors.log', level = logging.ERROR)

parser = argparse.ArgumentParser()

parser.add_argument("--minhit", help="Min hits", default=1, type=int)
parser.add_argument("--maxunm", help="Max unmatches before delete", default=3, type=int)
parser.add_argument("--iou", help="IOU threshold 0-1", default=0.4, type=float)
# parser.add_argument('--predunm', help="Use prediction on unmatched trackers", default=False, type=lambda x:bool(strtobool(x)))

args = parser.parse_args()
worker = FrameWorker(args.minhit, args.maxunm, args.iou)

# with open("logs.txt", "a") as f:
#     f.write("Line read\n")


while True:
    try:
        line = sys.stdin.readline()
        if len(line) < 3:
            continue


        frame = json.loads(line)

        worker.frame_processing(frame)
        sys.stdout.write(json.dumps(frame))
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        with open('log.txt', 'a') as f:
            f.write(str(e))
            f.write(traceback.format_exc())

# for line in sys.stdin:
#     if len(line) < 3:
#         continue

#     try:
#         frame = json.loads(line)
#     except EOFError as e:
#         logging.error('Error occurred ' + str(e))



#     worker.frame_processing(frame)

#     sys.stdout.write(json.dumps(frame))
#     sys.stdout.write("\n")
#     sys.stdout.flush()

