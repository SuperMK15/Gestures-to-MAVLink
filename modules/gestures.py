import cv2
import mediapipe as mp

# Finger indices in mediapipe landmarks:
# Thumb: tip=4, IP=3, MCP=2, CMC=1
# Index: tip=8, DIP=7, PIP=6, MCP=5
# Middle: tip=12, DIP=11, PIP=10, MCP=9
# Ring: tip=16, DIP=15, PIP=14, MCP=13
# Pinky: tip=20, DIP=19, PIP=18, MCP=17

def finger_is_open(hand_landmarks, finger_name):
    landmarks = hand_landmarks.landmark
    finger_tips = {'index': 8, 'middle': 12, 'ring': 16, 'pinky': 20}
    finger_pips = {'index': 6, 'middle': 10, 'ring': 14, 'pinky': 18}
    tip = landmarks[finger_tips[finger_name]]
    pip = landmarks[finger_pips[finger_name]]
    return tip.y < pip.y  # finger is open if tip is above pip vertically

def thumb_is_open(hand_landmarks, handedness_str):
    landmarks = hand_landmarks.landmark
    tip = landmarks[4]
    ip = landmarks[3]
    if handedness_str == 'Right':
        return tip.x > ip.x
    else:
        return tip.x < ip.x

def hand_fingers_status(hand_landmarks, handedness_str):
    status = {}
    status['thumb'] = thumb_is_open(hand_landmarks, handedness_str)
    for finger in ['index', 'middle', 'ring', 'pinky']:
        status[finger] = finger_is_open(hand_landmarks, finger)
    return status

def gesture_from_fingers(status):
    all_open = all(status[f] for f in status)
    all_closed = not any(status[f] for f in status)
    peace = status['index'] and status['middle'] and not status['ring'] and not status['pinky']

    if all_open:
        return 'open_palm'
    if peace:
        return 'peace_sign'
    if all_closed:
        return 'fist'
    return 'unknown'
