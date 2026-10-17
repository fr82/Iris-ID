import time
import cv2

from camera import Camera
from iris_detector import IrisDetector
from iris_matcher import IrisMatcher
from userdb import UserDatabase
from ui import Interface

from config import (
    ENROLMENT_SAMPLES,
    SAMPLE_INTERVAL,
    MATCH_THRESHOLD
)


def main():
    camera = Camera()
    detector = IrisDetector()
    matcher = IrisMatcher()
    database = UserDatabase()
    interface = Interface()

    # Check that the camera opened successfully before starting.
    if not camera.is_opened():
        print("Error: Could not open the camera.")
        return

    # Load any users that were registered during previous program runs.
    users = database.load_users()
    message = "Ready"

    mode = None
    enrol_name = None
    collected_samples = []
    last_sample_time = 0

    # Keep the camera program running until the user chooses to quit.
    while True:

        # Read the latest frame from the camera.
        success, frame = camera.read()

        if not success:
            message = "Could not read camera frame."
            continue

        # Detect the iris and extract the eye features from the frame.
        features = detector.detect(frame)

        # If the user is currently enrolling a new person,
        # collect multiple samples of their eyes.
        if mode == "enrol":
            if features is not None:
                current_time = time.time()
                if current_time - last_sample_time >= SAMPLE_INTERVAL:

                    collected_samples.append(features)
                    last_sample_time = current_time

                    message = (
                        f"Capturing sample "
                        f"{len(collected_samples)}/{ENROLMENT_SAMPLES}"
                    )

                    # Once enough samples have been collected, save them to the user database.
                    if len(collected_samples) >= ENROLMENT_SAMPLES:

                        database.save_user(
                            enrol_name,
                            collected_samples
                        )

                        users = database.load_users()
                        message = f"Enrolled: {enrol_name}"

                        mode = None
                        enrol_name = None
                        collected_samples = []

            else:
                message = "Look at the camera to enrol."

        elif mode == "authenticate":
            if features is not None and users:
                best_name, best_score = matcher.find_best_match(
                    features,
                    users
                )

                if best_score >= MATCH_THRESHOLD:
                    message = (
                        f"Recognised: {best_name} "
                        f"({best_score:.2f})"
                    )
                else:
                    message = (
                        f"Not recognised "
                        f"({best_score:.2f})"
                    )

                # Authentication is completed after one comparison.
                mode = None

            elif not users:
                message = "No registered users."
                mode = None

            else:
                message = "Look at the camera to authenticate."

        frame = interface.draw(
            frame,
            message,
            len(users)
        )

        cv2.imshow(
            "Iris Authentication",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Quit the program on q
        if key == ord("q"):
            break

        # Start enrolment.
        elif key == ord("e"):

            name = input("Enter the person's name: ").strip()

            if name:
                enrol_name = name
                collected_samples = []
                mode = "enrol"
                last_sample_time = 0

                message = f"Enrolling {name}..."

        # Start authentication.
        elif key == ord("a"):

            if users:
                mode = "authenticate"
                message = "Look at the camera..."
            else:
                message = "No registered users."

        # List all registered users in the terminal.
        elif key == ord("l"):

            if users:
                print("\nRegistered users:")

                for name in users:
                    print(f"- {name}")

                print()
                message = f"{len(users)} user(s) registered."

            else:
                print("\nNo registered users.\n")
                message = "No registered users."

        # Delete a registered user.
        elif key == ord("d"):

            name = input(
                "Enter the name of the person to delete: "
            ).strip()

            if name in users:

                database.delete_user(name)

                # Reload the database after deleting the user.
                users = database.load_users()

                message = f"Deleted: {name}"

            else:
                message = "User not found."

    # Release the camera and close OpenCV windows before exiting.
    camera.release()


if __name__ == "__main__":
    main()