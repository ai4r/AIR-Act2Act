import os
import glob
import shutil

download_path = "D:/download/"

video_path = os.path.join(download_path, 'video')
depth_path = os.path.join(download_path, 'depth')
body_path = os.path.join(download_path, 'body')
org_joint_path = os.path.join(download_path, 'org_joint')
ref_joint_path = os.path.join(download_path, 'ref_joint')
robott_path = os.path.join(download_path, 'robot')

output_path = "D:/AIR-Act2Act/"


def move_files(input_folder, output_folder):
    # check if data exists
    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        print('Info: there is no data in {}.'.format(input_folder))
        return

    # copy data
    input_data = glob.glob(os.path.join(input_folder, "*"))
    for data in input_data:
        # target path
        base_name = os.path.basename(data)
        data_name = base_name[:16]
        new_path = os.path.join(output_folder, data_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        # copy file or directory
        if os.path.isfile(data):
            shutil.copy(data, os.path.join(new_path, base_name))
        else:
            to_path = os.path.join(new_path, base_name)
            if os.path.exists(to_path):
                shutil.rmtree(to_path)
            shutil.copytree(data, to_path)


if __name__ == "__main__":
    # check if depth maps and joint files exist
    if not os.path.exists(depth_path) or not os.listdir(depth_path):
        raise Exception('There is no depth data in {}.'.format(depth_path))
    if not os.path.exists(ref_joint_path) or not os.listdir(ref_joint_path):
        raise Exception('There is no 3D skeletal data in {}.'.format(ref_joint_path))

    # move files
    move_files(video_path, output_path)
    move_files(depth_path, output_path)
    move_files(body_path, output_path)
    move_files(org_joint_path, output_path)
    move_files(ref_joint_path, output_path)
    move_files(robott_path, output_path)
