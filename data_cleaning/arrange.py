import glob
from dataloader import read_joint, write_joint
from constants import BODY_COUNT

path = 'C:/Users/user-1/Desktop/data/'
files = glob.glob(path + '*/*.joint')
startIndex = 154
nData = 1


def main():
    selected_files = files[startIndex:startIndex + nData]
    for cur, file in enumerate(selected_files):
        body_info = read_joint(file)
        name = file.split('\\')[-1].split('.')[0]

        if "C001" in name or "C002" in name:
            n_max_skeletons = 1
        elif "C003" in name:
            n_max_skeletons = 2
        else:
            print("Wrong File: " + file)
            continue

        # detect available body ID
        available_body_id = list()
        for b in range(BODY_COUNT):
            for f in range(len(body_info)):
                if b in available_body_id or body_info[f][b] is None:
                    break
                for j in range(25):
                    if any([body_info[f][b]['joints'][j][c] != 0 for c in ['depthX', 'depthY', 'x', 'y', 'z']]):
                        available_body_id.append(b)
                        break
        if len(available_body_id) > 2:
            print("Wrong Body Count: " + file)
            # continue

        # arrange bodies
        f_start = 0
        if "A001" in name:
            for f in range(len(body_info)):
                for b in range(BODY_COUNT):
                    if body_info[f][b] is None:
                        continue
                    if body_info[f][b]['joints'][20]['depthX'] != 0:
                        f_start = f
                        break
                if f_start != 0:
                    break

        s = sorted(available_body_id, key=lambda b: -body_info[f_start][b]['joints'][20]['depthX'])
        new_body_info = list()
        for f in range(len(body_info)):
            bodies = list()
            body_count = BODY_COUNT
            if "C001" in name:
                bodies.append(None)
                body_count -= 1
            for b in range(body_count):
                if "C002" in name and b == 1:
                    bodies.append(None)
                if "C003" in name and b >= len(s):
                    bodies.append(None)
                else:
                    body = body_info[f][s[b]] if len(bodies) < 2 else None
                    bodies.append(body)
            new_body_info.append(bodies)

        # save results
        new_file = path + name + '/' + name + '.joint'
        write_joint(new_file, new_body_info)
        print('{}/{}: {}'.format(startIndex+cur, startIndex+len(selected_files)-1, name))


if __name__ == '__main__':
    main()
