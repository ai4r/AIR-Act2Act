import os
import numpy as np
from PIL import Image
import simplejson as json

from constants import *


def count_files(path):
    _, _, files = next(os.walk(path))
    return len(files)


def read_depth_map(path, cur_frame):
    png_path = path + "frame_" + str(cur_frame).zfill(3) + ".png"
    with open(png_path, 'rb') as file:
        data = Image.open(file)
        if data.width != DEPTH_SIZE[1] or data.height != DEPTH_SIZE[0]:
            raise ValueError('The depth map size should be {} X {}.'.format(DEPTH_SIZE[0], DEPTH_SIZE[1]))
        frame_data = np.asarray(data)
        fixed_data = [i / 8000 * 255 for i in frame_data]
        frame = np.reshape(fixed_data, (DEPTH_SIZE[0], DEPTH_SIZE[1]))
        frame = frame.astype(np.uint8)
    return frame


def read_body(path, cur_frame):
    png_path = path + "frame_" + str(cur_frame).zfill(3) + ".png"
    if not os.path.isfile(png_path):
        return None
    with open(png_path, 'rb') as file:
        data = Image.open(file)
        if data.width != DEPTH_SIZE[1] or data.height != DEPTH_SIZE[0]:
            raise ValueError('The depth map size should be {} X {}.'.format(DEPTH_SIZE[0], DEPTH_SIZE[1]))
        frame = np.asarray(data)
    return frame


def read_joint(path):
    if not os.path.isfile(path):
        return None
    with open(path) as fp:
        data = fp.read()
        body_info = json.loads(data)
    return body_info


def write_joint(path, body_info):
    with open(path, 'w') as fp:
        json.dump(body_info, fp, indent=2)
