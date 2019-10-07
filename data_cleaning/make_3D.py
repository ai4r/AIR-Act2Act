from constants import *
from PIL import Image
import numpy as np
import glob
from dataloader import read_joint, write_joint

path = 'C:/Users/user-1/Desktop/data/'
files = glob.glob(path + '*/*.~joint')
startIndex = 154
nData = 1

px = 255
py = 211
hfov = 70 * np.pi / 180
vfov = 60 * np.pi / 180
fx = px / np.tan(hfov * 0.5)
fy = py / np.tan(vfov * 0.5)


# info: this is different from dataloader.read_depth_map in scale
def read_depth_map(path, cur_frame):
    png_path = path + "frame_" + str(cur_frame).zfill(3) + ".png"
    with open(png_path, 'rb') as file:
        data = Image.open(file)
        if data.width != DEPTH_SIZE[1] or data.height != DEPTH_SIZE[0]:
            raise ValueError('The depth map size should be {} X {}.'.format(DEPTH_SIZE[0], DEPTH_SIZE[1]))
        frame_data = np.asarray(data)
        frame = np.reshape(frame_data, (DEPTH_SIZE[0], DEPTH_SIZE[1]))
        # frame = frame.astype(np.uint8)
    return frame


def isError(body_info, f, b, j):
    if body_info[f][b]["joints"][j]["z"] == 0:
        return True

    if abs(body_info[f][b]["joints"][j]["x"] - body_info[f][b]["joints"][CONNECTING_JOINTS[j]]["x"]) > 0.8 or \
            abs(body_info[f][b]["joints"][j]["y"] - body_info[f][b]["joints"][CONNECTING_JOINTS[j]]["y"]) > 0.8 or \
            abs(body_info[f][b]["joints"][j]["z"] - body_info[f][b]["joints"][CONNECTING_JOINTS[j]]["z"]) > 0.8:
        return True

    if f >= 1 and \
            abs(body_info[f][b]["joints"][j]["z"] - body_info[f-1][b]["joints"][j]["z"]) > 0.3:
        return True

    return False


def remakeXY_from_Z(body_info):
    for f in range(len(body_info)):
        for b in range(BODY_COUNT):
            if body_info[f][b] is None:
                continue
            for j in range(JOINT_COUNT):
                if not body_info[f][b]["joints"][j]["z"]:
                    continue
                depth = body_info[f][b]["joints"][j]["z"]
                body_info[f][b]["joints"][j]["x"] = (body_info[f][b]["joints"][j]["depthX"] - px)\
                                                    * depth / fx
                body_info[f][b]["joints"][j]["y"] = (py - body_info[f][b]["joints"][j]["depthY"]) \
                                                    * depth / fy
    return body_info


def transform_body_info(skeleton_file, depth_path):
    body_info = read_joint(skeleton_file)
    name = skeleton_file.split('\\')[-1].split('.')[0]

    for f in range(len(body_info)):
        depth_data = read_depth_map(depth_path, f)
        for b in range(BODY_COUNT):
            if body_info[f][b] is None:
                continue
            for j in range(JOINT_COUNT):
                body_info[f][b]["joints"][j]["x"] = 0
                body_info[f][b]["joints"][j]["y"] = 0
                body_info[f][b]["joints"][j]["z"] = 0
                if body_info[f][b]["joints"][j]["depthX"] != 0:
                    depth = depth_data[body_info[f][b]["joints"][j]["depthY"]] \
                                [body_info[f][b]["joints"][j]["depthX"]] / 1000
                    body_info[f][b]["joints"][j]["x"] = (body_info[f][b]["joints"][j]["depthX"] - px) \
                                                        * (depth) / fx
                    body_info[f][b]["joints"][j]["y"] = (py - body_info[f][b]["joints"][j]["depthY"]) \
                                                        * (depth) / fy
                    body_info[f][b]["joints"][j]["z"] = depth

    for f in range(0, len(body_info)):
        for b in range(len(body_info[0])):
            if body_info[f][b] is None:
                continue

            for j in range(JOINT_COUNT):
                if body_info[f][b]["joints"][j]["depthX"] == 0 and \
                        body_info[f][b]["joints"][j]["depthY"] == 0:
                    continue

                f_ref = 0 if f == 0 else f - 1
                if f != 0 and body_info[f-1][b]["joints"][j]["depthX"] == 0 and \
                        body_info[f-1][b]["joints"][j]["depthY"] == 0:
                    f_ref = f

                if isError(body_info, f, b, j):  # and body_info[f - 1][b]["joints"][j]["z"] != 0:
                    depth_info = read_depth_map(depth_path, f)
                    square = list()

                    for c in range(11):
                        for r in range(11):
                            if not 424 > body_info[f][b]["joints"][j]["depthY"] - 5 + c >= 0 or \
                             not 512 > body_info[f][b]["joints"][j]["depthX"] - 5 + r >= 0:
                                square.append(0)
                            else:
                                square.append(depth_info[body_info[f][b]["joints"][j]["depthY"] - 5 + c]\
                                                  [body_info[f][b]["joints"][j]["depthX"] - 5 + r])
                    # body_info[f][body_id[b]]["joints"][j]["z"] = min([x for x in square if x != 0]) / 1000
                    difference_matrix = [abs(body_info[f_ref][b]["joints"][j]["z"]-x) for x in square]
                    body_info[f][b]["joints"][j]["z"] = square[difference_matrix.index(min(difference_matrix))] / 1000
                    if isError(body_info, f, b, j):
                        new_j = find_correct_joint(body_info[f_ref][b]["joints"], j)
                        body_info[f][b]["joints"][j]["z"] = body_info[f_ref][b]["joints"][new_j]["z"]
    body_info = remakeXY_from_Z(body_info)
    return body_info


def find_correct_joint(joints, cur_j):
    new_j = CONNECTING_JOINTS[cur_j]
    for iter in range(JOINT_COUNT):
        if joints[new_j]["z"] != 0:
            return new_j
        else:
            new_j = CONNECTING_JOINTS[new_j]
    print("cannot find correct joint.")
    return cur_j


def cut_float(var):
    if var != 0:
        var = float('%.3f' % var)
    return var


def main():
    selected_files = files[startIndex:startIndex + nData]
    for cur, file in enumerate(selected_files):
        name = file.split('\\')[-1].split('.')[0]
        new_file = path + name + '/' + name + '.joint'

        depth_path = path + name + '/' + name + '_depth/'
        body_info = transform_body_info(file, depth_path)
        for f in range(len(body_info)):
            for b in range(len(body_info[0])):
                if body_info[f][b] is None:
                    continue

                body_info[f][b]['type'] = 'refined'
                for j in range(25):
                    del body_info[f][b]['joints'][j]['depthZ']
                    body_info[f][b]['joints'][j]['x'] = cut_float(body_info[f][b]['joints'][j]['x'])
                    body_info[f][b]['joints'][j]['y'] = cut_float(body_info[f][b]['joints'][j]['y'])
                    body_info[f][b]['joints'][j]['z'] = cut_float(body_info[f][b]['joints'][j]['z'])

        # save results
        write_joint(new_file, body_info)
        print('{}/{}: {}'.format(startIndex + cur, startIndex + len(selected_files) - 1, name))


if __name__ == '__main__':
    main()
