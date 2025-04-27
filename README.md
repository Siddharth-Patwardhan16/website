# Hand Gesture Recognition with MediaPipe

This project is a hand gesture recognition system built using Python 3.11.9 and MediaPipe. It includes a web interface and backend services for recognizing hand gestures and performing related tasks.

## Prerequisites

- Python 3.11.9
- Install the required dependencies by running:

```bash
pip install -r requirement.txt
```

## Project Structure

### Main Directories and Files

#### `hand_sign_web/`

- **`app.py`**: The main entry point for the web application. It uses Flask to serve the web interface.
- **`gesture_service.py`**: Contains the backend logic for gesture recognition.
- **`requirement.txt`**: Lists all the Python dependencies required for the project.
- **`users.json`**: Stores user data for the application.

#### `hand_sign_main/`

- **`api.py`**: Provides API endpoints for gesture recognition services.
- **`keypoint_classification_EN.ipynb`**: Jupyter Notebook for training and testing the keypoint classification model (English version).
- **`keypoint_classification.ipynb`**: Jupyter Notebook for training and testing the keypoint classification model.
- **`point_history_classification.ipynb`**: Jupyter Notebook for training and testing the point history classification model.
- **`run_recognition.py`**: Script to run the gesture recognition system.

#### `hand_sign_main/model/`

- **`keypoint_classifier/`**: Contains files related to the keypoint classification model, including:
  - `keypoint_classifier.py`: The Python script for the keypoint classifier.
  - `keypoint_classifier.tflite`: The TensorFlow Lite model for keypoint classification.
  - `keypoint_classifier_label.csv`: Labels for the keypoint classifier.
- **`point_history_classifier/`**: Contains files related to the point history classification model, including:
  - `point_history_classifier.py`: The Python script for the point history classifier.
  - `point_history_classifier.tflite`: The TensorFlow Lite model for point history classification.
  - `point_history_classifier_label.csv`: Labels for the point history classifier.

#### `hand_sign_main/utils/`

- **`cvfpscalc.py`**: Utility for calculating frames per second (FPS) for the recognition system.

#### `static/` and `templates/`

- **`static/`**: Contains CSS files for styling the web interface.
- **`templates/`**: Contains HTML templates for the web interface.

## How to Start

1. **Set up the environment**:

   - Ensure Python 3.11.9 is installed.
   - Install dependencies using `pip install -r requirement.txt`.

2. **Run the Web Application**:

   - Navigate to the `hand_sign_web/` directory.
   - Start the Flask application by running:

   ```bash
   python app.py
   ```

   The application will be available at `http://127.0.0.1:5000/`.

3. **Run Gesture Recognition**:

   - Navigate to the `hand_sign_main/` directory.
   - Execute the recognition script by running:

   ```bash
   python run_recognition.py
   ```

## Notes

- The project uses TensorFlow Lite models for gesture recognition.
- Jupyter Notebooks are provided for training and testing the models.
- The web interface is built using Flask and styled with CSS.

Feel free to explore the code and customize it as needed!
