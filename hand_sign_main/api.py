# from flask import Flask, request, jsonify, Response
# import cv2 as cv
# import numpy as np
# import mediapipe as mp
# from collections import deque, Counter
# import copy
# import csv
# import itertools

# from utils import CvFpsCalc
# from model import KeyPointClassifier, PointHistoryClassifier

# app = Flask(__name__)

# # Initialize models and variables
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
# keypoint_classifier = KeyPointClassifier()
# point_history_classifier = PointHistoryClassifier()

# with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
#     keypoint_classifier_labels = [row[0] for row in csv.reader(f)]
# with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
#     point_history_classifier_labels = [row[0] for row in csv.reader(f)]

# history_length = 16
# point_history = deque(maxlen=history_length)
# finger_gesture_history = deque(maxlen=history_length)

# @app.route('/')
# def index():
#     return "Hand Gesture Recognition API"

# @app.route('/recognize', methods=['POST'])
# def recognize():
#     file = request.files['image']
#     image = cv.imdecode(np.fromstring(file.read(), np.uint8), cv.IMREAD_COLOR)
#     image = cv.flip(image, 1)
#     debug_image = copy.deepcopy(image)

#     image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#     image.flags.writeable = False
#     results = hands.process(image)
#     image.flags.writeable = True

#     response = {
#         "hand_sign": "",
#         "finger_gesture": ""
#     }

#     if results.multi_hand_landmarks is not None:
#         for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
#             landmark_list = calc_landmark_list(debug_image, hand_landmarks)
#             pre_processed_landmark_list = pre_process_landmark(landmark_list)
#             pre_processed_point_history_list = pre_process_point_history(debug_image, point_history)

#             hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
#             if hand_sign_id == 2:
#                 point_history.append(landmark_list[8])
#             else:
#                 point_history.append([0, 0])

#             finger_gesture_id = 0
#             if len(pre_processed_point_history_list) == (history_length * 2):
#                 finger_gesture_id = point_history_classifier(pre_processed_point_history_list)

#             finger_gesture_history.append(finger_gesture_id)
#             most_common_fg_id = Counter(finger_gesture_history).most_common()

#             if 0 <= hand_sign_id < len(keypoint_classifier_labels):
#                 response["hand_sign"] = keypoint_classifier_labels[hand_sign_id]
#             else:
#                 response["hand_sign"] = "Unknown"

#             response["finger_gesture"] = point_history_classifier_labels[most_common_fg_id[0][0]]

#     return jsonify(response)

# def calc_landmark_list(image, landmarks):
#     image_width, image_height = image.shape[1], image.shape[0]
#     landmark_point = []
#     for _, landmark in enumerate(landmarks.landmark):
#         landmark_x = min(int(landmark.x * image_width), image_width - 1)
#         landmark_y = min(int(landmark.y * image_height), image_height - 1)
#         landmark_point.append([landmark_x, landmark_y])
#     return landmark_point

# def pre_process_landmark(landmark_list):
#     temp_landmark_list = copy.deepcopy(landmark_list)
#     base_x, base_y = 0, 0
#     for index, landmark_point in enumerate(temp_landmark_list):
#         if index == 0:
#             base_x, base_y = landmark_point[0], landmark_point[1]
#         temp_landmark_list[index][0] -= base_x
#         temp_landmark_list[index][1] -= base_y
#     temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
#     max_value = max(list(map(abs, temp_landmark_list)))
#     return list(map(lambda n: n / max_value, temp_landmark_list))

# def pre_process_point_history(image, point_history):
#     image_width, image_height = image.shape[1], image.shape[0]
#     temp_point_history = copy.deepcopy(point_history)
#     base_x, base_y = 0, 0
#     for index, point in enumerate(temp_point_history):
#         if index == 0:
#             base_x, base_y = point[0], point[1]
#         temp_point_history[index][0] = (temp_point_history[index][0] - base_x) / image_width
#         temp_point_history[index][1] = (temp_point_history[index][1] - base_y) / image_height
#     return list(itertools.chain.from_iterable(temp_point_history))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
