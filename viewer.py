from PIL import Image, ImageTk
from tkinter import ttk, filedialog
import tkinter as tk
import os
import cv2
import numpy as np

import dataloader
import constants

__author__ = "Woo-Ri Ko"

############
# *Command*
# <space-bar>: start or pause,
# <r>or<R>: activate or deactivate robot view,
# <h>or<H>: activate or deactivate human view
# <Enter>or<Double-click>: open video file
############


def main():
    viewer = AIRViewer()
    viewer.root.mainloop()


class AIRViewer:
    def __init__(self):
        # ========== main window ========== #
        self.root = tk.Tk()
        self.root.geometry("1150x500+100+100")
        self.root.title('AIR-Act2Act Viewer')

        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=8)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1)

        self.root.bind("<space>", lambda e: self.click_play_button())
        self.root.bind("<r>", lambda e: self.toggle_view(var=self.is_drawn[0]))
        self.root.bind("<R>", lambda e: self.toggle_view(var=self.is_drawn[0]))
        self.root.bind("<h>", lambda e: self.toggle_view(var=self.is_drawn[1]))
        self.root.bind("<H>", lambda e: self.toggle_view(var=self.is_drawn[1]))

        directory_frame = tk.Frame(self.root)
        directory_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        video_frame = tk.Frame(self.root)
        video_frame.grid(row=0, column=1, sticky='nsew')
        control_frame = tk.Frame(self.root, bg="white", height=100)
        control_frame.grid(row=1, column=1, sticky='nsew')

        # ========== variables ========== #
        self.speed = 1  # ms per frame
        self.play = False
        self.frame_count = 0
        self.cur_frame = tk.IntVar(value=0)
        self.is_drawn = [tk.BooleanVar(value=True), tk.BooleanVar(value=True)]  # [robot, human]

        self.depth_path = ""
        self.body_path = ""
        self.joint_path = ""
        self.joint_org = list()
        self.joint_ref = list()

        # ========== menu bar ========== #
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="Open directory", command=self.open_directory)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        view_menu = tk.Menu(self.menu_bar, tearoff=False)
        view_menu.add_checkbutton(label="Robot", variable=self.is_drawn[0], onvalue=True, offvalue=False,
                                  command=self.update_video)
        view_menu.add_checkbutton(label="Human", variable=self.is_drawn[1], onvalue=True, offvalue=False,
                                  command=self.update_video)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=self.menu_bar)

        # ========== directory box ========== #
        tree_frame = tk.Frame(directory_frame, bg='white', padx=1, pady=1)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.tree = ttk.Treeview(tree_frame)
        self.tree.heading('#0', text='Video List', anchor='w')
        xsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        ysb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(xscroll=xsb.set, yscroll=ysb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        xsb.grid(row=1, column=0, sticky='nsew')
        ysb.grid(row=0, column=1, sticky='nsew')

        self.tree.bind("<Double-Button-1>", self.click_tree)
        self.tree.bind("<Return>", self.click_tree)
        self.child = None

        # ========== video player ========== #
        notebook1 = ttk.Notebook(video_frame)
        notebook1.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.label_depth1 = tk.Label(notebook1, bd=0, highlightthickness=0, relief='flat', bg='white')
        self.label_depth1.pack(fill='both', expand='yes')
        self.label_depth1.bind('<Configure>', lambda e: self.update_video())
        notebook1.add(self.label_depth1, text='Refined')

        notebook2 = ttk.Notebook(video_frame)
        notebook2.place(relx=.5, rely=0, relwidth=0.5, relheight=1)
        self.label_depth2 = tk.Label(notebook2, bd=0, highlightthickness=0, relief='flat', bg='white')
        self.label_depth2.pack(fill='both', expand='yes')
        notebook2.add(self.label_depth2, text='Original')

        # ========== controller ========== #
        control_frame.columnconfigure(0)
        control_frame.columnconfigure(1, weight=1)

        button_frame = tk.Frame(control_frame, bg='white', width=70)
        button_frame.grid(row=0, column=0, sticky='nsew')
        bar_frame = tk.Frame(control_frame, bg='white')
        bar_frame.grid(row=0, column=1, sticky='nsew')

        self.photo_play = tk.PhotoImage(file="image/play.png")
        self.photo_stop = tk.PhotoImage(file="image/stop.png")
        self.button = tk.Button(button_frame, command=self.click_play_button, image=self.photo_play,
                                relief='solid', padx=10, pady=10)
        self.button.pack(fill='x', padx=10, pady=10)

        self.track_bar = tk.Scale(bar_frame, variable=self.cur_frame, showvalue=True,
                                  from_=0, to=self.frame_count-1, orient='horizontal')
        self.track_bar.pack(fill='x', padx=2, pady=10)
        self.track_bar.bind("<B1-Motion>", lambda e: self.drag_track_bar())

        # update videos
        self.video_loop()

    # open directory explorer
    def open_directory(self):
        # 'cancel' button is clicked
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        self.tree.delete(*self.tree.get_children())
        # 'select' button is clicked
        for data_name in os.listdir(folder_path):
            abspath = folder_path + "/" + data_name
            if all(c in data_name for c in ['C', 'P', 'A', 'S']):
                self.tree.insert('', 'end', text=data_name, values=str(abspath), open=False)

    # select item in tree
    def click_tree(self, _):
        # set paths of depth and body data
        path = ' '.join(self.tree.item(self.tree.selection())['values'])
        data_name = path.split('/')[-1]
        self.depth_path = path + '/' + data_name + '_depth/'
        self.body_path = path + '/' + data_name + '_body/'

        # load joint data in advance
        joint_org_path = path + '/' + data_name + '.~joint'
        if os.path.isfile(joint_org_path):
            self.joint_org = dataloader.read_joint(joint_org_path)
        joint_ref_path = path + '/' + data_name + '.joint'
        if os.path.isfile(joint_ref_path):
            self.joint_ref = dataloader.read_joint(joint_ref_path)

        # change track bar status
        self.track_bar.set(0)
        self.cur_frame.set(0)
        self.update_video()
        self.track_bar["to"] = self.frame_count - 1

    # limit track bar value
    def drag_track_bar(self):
        old = self.cur_frame.get()
        new = max(min(old, self.frame_count - 1), 0)
        self.cur_frame.set(new)
        self.update_video()

    # draw depth map, body indexes, skeletons
    def update_video(self):
        if not os.path.isdir(self.depth_path):
            return
        # depth map
        cur_frame = self.cur_frame.get()
        depth = dataloader.read_depth_map(self.depth_path, cur_frame)
        self.frame_count = dataloader.count_files(self.depth_path)
        depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
        # body index
        body = dataloader.read_body(self.body_path, cur_frame)
        if body is not None:
            self.draw_bodies(depth, body_map=body)
        # skeleton
        depth_org = np.array(depth)
        if self.joint_org is not None:
            self.draw_joints(depth_org, self.joint_org[cur_frame])
        depth_ref = np.array(depth)
        if self.joint_ref is not None:
            self.draw_joints(depth_ref, self.joint_ref[cur_frame])
        # draw
        self.show_image(depth_org, self.label_depth2)
        self.show_image(depth_ref, self.label_depth1)

    @staticmethod
    def draw_bodies(image, body_map):
        for index in range(len(constants.BODY_COLORS)):
            image[body_map == index] = constants.BODY_COLORS[index]

    # draw joints on image
    def draw_joints(self, image, joints):
        for b in range(constants.BODY_COUNT):
            if joints[b] is None:
                continue
            if joints[b]["type"] == 'refined' and not self.is_drawn[b].get():
                continue
            for j in range(constants.JOINT_COUNT):
                k = constants.CONNECTING_JOINTS[j]
                vector_j = (int(joints[b]["joints"][j]["depthX"]), int(joints[b]["joints"][j]["depthY"]))
                vector_k = (int(joints[b]["joints"][k]["depthX"]), int(joints[b]["joints"][k]["depthY"]))
                cv2.line(image, vector_j, vector_k, constants.LINE_COLORS[b], 2)
                cv2.circle(image, vector_j, 4, constants.JOINT_COLORS[j], -1)

    def show_image(self, image, label):
        # resize image
        h_image, w_image, _ = image.shape
        w_frame = label.winfo_width()
        h_frame = label.winfo_height()
        new_size = self.cal_size(w_image=w_image, h_image=h_image, w_frame=w_frame, h_frame=h_frame)
        image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

        # display on window
        photo = ImageTk.PhotoImage(Image.fromarray(image))
        label.configure(image=photo)
        label.image = photo

    @staticmethod
    def cal_size(w_image, h_image, w_frame, h_frame):
        ratio_image = w_image / h_image
        ratio_frame = w_frame / h_frame
        if ratio_image > ratio_frame:
            ratio = w_frame / w_image
        else:
            ratio = h_frame / h_image
        return tuple((int(w_image * ratio), int(h_image * ratio)))

    def click_play_button(self):
        photo = self.photo_play if self.play else self.photo_stop
        self.button.config(image=photo)
        self.play = not self.play
        if self.play and self.track_bar.get() == self.frame_count - 1:
            self.track_bar.set(0)

    def video_loop(self):
        # if self.track_bar.get() == self.frame_count - 1:
        #     self.play = False
        #     self.button.config(image=self.photo_play)
        if self.play:
            self.track_bar.set(self.track_bar.get() + 1)
            self.update_video()
        self.root.after(self.speed, self.video_loop)

    # draw/remove skeletons on videos
    def toggle_view(self, var):
        var.set(not var.get())
        self.update_video()


if __name__ == '__main__':
    main()
