import cv2


class FaceDetection:

    # Loading the cascades
    # For more features you can check https://github.com/opencv/opencv/tree/master/data/haarcascades
    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_smile.xml')

    # Face detection
    def face_detection(self, gray, frame):
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (face_x, face_y, face_width, face_height) in faces:
            cv2.rectangle(frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (255, 0, 0), 2)
            gray_image = gray[face_y:face_y + face_height, face_x:face_x + face_width]
            original_image = frame[face_y:face_y + face_height, face_x:face_x + face_width]
            self.eye_detection(gray_image, original_image)
            self.smile_detection(gray_image, original_image)
        return frame

    # Eye Detection
    def eye_detection(self, gray, frame):
        eyes = self.eye_cascade.detectMultiScale(gray, 1.1, 20)
        for (eye_x, eye_y, eye_width, eye_height) in eyes:
            cv2.rectangle(frame, (eye_x, eye_y), (eye_x + eye_width, eye_y + eye_height), (0, 255, 0), 2)

    # Smile Detection
    def smile_detection(self, gray, frame):
        smile = self.smile_cascade.detectMultiScale(gray, 1.7, 22)
        for (smile_x, smile_y, smile_width, smile_height) in smile:
            cv2.rectangle(frame, (smile_x, smile_y), (smile_x + smile_width, smile_y + smile_height), (0, 0, 255), 2)

    # Start detection
    # cam_option 0 for laptop cam and 1 for external cam
    def main(self, cam_option):
        video_capture = cv2.VideoCapture(cam_option)
        while True:
            _, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            canvas = self.face_detection(gray, frame)
            cv2.imshow('Video', canvas)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()
