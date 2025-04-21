import csv
import os
import numpy as np
from hand_sign_main.model.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from hand_sign_main.model.point_history_classifier.point_history_classifier import PointHistoryClassifier

class GestureService:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'hand_sign_main', 'model', 'keypoint_classifier', 'keypoint_classifier.tflite')
        self.keypoint_classifier = KeyPointClassifier(model_path=model_path)

        point_history_model_path = os.path.join(os.path.dirname(__file__), 'hand_sign_main', 'model', 'point_history_classifier', 'point_history_classifier.tflite')
        self.point_history_classifier = PointHistoryClassifier(model_path=point_history_model_path)

        keypoint_label_path = os.path.join(os.path.dirname(__file__), 'hand_sign_main', 'model', 'keypoint_classifier', 'keypoint_classifier_label.csv')
        point_history_label_path = os.path.join(os.path.dirname(__file__), 'hand_sign_main', 'model', 'point_history_classifier', 'point_history_classifier_label.csv')

        self.keypoint_labels = self.load_labels(keypoint_label_path)
        self.point_history_labels = self.load_labels(point_history_label_path)

    def load_labels(self, file_path):
        with open(file_path, encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            labels = [row[0] for row in reader]
        return labels

    def preprocess_landmarks(self, landmarks):
        base_x, base_y = landmarks[0][0], landmarks[0][1]
        normalized = []
        for x, y in landmarks:
            normalized.append(x - base_x)
            normalized.append(y - base_y)

        max_value = max(list(map(abs, normalized)))
        if max_value != 0:
            normalized = [val / max_value for val in normalized]
        return normalized

    def preprocess_point_history(self, history):
        base_x, base_y = history[0][0], history[0][1]
        normalized = []
        for x, y in history:
            normalized.append(x - base_x)
            normalized.append(y - base_y)

        max_value = max(list(map(abs, normalized)))
        if max_value != 0:
            normalized = [val / max_value for val in normalized]
        return normalized

    def classify_static(self, landmarks):
        processed = self.preprocess_landmarks(landmarks)
        index = self.keypoint_classifier(processed)
        return self.keypoint_labels[index]

    def classify_dynamic(self, point_history):
        processed = self.preprocess_point_history(point_history)
        index = self.point_history_classifier(processed)
        return self.point_history_labels[index]

    def predict_gesture(self, landmarks, point_history=None):
        # Optional: fallback combined method
        if point_history is None:
            return self.classify_static(landmarks)
        else:
            return self.classify_dynamic(point_history)
