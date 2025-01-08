import threading

import cv2
from deepface import DeepFace
from UserManager import *

class FaceDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.manager = UserManager()
        self.user_list = self.manager.get_users()

        self.counter = 0
        self.face_match = False
        self.current_user = None

    def check_face(self, frame):
        try:
            for user in self.user_list:
                if DeepFace.verify(frame, user.image.copy())['verified']:
                    self.face_match = True
                    self.current_user = user
                else:
                    self.face_match = False
        except ValueError:
            self.face_match = False


    def run_face_detection(self):

        while True:
            ret, frame = self.cap.read()

            if ret:
                if self.counter % 30 == 0:
                    try:
                        threading.Thread(target=self.check_face, args=(frame.copy(),)).start()
                    except ValueError:
                        pass
                self.counter += 1
                if self.face_match:
                    cv2.putText(frame, f"Hi {self.current_user.username}!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                else:
                    cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

                cv2.imshow('video', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cv2.destroyAllWindows()



if __name__ == '__main__':
    face_detection = FaceDetection()
    face_detection.run_face_detection()

