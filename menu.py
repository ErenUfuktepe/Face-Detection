import tkinter as tk
from face_recognition_and_detection import FaceRecognition
from face_detection import FaceDetection
import pyautogui


class Menu:
    window = None
    post = None
    recognition_object = None
    detection_object = None
    width, height = pyautogui.size()

    # Constructor for creating window.
    def __init__(self):
        if self.recognition_object is None and self.detection_object is None:
            self.recognition_object = FaceRecognition()
            self.detection_object = FaceDetection()
        self.recognition_object.initialize()
        self.create_main_window(self.initialize_window_size(400, 400))
        self.set_main_window_buttons()

    # Create main window.
    def create_main_window(self, window_size):
        self.window = tk.Tk()
        self.window.title("Face Detection")
        self.window.geometry(window_size)

    # Setting main window's buttons.
    def set_main_window_buttons(self):
        app = tk.Frame(self.window)
        app.grid()

        button1 = tk.Button(app, text=" Image ", width=20, command=self.face_detection_from_image)
        button1.grid(padx=115, pady=30)

        button2 = tk.Button(app, text=" Camera ", width=20, command=self.call_face_detection_from_camera)
        button2.grid(padx=115, pady=30)

        button3 = tk.Button(app, text=" Add New Face ", width=20, command=self.add_new_face_window)
        button3.grid(padx=115, pady=30)

        button4 = tk.Button(app, text=" Face Detection ", width=20, command=self.call_face_detection)
        button4.grid(padx=115, pady=30)

        self.window.mainloop()

    # Creates face detection from image window.
    def face_detection_from_image(self):
        self.create_main_window(self.initialize_window_size(380, 150))

        label = tk.Label(self.window, text="Image Name")
        self.post = tk.Entry(self.window, width=35)

        label.grid(row=0, sticky="E", pady=10)
        self.post.grid(row=0, column=1, pady=10)

        submit = tk.Button(self.window, text="Check Images", command=self.call_face_detection_from_image, width=20)
        submit.grid(columnspan=2, pady=5)

        back = tk.Button(self.window, text="Back", command=self.back, width=20)
        back.grid(columnspan=2, pady=5)

        self.window.mainloop()

    # Window for adding new face.
    def add_new_face_window(self):
        self.create_main_window(self.initialize_window_size(360, 150))

        label = tk.Label(self.window, text="Full Name")
        self.post = tk.Entry(self.window, width=34)

        label.grid(row=0, sticky="E", pady=10)
        self.post.grid(row=0, column=1, pady=10)

        submit = tk.Button(self.window, text="Submit", command=self.call_create_dataset, width=20)
        submit.grid(columnspan=2, pady=5)

        back = tk.Button(self.window, text="Back", command=self.back, width=20)
        back.grid(columnspan=2, pady=5)

        self.window.mainloop()

    # Camera button action. Calls the method for opening the video cam and finds the people face.
    def call_face_detection_from_camera(self):
        self.recognition_object.face_detection_from_camera()

    # Image button action. Calls the method for face detection from image.
    def call_face_detection_from_image(self):
        name = self.post.get()
        self.window.destroy()
        is_success = self.recognition_object.face_detection_from_image(name)
        if is_success[0] == 0:
            self.popup_message("Error", is_success[1])
            self.face_detection_from_image()

    # Add New Face button action.. Calls the method for adding new data.
    def call_create_dataset(self):
        person_name = self.post.get()
        self.window.destroy()
        is_success = self.recognition_object.create_new_data(person_name)
        if is_success[0] == 0:
            self.popup_message("Error", is_success[1])
        else:
            self.popup_message("Success", is_success[1])

    # Creating dynamic popup with title and message.
    def popup_message(self, title, message):
        popup = tk.Tk()
        popup.wm_title(title)
        popup.geometry(self.initialize_window_size(300, 100))
        label = tk.Label(popup, text=message)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="Okay", command=popup.destroy)
        button.pack()
        popup.mainloop()

    # Back button action.
    def back(self):
        self.window.destroy()
        self.__init__()

    # Initialize the window size.
    def initialize_window_size(self, width, height):
        width_x = int((self.width / 2) - int(width/2))
        height_x = int((self.height / 2) - int(height/2))
        return str(width) + "x" + str(height) + "+" + str(width_x) + "+" + str(height_x)

    # Calls the face, eye, and smile detection using haarcascade.
    def call_face_detection(self):
        self.detection_object.main(0)


Menu()
