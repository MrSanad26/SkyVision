# Sky Vision - Face Recognition and Drone Integration

Sky Vision is an application that combines face recognition technology with drone control to aid in the identification and capture of criminals. The application allows users to connect to a Tello drone, control its movement, and identify wanted individuals in real-time. This README.md file provides an overview of the code, its functionalities, and how to use the application.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Drone Control](#drone-control)
- [Face Recognition](#face-recognition)
- [MongoDB Integration](#mongodb-integration)
- [Application Interface](#application-interface)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

Sky Vision offers the following features:

1. **Drone Control**: You can connect to a Tello drone and control its movements using keyboard shortcuts.

2. **Face Recognition**: The application uses face recognition technology to identify and match faces in real-time.

3. **Wanted Persons Database**: Information about wanted individuals is stored in a MongoDB database and retrieved for matching.

4. **Real-Time Updates**: The application updates information about the identified person's last seen time and location.

5. **Visual Interface**: Sky Vision provides a visual interface with information displayed on the screen, making it user-friendly.

## Requirements

To use Sky Vision, you need the following:

- [Python 3](https://www.python.org/downloads/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Face Recognition Library](https://pypi.org/project/face-recognition/)
- [DJI Tello Python Library](https://github.com/damiafuentes/DJITelloPy)
- [Keyboard Module](https://pypi.org/project/keyboard/)
- [Pymongo](https://pypi.org/project/pymongo/)
- A DJI Tello drone

## Installation

1. Clone or download the Sky Vision repository to your local machine.

2. Install the required Python packages if you haven't already. You can use pip for this:

   ```bash
   pip install opencv-python
   pip install face-recognition
   pip install djitellopy
   pip install keyboard
   pip install pymongo
   ```

3. Ensure that you have MongoDB installed and running, and adjust the MongoDB connection details in the code as needed.

4. Make sure you have the necessary image files for wanted individuals in the "wantedPersons" directory.

## Usage

1. Connect your Tello drone to your computer and power it on.

2. Run the Sky Vision application by executing the Python script.

   ```bash
   python sky_vision.py
   ```

3. The application will open, and you will see the live camera feed from the drone.

4. Sky Vision will start recognizing faces in the video feed and compare them to the images in the "wantedPersons" directory.

## Drone Control

You can control the drone using the following keyboard shortcuts:

- `W` - Move forward
- `S` - Move backward
- `A` - Move left
- `D` - Move right
- `UP` - Increase altitude
- `DOWN` - Decrease altitude
- `Q` - Rotate left
- `E` - Rotate right
- `T` - Takeoff
- `L` - Land

## Face Recognition

- When a wanted individual is detected, the person's information is displayed on the screen, including their name, severity, last seen time, and last seen location.

- You can approve or deny a person by pressing `P` or `O`, respectively.

## MongoDB Integration

Sky Vision integrates with MongoDB to store and retrieve information about wanted individuals. Make sure your MongoDB server is running, and update the MongoDB connection details in the code if necessary.

## Application Interface

The application provides a visual interface with live video feed, recognized faces, and information about wanted persons. The interface is designed to be user-friendly and informative.

## Keyboard Shortcuts

Sky Vision uses keyboard shortcuts for drone control and interaction with the application. Refer to the [Drone Control](#drone-control) and [Face Recognition](#face-recognition) sections for details on keyboard shortcuts.

## Troubleshooting

If you encounter any issues or have questions, please refer to the code or the libraries' documentation for troubleshooting. Ensure that all requirements are met and that your drone is properly connected.

## Contributing

Contributions to Sky Vision are welcome. If you'd like to contribute, please open an issue or create a pull request on the GitHub repository.


---

Sky Vision is a powerful tool that combines drone technology with face recognition to enhance security and law enforcement efforts. It provides real-time identification of wanted individuals and can be a valuable asset in various applications, including criminal tracking and public safety.
