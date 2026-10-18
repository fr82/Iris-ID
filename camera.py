import cv2
from config import CAMERA_INDEX

# point
class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(CAMERA_INDEX)

    def is_opened(self):
        # Check whether the camera was successfully opened.
        if self.camera.isOpened() == True:
            return True
        else:
            return False

    def read(self):
        success, frame = self.camera.read()

        if not success:
            return False, None

        # Flip the frame horizontally so the camera behaves like a mirror.
        frame = cv2.flip(frame, 1)

        return True, frame

    def release(self):
        # Release the camera so other programs can use it afterwards.
        self.camera.release()
        cv2.destroyAllWindows()
