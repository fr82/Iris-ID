import cv2
import mediapipe as mp
import numpy as np

from config import FEATURE_SIZE, LEFT_IRIS, RIGHT_IRIS


class IrisDetector:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def _get_eye_crop(self, frame, landmarks, iris_indices):
        height, width = frame.shape[:2]

        points = []

        for index in iris_indices:
            x = int(landmarks[index].x * width)
            y = int(landmarks[index].y * height)

            points.append((x, y))

        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        min_x = max(min(x_values) - 15, 0)
        max_x = min(max(x_values) + 15, width)
        min_y = max(min(y_values) - 15, 0)
        max_y = min(max(y_values) + 15, height)

        eye = frame[min_y:max_y, min_x:max_x]

        # Make sure a valid eye was found before continuing.
        if eye.size == 0:
            return None

        # Convert the eye image to greyscale.
        # This removes colour information that is not needed for the image based iris comparison.
        eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)

        # Resize every eye image to the same dimensions so they can be compared consistently.
        eye = cv2.resize(
            eye,
            (FEATURE_SIZE, FEATURE_SIZE),
            interpolation=cv2.INTER_AREA
        )

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        eye = clahe.apply(eye)

        # Apply a small amount of blur to reduce camera noise.
        eye = cv2.GaussianBlur(eye, (3, 3), 0)

        return eye

    def detect(self, frame):
        # MP expects RGB images rather than OpenCV's default BGR format.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the current camera frame to detect facial landmarks.
        results = self.face_mesh.process(rgb_frame)

        # If no face was detected, there are no iris features to return.
        if not results.multi_face_landmarks:
            return None

        # Use the first detected face's landmarks to locate the irises
        landmarks = results.multi_face_landmarks[0].landmark

        # Extract the left and right eye points.
        left_eye = self._get_eye_crop(
            frame,
            landmarks,
            LEFT_IRIS
        )

        right_eye = self._get_eye_crop(
            frame,
            landmarks,
            RIGHT_IRIS
        )

        # Both eyes are required for authentication.
        if left_eye is None or right_eye is None:
            return None

        # Storing both eyes gives the matcher more information to work with.
        features = np.stack(
            [left_eye, right_eye]
        ).astype(np.uint8)

        return features

    def draw_landmarks(self, frame, results):
        if not results or not results.multi_face_landmarks:
            return frame

        height, width = frame.shape[:2]
        landmarks = results.multi_face_landmarks[0].landmark

        # Draw the points used to locate both irises.
        for iris_indices in [LEFT_IRIS, RIGHT_IRIS]:
            for index in iris_indices:
                x = int(landmarks[index].x * width)
                y = int(landmarks[index].y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    2,
                    (0, 255, 0),
                    -1
                )

        return frame