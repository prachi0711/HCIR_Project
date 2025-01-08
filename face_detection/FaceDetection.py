import threading

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
        self.facial_areas_dict = None

    def check_face(self, frame):
        try:
            for user in self.user_list:
                deepface_verification_result = DeepFace.verify(frame, user.image.copy())

                if deepface_verification_result['verified']:
                    self.face_match = True
                    self.current_user = user
                    self.facial_areas_dict = deepface_verification_result['facial_areas']
                    break
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

                    cv2.putText(frame, f"Hi {self.current_user.username}!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    if self.facial_areas_dict is not None:
                        facial_areas = self.facial_areas_dict['img1']
                        cv2.rectangle(frame, (facial_areas['x'], facial_areas['y']),
                                      (facial_areas['x'] + facial_areas['w'], facial_areas['y'] + facial_areas['h']),
                                      (0, 0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Unauthorized User!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

                cv2.imshow('video', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cv2.destroyAllWindows()



if __name__ == '__main__':
    face_detection = FaceDetection()
    face_detection.run_face_detection()

