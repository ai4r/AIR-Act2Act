"""
correcting (or removing) inaccurate data
"""
import shutil
import glob
from dataloader import read_joint, write_joint

mode = 'F'  # {'I', 'F', 'M'}
startFrame = 0
endFrame = 121
referenceFrame = 122
body = 'RAA'
b = 0
fileIndex = 460

path = 'C:/Users/user-1/Desktop/data/'
files = glob.glob(path + '*/*.joint')
file = files[fileIndex]

# Path = "C:/Users/wrko/Desktop/C001/"
# newPath = "C:/Users/wrko/Desktop/C001/new/"
BODY_PART = {  # --------------상체부
             'LA': [5, 6, 7, 21, 22],                        # 왼팔
             'RA': [9, 10, 11, 23, 24],                      # 오른팔
             'DA': [5, 6, 7, 21, 22, 9, 10, 11, 23, 24],     # 양팔
             'LS': [4],                                      # 왼쪽 어깨
             'RS': [8],                                      # 오른쪽 어깨
            'LAA': [4, 5, 6, 7, 21, 22],                     # 왼팔 전체
            'RAA': [8, 9, 10, 11, 23, 24],                   # 오른팔 전체
               # --------------하체부
             'LL': [13, 14],                              # 왼쪽 종아리
             'RL': [17, 18],                              # 오른쪽 종아리
             'LT': [12, 13],                              # 왼쪽 허벅지
             'RT': [16, 17],                              # 오른쪽 허벅지
            'LLA': [12, 13, 14, 15],                       # 왼쪽 다리 전체
            'RLA': [16, 17, 18, 19],                       # 오른쪽 다리 전체
             'LF': [15],                                  # 왼발
             'RF': [19],                                  # 오른발
               # --------------기타
             'ALL': [j for j in range(25)],             # 전신
             'WS': [12, 0, 16],                         # 허리
             'HD': [3, 2, 20]}                          # 머리-목뼈


def main():
    body_info = read_joint(file)
    shutil.copyfile(file, file + '_backup')

    #INTERPOLATION MODE (filename, mode, start frame, end frame, body part)
    if mode == 'I':
        for f in range(startFrame, endFrame+1):
            interpolate(body_info[startFrame-1][b], body_info[endFrame+1][b], body_info[f][b],
                        (f - startFrame) / (endFrame - startFrame), BODY_PART[body])

    #FIX MODE (filename, mode, start frame, end frame , reference frame, body part)
    elif mode == 'F':
        fix_body(body_info, startFrame, endFrame, BODY_PART[body], referenceFrame)

    #MAKE NULL MODE
    elif mode == 'M':
        make_null(body_info, startFrame, endFrame, BODY_PART[body])

    else:
        print("non-existing mode('" + mode + "')")

    # write body_info in file
    write_joint(file, body_info)


def fix_body(body_info, begin, end, part, ref_frame):
    for f in range(begin, end+1):
        for j in part:
            body_info[f][b]["joints"][j] = body_info[ref_frame][b]["joints"][j]


def interpolate(begin, end, out, step, part):

    # 3D location of the joint j
    for j in part:
        out["joints"][j]["x"] = begin["joints"][j]["x"] + (end["joints"][j]["x"] - begin["joints"][j]["x"]) * step
        out["joints"][j]["y"] = begin["joints"][j]["y"] + (end["joints"][j]["y"] - begin["joints"][j]["y"]) * step
        out["joints"][j]["z"] = begin["joints"][j]["z"] + (end["joints"][j]["z"] - begin["joints"][j]["z"]) * step

    # 2D location of the joint j in corresponding depth frame
    for j in part:
        out["joints"][j]["depthX"] = begin["joints"][j]["depthX"] + (end["joints"][j]["depthX"] - begin["joints"][j]["depthX"]) * step
        out["joints"][j]["depthY"] = begin["joints"][j]["depthY"] + (end["joints"][j]["depthY"] - begin["joints"][j]["depthY"]) * step


def make_null(body_info, begin, end, part):
    for f in range(begin, end + 1):
        for j in part:
            body_info[f][b]["joints"][j]["x"] = 0
            body_info[f][b]["joints"][j]["y"] = 0
            body_info[f][b]["joints"][j]["z"] = 0

            body_info[f][b]["joints"][j]["depthX"] = 0
            body_info[f][b]["joints"][j]["depthY"] = 0


if __name__ == "__main__":
    main()
