import os
import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFont
import face_recognition


# Face recognition with video using face_recognition lib.
def face_recognition_with_camera():
    global df
    window_name = 'Camera'
    video_cap = cv2.VideoCapture(0)

    while video_cap.isOpened():
        _, frame = video_cap.read()
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            encoding_list = df['encoding'].to_list()
            matches = face_recognition.compare_faces(encoding_list, face_encoding)

            name = UNKNOWN
            if True in matches:
                name = df['name'].iloc[matches.index(True)]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow(window_name, frame)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    video_cap.release()
    cv2.destroyAllWindows()


# Select image from local computer.
def select_file():
    global df

    filetypes = (
        ('Image file', '*.jpg'),
        ('Image file', '*.jpeg'),
        ('Image file', '*.png')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    return filename


# Face recognition with image using face_recognition lib.
def face_recognition_with_image():
    filename = select_file()
    image = face_recognition.load_image_file(filename)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        encoding_list = df['encoding'].to_list()
        matches = face_recognition.compare_faces(encoding_list, face_encoding, tolerance=0.5)

        name = UNKNOWN
        if True in matches:
            name = df['name'].iloc[matches.index(True)]

        draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0))
        font = ImageFont.truetype("arial.ttf", 36)
        _, top, _, _ = draw.textbbox((0, 0), name, font=font)
        draw.rectangle(((left, bottom - top - 10), (right, bottom)), fill=(255, 255, 0),
                       outline=(255, 255, 0))
        draw.text((left + 6, bottom - top - 5), name, fill=(0, 0, 0))
    del draw
    pil_image.show()


# Check if the file type is supported
def is_allowed(file):
    global ALLOWED_FILE_TYPES
    array = file.split('.')
    extension = array[len(array) - 1].lower()
    return any(list(map(lambda file_type: extension == file_type.lower(), ALLOWED_FILE_TYPES)))


# Add new encoding
def learn_new_face():
    global df
    filename = select_file()
    name = filename.split('/')[-1]
    image = face_recognition.load_image_file(filename)
    data = {
        'name': name.split('.')[0],
        'filename': name,
        'encoding': face_recognition.face_encodings(image)[0]
    }
    df.loc[len(df)] = data
    df.to_parquet(os.path.join(PATH, TRAINED), index=True)


# Load previous encodings
def load_faces():
    global PATH, TRAINED, DELETE_IMAGE_AFTER_SAVE, df

    df_directory = os.path.join(PATH, TRAINED)
    for filename in os.listdir(PATH):
        image_directory = os.path.join(PATH, filename)
        if is_allowed(filename):
            image = face_recognition.load_image_file(image_directory)
            person_name = filename.split('.')[0]
            if not df[df['name'] == person_name].shape[0] > 0:
                data = {
                    'name': person_name,
                    'filename': filename,
                    'encoding': face_recognition.face_encodings(image)[0]
                }
                df.loc[len(df)] = data
            if DELETE_IMAGE_AFTER_SAVE:
                os.remove(image_directory)
    # Update the file if there are new faces in data folder
    df.to_parquet(df_directory, index=True)
    df = pd.read_parquet(df_directory)


# Face detection with haarcascade
def face_detection_with_haarcascade():
    window_name = 'Camera'
    video_cap = cv2.VideoCapture(0)

    while True:
        _, frame = video_cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        for (face_x, face_y, face_width, face_height) in faces:
            cv2.rectangle(frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (255, 0, 0), 2)
            gray_image = gray[face_y:face_y + face_height, face_x:face_x + face_width]
            original_image = frame[face_y:face_y + face_height, face_x:face_x + face_width]
            eye_detection_with_haarcascade(gray_image, original_image)
            smile_detection_with_haarcascade(gray_image, original_image)
        cv2.imshow(window_name, frame)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    video_cap.release()
    cv2.destroyAllWindows()


# Eye Detection with haarcascade
def eye_detection_with_haarcascade(gray, frame):
    eyes = eye_classifier.detectMultiScale(gray, 1.1, 20)
    for (eye_x, eye_y, eye_width, eye_height) in eyes:
        cv2.rectangle(frame, (eye_x, eye_y), (eye_x + eye_width, eye_y + eye_height), (0, 255, 0), 2)


# Smile Detection with haarcascade
def smile_detection_with_haarcascade(gray, frame):
    smile = smile_classifier.detectMultiScale(gray, 1.7, 22)
    for (smile_x, smile_y, smile_width, smile_height) in smile:
        cv2.rectangle(frame, (smile_x, smile_y), (smile_x + smile_width, smile_y + smile_height), (0, 0, 255), 2)


# Dataset location
PATH = os.path.join(os.getcwd(), 'data')
TRAINED = 'trained.parquet'

# Create dataframe to encodings
df = pd.DataFrame(columns=['name', 'filename', 'encoding'])

# Constants
UNKNOWN = 'Unknown Person'
ALLOWED_FILE_TYPES = ['jpeg', 'png', 'jpg']
DELETE_IMAGE_AFTER_SAVE = True # Delete the image after we add the image to parquet file

# Main frame size
WIDTH = 250
HEIGHT = 200

# https://github.com/opencv/opencv/tree/master/data/haarcascades
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

smile_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

load_faces()

window = tk.Tk()

ws = window.winfo_screenwidth()  # width of the screen
hs = window.winfo_screenheight()  # height of the screen

# Setting the window to open in the middle of the screen
x = int((ws / 2) - int(WIDTH / 2))
y = int((hs / 2) - int(HEIGHT / 2))

camera_button = tk.Button(window, text="Camera", width=20, command=face_recognition_with_camera)
camera_button.place(x=55, y=30)

detect_from_image_button = tk.Button(window, text="Detect Faces From Image", width=20, command=face_recognition_with_image)
detect_from_image_button.place(x=55, y=60)

add_new_face_button = tk.Button(window, text="Learn New Face", width=20, command=learn_new_face)
add_new_face_button.place(x=55, y=90)

smile_detection_button = tk.Button(window, text="Smile Detection", width=20, command=face_detection_with_haarcascade)
smile_detection_button.place(x=55, y=120)

window.title("Face Detection")
window.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
window.attributes('-topmost', 'true')  # keep it on top

window.mainloop()
