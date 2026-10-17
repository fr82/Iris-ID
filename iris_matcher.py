import cv2
import numpy as np


class IrisMatcher:
    def compare_eye(self, eye1, eye2):
        image1 = eye1.astype(np.float32) / 255.0
        image2 = eye2.astype(np.float32) / 255.0

        best_score = -1.0

        for shift_x in range(-3, 4):
            for shift_y in range(-3, 4):

                # Create a translated version of the second eye image.
                matrix = np.float32([
                    [1, 0, shift_x],
                    [0, 1, shift_y]
                ])

                shifted = cv2.warpAffine(
                    image2,
                    matrix,
                    (image2.shape[1], image2.shape[0]),
                    borderMode=cv2.BORDER_REFLECT
                )

                # Compare the two images.
                result = cv2.matchTemplate(
                    image1,
                    shifted,
                    cv2.TM_CCOEFF_NORMED
                )

                score = float(result[0][0])

                # Keep the best result from all tested positions.
                if score > best_score:
                    best_score = score

        return best_score

    def compare_features(self, features1, features2):
        # Compare the left eye and right eye separately.
        left_score = self.compare_eye(
            features1[0],
            features2[0]
        )

        right_score = self.compare_eye(
            features1[1],
            features2[1]
        )

        # Give both eyes equal importance when calculating the final score.
        return (left_score + right_score) / 2.0

    def find_best_match(self, features, users):
        # Keep track of the highest similarity score found.
        best_name = None
        best_score = -1.0

        for name, stored_samples in users.items():

            # Each person has multiple enrolment samples.
            for stored_features in stored_samples:
                score = self.compare_features(
                    features,
                    stored_features
                )

                # Update the best match whenever a higher score is found.
                if score > best_score:
                    best_score = score
                    best_name = name

        return best_name, best_score