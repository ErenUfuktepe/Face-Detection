import tkinter as tk
import os
from face_recognation import FaceDetection
import pyautogui


class Menu:
    window = None
    post = None
    detection_object = None
    width, height = pyautogui.size()

    def __init__(self):
        if self.detection_object is None:
            self.detection_object = FaceDetection()
        self.detection_object.initialize()
        self.setup_window(self.initialize_window_size(400, 300))
        self.set_buttons_to_window()

    def setup_window(self, window_size):
        self.window = tk.Tk()
        self.window.title("Face Detection")
        self.window.geometry(window_size)

    def set_buttons_to_window(self):
        app = tk.Frame(self.window)
        app.grid()

        button1 = tk.Button(app, text=" Image ", width=20, command=self.image_selection_window)
        button1.grid(padx=115, pady=30)

        button2 = tk.Button(app, text=" Camera ", width=20, command=self.call_face_detection_from_video)
        button2.grid(padx=115, pady=30)

        button3 = tk.Button(app, text=" Add New Face ", width=20, command=self.add_new_face_window)
        button3.grid(padx=115, pady=30)

        self.window.mainloop()

    def image_selection_window(self):
        self.window.destroy()
        self.setup_window(self.initialize_window_size(380, 150))

        label = tk.Label(self.window, text="Image Name")
        self.post = tk.Entry(self.window, width=35)

        label.grid(row=0, sticky="E", pady=10)
        self.post.grid(row=0, column=1, pady=10)

        submit = tk.Button(self.window, text="Check Images", command=self.check_images, width=20)
        submit.grid(columnspan=2, pady=5)

        back = tk.Button(self.window, text="Back", command=self.back, width=20)
        back.grid(columnspan=2, pady=5)

        self.window.mainloop()

    def add_new_face_window(self):
        self.window.destroy()
        self.setup_window(self.initialize_window_size(360, 150))

        label = tk.Label(self.window, text="Full Name")
        self.post = tk.Entry(self.window, width=34)

        label.grid(row=0, sticky="E", pady=10)
        self.post.grid(row=0, column=1, pady=10)

        submit = tk.Button(self.window, text="Submit", command=self.add_new_face, width=20)
        submit.grid(columnspan=2, pady=5)

        back = tk.Button(self.window, text="Back", command=self.back, width=20)
        back.grid(columnspan=2, pady=5)

        self.window.mainloop()

    def check_images(self):
        path = os.getcwd()
        if not path.__contains__('images'):
            os.chdir('images')
        name = self.post.get()
        self.is_valid_image(name)
        os.chdir('../')

    def is_valid_image(self, image_name):
        path = os.getcwd()
        flag = False
        for filename in os.listdir(path):
            if filename == image_name:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    flag = True
                    path = (os.path.join(os.getcwd(), image_name))
                else:
                    self.pop_message("Error.", "Invalid directory, please write whole path.")
        if not flag:
            self.pop_message("Error.", "Image does not exists.")
        else:
            self.call_face_detection_from_image(path)
            self.__init__()

    def call_face_detection_from_video(self):
        self.window.destroy()
        self.detection_object.face_detection_from_camera()
        self.__init__()

    def call_face_detection_from_image(self, path):
        self.window.destroy()
        self.detection_object.identify_face(path)
        self.__init__()

    def add_new_face(self):
        name = self.post.get()
        self.window.destroy()
        result = self.detection_object.create_dataset(name)
        if result == 1:
            self.pop_message("Success.", "Image have been saved.")
            self.__init__()
        elif result == -1:
            self.pop_message("Fail.", "Could not detect any face try again!")
            self.__init__()
        elif result == 0:
            self.pop_message("Warning.", "We already know you!")
            self.__init__()
        else:
            self.pop_message("Warning.", "Please change the name and try again.")
            self.__init__()

    def pop_message(self, title, message):
        pop_up = tk.Tk()
        pop_up.wm_title(title)
        pop_up.geometry(self.initialize_window_size(300, 100))
        label = tk.Label(pop_up, text=message)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(pop_up, text="Okay", command=pop_up.destroy)
        button.pack()
        pop_up.mainloop()

    def back(self):
        self.window.destroy()
        self.__init__()

    def initialize_window_size(self, width, height):
        width_x = int((self.width / 2) - int(width/2))
        height_x = int((self.height / 2) - int(height/2))
        return str(width) + "x" + str(height) + "+" + str(width_x) + "+" + str(height_x)


Menu()
