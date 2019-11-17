import cv2
import face_recognition
from PIL import Image, ImageDraw
import os


class FaceDetection:
    known_face_encodings = []
    known_face_names = []

    def initialize(self):
        self.known_face_encodings = self.encoding_face()[1]
        self.known_face_names = self.encoding_face()[0]

    def face_detection_from_camera(self):
        video_cap = cv2.VideoCapture(0)

        if not os.getcwd().__contains__("images"):
            os.chdir("images")

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

    def encoding_face(self):
        path = os.getcwd()
        if not path.__contains__('training_set'):
            if not path.__contains__('images'):
                os.chdir("images")
            os.chdir("training_set")
            path = os.getcwd()

        face_encodings_list = []
        face_names_list = []

        for filename in os.listdir(path):
            image = face_recognition.load_image_file(filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            face_encodings_list.append(face_encoding)
            name = filename.replace('.jpg', '')
            name = name.replace('.png', '')
            name = name.replace('.jpeg', '')
            face_names_list.append(name)

        return [face_names_list, face_encodings_list]

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

    def create_dataset(self, filename):
        if not os.getcwd().__contains__("training_set"):
            os.chdir("./images/training_set")

        if not filename.__contains__(".jpg") or filename.__contains__(".jpeg") or filename.__contains__(".png"):
            filename = filename + ".jpg"

        video_capture = cv2.VideoCapture(0)

        while video_capture.isOpened():
            ret, frame = video_capture.read()

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_capture.release()
                cv2.destroyWindow("Video")
                cv2.imwrite(filename, frame)
                return self.face_detection_check(filename)
                break

    def face_detection_check(self, image_name):
        image = face_recognition.load_image_file(image_name)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) == 1:
            return 1
        else:
            os.remove(image_name)
            return 0
