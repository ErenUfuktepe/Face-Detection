import cv2
import face_recognition
from PIL import Image, ImageDraw
import os
import glob


class FaceRecognition:
    known_face_encodings = []
    known_face_names = []

    # Encoding all the faces in training_set folder.
    def initialize(self):
        self.known_face_encodings = self.encoding_face()[1]
        self.known_face_names = self.encoding_face()[0]

    # Encoding faces in order to learn the person.
    def encoding_face(self):
        path = self.change_directory(0)

        face_encodings_list = []
        face_names_list = []

        for filename in os.listdir(path):
            image = face_recognition.load_image_file(filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            face_encodings_list.append(face_encoding)
            name = os.path.splitext(filename)[0]
            face_names_list.append(name)

        self.change_directory(2)
        return [face_names_list, face_encodings_list]

    # Opens a camera and detects faces. If it know the person it will print his/her
    # name in box. Otherwise, it will print unknown person in the box.
    def face_detection_from_camera(self):
        video_cap = cv2.VideoCapture(0)

        if video_cap.isOpened():
            return_val, frame = video_cap.read()
        else:
            return_val = False

        while return_val:

            return_val, frame = video_cap.read()
            rgb_frame = frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                name = "Unknown Person"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    # Finds and identifies the face in given image.
    def identify_face(self, image):
        test_image = face_recognition.load_image_file(image)

        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        pil_image = Image.fromarray(test_image)

        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)

            name = "Unknown Person"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

            draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0))

            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(255, 255, 0),
                           outline=(255, 255, 0))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(0, 0, 0))

        del draw
        pil_image.show()

    # Detect face in given image.
    def face_detection_from_image(self, image_name):
        name = os.path.splitext(image_name)[0]
        check_image = self.is_valid_image(name)
        if check_image[0] == 1:
            self.identify_face(check_image[1])
        self.change_directory(2)
        return check_image

    # Checks file extension type of the image.
    def is_valid_image(self, image_name):
        path = self.change_directory(1)
        for infile in glob.glob(os.path.join(path, image_name+".*")):
            file_extension = os.path.splitext(infile)[1]
            if file_extension == ".png" or file_extension == ".jpeg" or file_extension == ".jpg":
                return [1, image_name + file_extension]
            else:
                return [0, "Invalid file extension!"]
        return [0, "Image does not exists."]

    # Creates new image to learn the person face.
    def create_new_data(self, name):
        self.change_directory(0)
        check_name = self.check_new_data(name)

        if check_name[0] == 0:
            return check_name

        name = check_name[1]
        video_capture = cv2.VideoCapture(0)

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_capture.release()
                cv2.destroyWindow("Video")
                cv2.imwrite(name, frame)
                check_face_detection = self.check_face_location(name)
                if check_face_detection[0] == 0:
                    os.remove(name)
                self.change_directory(2)
                return check_face_detection

    # Checks whether the face found in given image.
    def check_face_location(self, image):
        test_image = face_recognition.load_image_file(image)
        face_locations = face_recognition.face_locations(test_image)
        if len(face_locations) == 1:
            return [1, "Image have been saved."]
        return [0, "Could not detect any face try again!"]

    # Change the directory according to given key number.
    def change_directory(self, key):
        if key == 0:
            os.chdir("./training_set")
        elif key == 1:
            os.chdir("./images")
        else:
            os.chdir("../")
        return os.getcwd()

    # Checks whether it knows the face earlier and controls the file extension type.
    def check_new_data(self, name):
        for names in self.known_face_names:
            if name == names:
                self.change_directory(2)
                return [0, "We already know this face!"]
        if not (name.__contains__(".jpg") or name.__contains__(".jpeg") or name.__contains__(".png") ) \
                and not name.__contains__("."):
            name = name + ".jpg"
            return [1, name]
        elif not (name.__contains__(".jpg") or name.__contains__(".jpeg") or name.__contains__(".png") ) \
                and name.__contains__("."):
            self.change_directory(2)
            return [0, "Invalid file extension type!"]
        return [1, name]
