# depth map size : [height, width]
DEPTH_SIZE = [424, 512]

# number of joints
JOINT_COUNT = 25

# maximum number of people
BODY_COUNT = 6

# connecting joint id
CONNECTING_JOINTS = [1, 0, 20, 2, 20, 4, 5, 6, 20, 8, 9, 10, 0, 12, 13, 14, 0, 16, 17, 18, 1, 7, 7, 11, 11]

# colors to draw bodies
BODY_COLORS = [(204, 0, 0), (0, 204, 0), (0, 0, 204), (0, 204, 204), (204, 0, 204), (204, 204, 0)]
LINE_COLORS = [tuple(int(num / 2) for num in item) for item in BODY_COLORS]

# colors to draw joints
JOINT_COLORS = [(0, 0, 160), (64, 0, 128), (255, 128, 64), (64, 128, 128), (255, 128, 192), (0, 255, 0),
                (128, 64, 64), (0, 128, 255), (128, 128, 128), (128, 128, 0), (0, 255, 255), (255, 128, 64),
                (64, 0, 128), (128, 64, 0), (0, 0, 0), (128, 128, 192), (0, 64, 128), (64, 0, 64), (128, 0, 255),
                (255, 0, 255), (0, 128, 192), (0, 128, 64), (0, 0, 64), (255, 255, 128), (0, 128, 128)]
