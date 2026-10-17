# Iris-ID 👁️

A Python-based iris authentication prototype that uses computer vision to detect eye regions, register users and attempt to recognise them using stored eye-image samples.

## Features

- **Eye detection:** Uses OpenCV and MediaPipe to locate iris landmarks.
- **User enrolment:** Registers users under their chosen names by collecting multiple eye samples.
- **Persistent storage:** Saves registered templates locally so they can be loaded between sessions.
- **Authentication:** Compares live eye images against stored samples to find the closest match.
- **Image preprocessing:** Uses greyscale conversion, contrast enhancement and Gaussian blur to improve image consistency.
- **User interface:** Displays a live camera feed and provides keyboard controls for the main functions.
- **Modular architecture:** Separates camera handling, iris detection, image matching, data storage and interface logic into individual Python modules.

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- Git and GitHub

## Project Structure

```text
Iris-ID/
├── main.py              # Main application and program flow
├── camera.py            # Camera initialisation and frame capture
├── config.py            # Configuration settings
├── iris_detector.py     # Eye-region detection and preprocessing
├── iris_matcher.py      # Image similarity comparison
├── ui.py                # Camera interface and status messages
├── userdb.py             # User template storage and retrieval
├── README.md
└── iris_templates/      # Locally stored user templates
```

The `iris_templates/` directory is generated or populated locally and should not be committed to a public repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/fr82/Iris-ID.git
cd Iris-ID
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install opencv-python numpy mediapipe==0.10.21
```

The pinned MediaPipe version is intended for compatibility with the legacy `mp.solutions` API used by this project.

### 4. Run the application

```bash
python main.py
```

Allow camera access if your operating system requests permission.

## Controls

| Key | Function |
|---|---|
| `E` | Enrol a new user |
| `A` | Attempt authentication |
| `L` | List registered users |
| `D` | Delete a registered user |
| `Q` | Quit the application |

During enrolment, follow the terminal prompt to enter a name and look towards the camera while the application collects eye samples.

## How It Works

1. **Capture:** OpenCV captures frames from the webcam.
2. **Detect:** MediaPipe identifies facial landmarks, including landmarks around the irises.
3. **Preprocess:** The detected eye regions are resized and processed to make image comparisons more consistent.
4. **Enrol:** Multiple eye-image samples are stored against the user's name.
5. **Match:** The application compares new eye images with stored samples using normalised image correlation and small positional shifts.
6. **Decide:** The best similarity score is compared against a configurable threshold to determine whether a match is accepted.

## Configuration

The `config.py` file contains settings such as:

- `CAMERA_INDEX` — selects the camera device.
- `FEATURE_SIZE` — sets the dimensions of the processed eye images.
- `ENROLMENT_SAMPLES` — controls how many samples are collected per enrolment.
- `SAMPLE_INTERVAL` — sets the delay between samples.
- `MATCH_THRESHOLD` — sets the minimum similarity score required for a match.

These values can be adjusted to experiment with the system's behaviour.

## Limitations and Security

This project is an experimental computer-vision prototype, not a production-ready biometric authentication system.

- Image similarity is sensitive to lighting, focus, eye position and camera quality.
- The matching method is not a validated iris-recognition algorithm.
- The system may incorrectly accept or reject a match.
- The prototype does not implement reliable liveness detection, so it should not be assumed to resist photographs, video replays or other spoofing attempts.
- Stored templates contain biometric image data and must be protected appropriately.

**Do not use this prototype to protect sensitive accounts, financial information or other high-value resources.** For real authentication, a validated biometric implementation and appropriate security controls would be required.

## Future Improvements

- Implement more robust iris segmentation and feature encoding.
- Improve matching accuracy under different lighting conditions.
- Add liveness detection and spoofing resistance.
- Introduce automated tests and performance evaluation.
- Improve enrolment feedback and error handling.
- Add secure storage and stronger access controls.

## Disclaimer

Iris ID was developed as a learning project to explore Python, computer vision, image processing and biometric authentication concepts. It is not intended for real security use.
