import cv2
import mediapipe as mp
import time

from modules import (
    drone,
    gestures,
    configs,
)

drone_configs = configs.load_drone_config()
CONNECTION_STRING = drone_configs["connection_string"]
TAKEOFF_ALT = drone_configs["takeoff_alt"]
TRAVEL_SPEED = drone_configs["speeds"]["travel"]
UP_SPEED = drone_configs["speeds"]["up"]
DOWN_SPEED = drone_configs["speeds"]["down"]
YAW_RATE_STATIC = drone_configs["speeds"]["yaw_rate_static"]
YAW_RATE_TRAVEL = drone_configs["speeds"]["yaw_rate_travel"]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

def main():
    drone_connection = drone.Drone(connection_string=CONNECTION_STRING)
    action_text, prev_action_text = '', ''
    timestamp = time.time()
    
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            action_text = 'No Action'

            if results.multi_hand_landmarks and results.multi_handedness:
                hands_info = {}
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = results.multi_handedness[idx].classification[0].label
                    status = gestures.hand_fingers_status(hand_landmarks, handedness)
                    gesture = gestures.gesture_from_fingers(status)
                    hands_info[handedness] = gesture

                if 'Left' in hands_info and 'Right' in hands_info:
                    if hands_info['Left'] == 'fist' and hands_info['Right'] == 'fist':
                        action_text = 'RTL'
                        print(action_text)
                    elif hands_info['Left'] == 'open_palm' and hands_info['Right'] == 'open_palm':
                        action_text = 'Fly Forwards'
                        print(action_text)
                    elif hands_info['Left'] == 'peace_sign' and hands_info['Right'] == 'peace_sign':
                        action_text = 'Takeoff'
                        print(action_text)
                    elif hands_info['Left'] == 'peace_sign' and hands_info['Right'] == 'open_palm':
                        action_text = 'Fly Forwards AND Yaw Left'
                        print(action_text)
                    elif hands_info['Right'] == 'peace_sign' and hands_info['Left'] == 'open_palm':
                        action_text = 'Fly Forwards AND Yaw Right'
                        print(action_text)
                    elif hands_info['Left'] == 'fist' and hands_info['Right'] == 'open_palm':
                        action_text = 'Fly Left'
                        print(action_text)
                    elif hands_info['Right'] == 'fist' and hands_info['Left'] == 'open_palm':
                        action_text = 'Fly Right'
                        print(action_text)
                    else:
                        for hand, gesture in hands_info.items():
                            if gesture == 'open_palm':
                                action_text = 'Fly Forwards' if hand == 'Left' else 'Fly Forwards'
                            elif gesture == 'peace_sign':
                                action_text = 'Yaw Left' if hand == 'Left' else 'Yaw Right'
                            elif gesture == 'fist':
                                action_text = 'Fly Down' if hand == 'Left' else 'Fly Up'
                            print(action_text)
                else:
                    for hand, gesture in hands_info.items():
                        if gesture == 'open_palm':
                            action_text = 'Fly Forwards' if hand == 'Left' else 'Fly Forwards'
                        elif gesture == 'peace_sign':
                            action_text = 'Yaw Left' if hand == 'Left' else 'Yaw Right'
                        elif gesture == 'fist':
                            action_text = 'Fly Down' if hand == 'Left' else 'Fly Up'
                        print(action_text)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            cv2.putText(frame, f'Action: {action_text}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Drone Gesture Control', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            if action_text != prev_action_text:
                timestamp = time.time()
                prev_action_text = action_text
            else:
                if time.time() - timestamp > 1:
                    if action_text == 'Takeoff':
                        drone_connection.arm()
                        drone_connection.takeoff(altitude=TAKEOFF_ALT)
                    elif action_text == 'RTL':
                        drone_connection.rtl()
                    elif action_text == 'Fly Forwards':
                        drone_connection.set_speed(vx=TRAVEL_SPEED, vy=0, vz=0)
                    elif action_text == 'Fly Up':
                        drone_connection.set_speed(vx=0, vy=0, vz=-UP_SPEED)
                    elif action_text == 'Fly Down':
                        drone_connection.set_speed(vx=0, vy=0, vz=DOWN_SPEED)
                    elif action_text == 'Yaw Left':
                        drone_connection.set_yaw_rate(yaw_rate=-YAW_RATE_STATIC)
                    elif action_text == 'Yaw Right':
                        drone_connection.set_yaw_rate(yaw_rate=YAW_RATE_STATIC)
                    elif action_text == 'Fly Forwards AND Yaw Left':
                        drone_connection.set_speed_and_yaw_rate(vx=TRAVEL_SPEED, vy=0, vz=0, yaw_rate=-YAW_RATE_TRAVEL)
                    elif action_text == 'Fly Forwards AND Yaw Right':
                        drone_connection.set_speed_and_yaw_rate(vx=TRAVEL_SPEED, vy=0, vz=0, yaw_rate=YAW_RATE_TRAVEL)
                    elif action_text == 'Fly Left':
                        drone_connection.set_speed(vx=0, vy=-TRAVEL_SPEED, vz=0)
                    elif action_text == 'Fly Right':
                        drone_connection.set_speed(vx=0, vy=TRAVEL_SPEED, vz=0)
                    else:
                        drone_connection.set_speed_and_yaw_rate(vx=0, vy=0, vz=0, yaw_rate=0)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
