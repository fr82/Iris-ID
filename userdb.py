import hashlib
import os
import numpy as np

from config import TEMPLATES_DIR


class UserDatabase:
    def __init__(self):
        os.makedirs(TEMPLATES_DIR, exist_ok=True)

    def _get_filename(self, name):
        user_hash = hashlib.sha256(
            name.encode("utf-8")
        ).hexdigest()

        return os.path.join(
            TEMPLATES_DIR,
            user_hash + ".npz"
        )

    def save_user(self, name, samples):
        # Create the filename associated with the person's name.
        filename = self._get_filename(name)

        # Store the person's name and all of their eye samples.
        np.savez_compressed(
            filename,
            name=name,
            samples=np.array(samples, dtype=np.uint8)
        )

    def load_users(self):
        # Dictionary containing all registered users and their samples.
        users = {}

        # Look through every stored template file.
        for filename in os.listdir(TEMPLATES_DIR):

            if not filename.endswith(".npz"):
                continue

            filepath = os.path.join(
                TEMPLATES_DIR,
                filename
            )

            try:
                # Load the saved person's name and eye samples.
                data = np.load(
                    filepath,
                    allow_pickle=False
                )

                name = str(data["name"])
                samples = data["samples"]

                users[name] = samples

            except Exception:
                # Ignore damaged or invalid template files rather than stopping the entire program.
                continue

        return users

    def delete_user(self, name):
        filename = self._get_filename(name)

        if os.path.exists(filename):
            os.remove(filename)
            return True

        return False