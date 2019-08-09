import tkinter as tk
import os
from face_recognation import FaceDetection


class Menu:
    window = None
    post = None
    detection_object = None

    def __init__(self):
        self.setup_window()
        self.main()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title("Face Detection")
        self.window.geometry("400x300")

    def main(self):
        app = tk.Frame(self.window)
        app.grid()

        button1 = tk.Button(app, text=" Image ", width=20, command=self.image_selection)
        button1.grid(padx=110, pady=30)

        button2 = tk.Button(app, text=" Camera ", width=20, command=self.call_face_detection_from_video)
        button2.grid(padx=110, pady=30)

        button3 = tk.Button(app, text=" Add New Face ", width=20, command=self.new_face_name)
        button3.grid(padx=110, pady=30)

        self.window.mainloop()

    def image_selection(self):
        self.window.destroy()
        self.setup_window()

        label = tk.Label(self.window, text="Image Name")
        self.post = tk.Entry(self.window, width=50)

        label.grid(row=0, sticky="E")
        self.post.grid(row=0, column=1)

        submit = tk.Button(self.window, text="Check Images", command=self.check_images)
        submit.grid(columnspan=2)

        self.window.mainloop()

    def new_face_name(self):
        self.window.destroy()
        self.setup_window()

        label = tk.Label(self.window, text="Please Enter Full Name")
        self.post = tk.Entry(self.window, width=50)

        label.grid(row=0, sticky="E")
        self.post.grid(row=0, column=1)

        submit = tk.Button(self.window, text="Submit", command=self.add_new_face)
        submit.grid(columnspan=2)

        self.window.mainloop()

    def check_images(self):
        path = os.getcwd()
        if not path.__contains__('image'):
            os.chdir('images')
        name = self.post.get()
        self.is_valid_image(name)

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

    def call_face_detection_from_video(self):
        self.window.destroy()
        self.detection_object = FaceDetection
        self.detection_object.face_detection_from_camera(FaceDetection)

    def call_face_detection_from_image(self, path):
        self.window.destroy()
        self.detection_object = FaceDetection
        self.detection_object.identify_face(FaceDetection, path)

    def add_new_face(self):
        name = self.post.get()
        self.window.destroy()
        self.detection_object = FaceDetection
        result = self.detection_object.create_dataset(FaceDetection, name)
        if result == 1:
            self.pop_message("Success.", "Image have been saved.")
            os.walk("training_set")
            os.walk("images")
            Menu()

        else:
            self.pop_message("Fail.", "Could not detect any face try again!")
            Menu()

    def pop_message(self, title, message):
        pop_up = tk.Tk()
        pop_up.wm_title(title)
        label = tk.Label(pop_up, text=message)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(pop_up, text="Okay", command=pop_up.destroy)
        button.pack()
        pop_up.mainloop()


Menu()
