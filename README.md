# Hand-Gesture-Drone
# ✋🛸 Drone Control via Hand Gestures (MediaPipe + OpenCV)

This project enables **gesture-based drone control** using real-time webcam input and **MediaPipe Hands**. Control a drone by simply moving your hands — no controllers or voice required!

---

## ✨ Features

- 🖐️ **Hand Gesture Detection** – Uses MediaPipe to detect and classify hand gestures.
- 🎮 **Gesture-to-Command Mapping** – Predefined gestures translate directly to drone actions.
- 🚁 **Drone API Integration** – Commands are executed through a MAVLink-compatible drone interface.
- 📹 **Live Webcam Feed** – Visual feedback and action overlays shown in real-time.
- ✅ **Safety Checks** – Commands are only triggered if gestures persist for over 1 second.

---

## ✋ Supported Gestures

| Left Hand       | Right Hand      | Drone Action                        |
|-----------------|------------------|-------------------------------------|
| ✌️ Peace Sign   | ✌️ Peace Sign   | Takeoff                             |
| ✊ Fist          | ✊ Fist          | Return to Launch (RTL)              |
| 🖐️ Open Palm   | 🖐️ Open Palm   | Fly Forwards                        |
| ✌️ Peace Sign   | 🖐️ Open Palm   | Fly Forwards + Yaw Left             |
| 🖐️ Open Palm   | ✌️ Peace Sign   | Fly Forwards + Yaw Right            |
| ✊ Fist          | 🖐️ Open Palm   | Fly Left                            |
| 🖐️ Open Palm   | ✊ Fist          | Fly Right                           |
| ✌️ Peace Sign   | ---          | Yaw Left    |
| ---             | ✌️ Peace Sign | Yaw Right    |
| ✊ Fist          | ---          | Fly Down       |
| ---          | ✊ Fist          | Fly Up       |
| 🖐️ Open Palm   | ---         | Fly Forwards                        |
| ---   | 🖐️ Open Palm         | Fly Forwards                        |

---

## ⚙️ How It Works

1. Launch the system using your webcam.
2. The program detects hand landmarks using MediaPipe.
3. Hand poses (open palm, fist, peace sign) are classified per hand.
4. If a valid gesture is held for more than one second, the corresponding drone command is executed.
5. Visual feedback is provided via OpenCV.

---

## 📦 Modules

- `drone.py` – Abstraction layer for MAVLink drone commands (arm, takeoff, movement, yaw, RTL).
- `gestures.py` – Classifies finger status and maps them to predefined gestures.
- `configs.py` – Loads drone-specific configuration like connection strings and speeds.

---

## 🧭 Example Commands

- **Takeoff** → ✌️ + ✌️
- **Fly Forward** → 🖐️ + 🖐️
- **Yaw Left** → ✌️ (Left hand only)
- **Fly Up** → ✊ (Right hand only)
- **RTL (Return to Launch)** → ✊ + ✊

---

## 🛠️ Requirements

- Python 3.7+
- Webcam
- Recommended Python packages:
  - `mediapipe`
  - `opencv-python`
  - `pymavlink`
- See [requirements.txt](./requirements.txt) for more!

---
## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/SuperMK15/Gestures-to-MAVLink.git
   cd Gestures-to-MAVLink
   ```

2. Create `venv` and install dependencies:
   ```bash
   python -m venv venv
   ./venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start MAVLink forwarding from Mission Planner (or whatever GCS software you use) and modify the drone connection string inside [drone.yaml](./configs/drone.yaml) accordingly:
   ```yaml
   connection_string: "tcp:127.0.0.1:14550"
   ```

4. Run [main.py](./main.py):
   ```bash
   python main.py
   ```

---
## ⚠️ Disclaimer
- Always test indoors with props removed or in a safe simulation environment first. Ensure safety protocols are in place when flying a real drone.