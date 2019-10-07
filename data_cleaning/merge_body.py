import glob
from dataloader import read_joint, write_joint
# colorTable
# 0=red, 1=green, 2=blue, 3=cyan(옥색?), 4=m(보라색), 5=y(노란색)

mode = 'R'  # {'C', 'R'}
fileIndex = 4010
startFrame = 0
endFrame = 221
correct_body = 0
incorrect_body = 5
remove_body_id = 1

path = 'C:/Users/user-1/Desktop/data/'
ref_files = glob.glob(path + '*/*.joint')
ref_file = ref_files[fileIndex]


def main():
    body_info = read_joint(ref_file)

    # CHANGE BODY MODE
    if mode == 'C':
        change_body(body_info, startFrame, endFrame, correct_body, incorrect_body)

    # REMOVE BODY MODE
    elif mode == 'R':
        remove_body(body_info, startFrame, endFrame, remove_body_id)

    else:
        print("non-existing mode('" + mode + "')")

    # save results
    write_joint(ref_file, body_info)


def change_body(body_info, begin, end, correct, incorrect):
    for f in range(begin, end+1):
        body_info[f][correct] = body_info[f][incorrect]
        body_info[f][correct]['body'] = correct
        body_info[f][incorrect] = None


def remove_body(body_info, begin, end, remove_body_id):
    for f in range(begin, end + 1):
        body_info[f][remove_body_id] = None


if __name__ == "__main__":
    main()
