import cv2


class Interface:
    def draw(self, frame, message, user_count):
        # Display the available keyboard controls at the top of the window.
        cv2.putText(
            frame,
            "E: Enrol  A: Authenticate  L: List  D: Delete  Q: Quit",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Display the current status or instruction underneath the controls.
        cv2.putText(
            frame,
            message,
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Show how many people are currently registered.
        cv2.putText(
            frame,
            f"Registered users: {user_count}",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        return frame