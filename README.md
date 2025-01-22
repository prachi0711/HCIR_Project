# HCIR Project

This project aims to build a career advisor robot using a simulated Pepper robot in Qibullet, powered by a Rasa-based conversational agent. The robot will interact with users through dialogue and provide career suggestions using bayesian network model based on their preferences.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
5. [Running the Project](#running-the-project)

## Prerequisites

Before starting, make sure you have the following:

- **Python 3.8+** installed
- **Rasa** for the conversational agent

### Install Python

You can download Python 3.8 from the official [Python website](https://www.python.org/downloads/).

### Install Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies:

```
python -m venv .venv
```
Activate the virtual environment:

Linux/macOS:
   ```
   source .venv/bin/activate
```

Windows:

    .\.venv\Scripts\activate

### Install Rasa

Rasa is used to manage the conversational flow and provide career suggestions. To set it up:

    pip install rasa

## Setup Instructions
### 1. Clone the Repository

Clone this repository to your local machine:

```
git clone git@github.com:prachi0711/HCIR_Project.git

cd HCIR_PROJECT
```

### 2. Install Dependencies

Install the required dependencies:
```
pip install -r requirements.txt
```

This will install necessary libraries like requests, pyttsx3, and others.

### 3. Set Up Rasa

Navigate to the rasa_agent directory and train the model:

    cd rasa_agent
    rasa train


## Face Detection Module

The Face Detection module is a core component of this project, enabling real-time face recognition and identification using DeepFace and a custom UserManager.

### Features
- Verifies if a face in the video stream matches any registered users.
- Detects faces every 30 frames for optimized performance.
- Displays a personalized greeting if a face is recognized.

### Code Overview
The main functionalities of the module are implemented in the `FaceDetection` class, defined in `face_detection`. Key methods include:

#### `check_face(frame)`
- Verifies the input frame against registered user images.
- Updates the `face_match` and `current_user` attributes when a match is found.

#### `run_face_detection(frame)`
- Processes video frames for face detection every 30 frames.
- Launches the `check_face` method in a separate thread for non-blocking execution.

#### `face_detected(frame)`
- Displays a greeting on the video stream if a face is successfully recognized.


### Dependencies
The module depends on the following:
- [DeepFace](https://github.com/serengil/deepface): A facial recognition framework.
- OpenCV: For video frame processing.
- `face_detection.UserManager`: A custom user management module.
- `user.json`: a custom user data in json format.

### Notes
- Ensure that the `UserManager` provides a list of user objects, each with an `image` attribute containing the user image.
- The frame passed to `run_face_detection` and `check_face` must be a valid image array compatible with DeepFace.
- For optimal performance, adjust the frame interval (`self.counter % 30`) as needed based on your application's requirements.

---


## Running the Project

The custom actions are defined in the actions.py file. To run the action server, use the following command:

    rasa run actions

Start the Rasa server to enable the robot to communicate with Rasa:

    rasa run --enable-api --cors "*"

The server will be accessible at http://localhost:5005.

Run the pepper simulation script


    python behaviour_script.py

This will launch the Qibullet simulation, start the Pepper robot, and enable the conversation to begin.


Continuous Dialogue: The conversation can continue with the user providing input, and Rasa will process and generate appropriate responses.

Text-to-Speech: The robot uses pyttsx3 for speech synthesis to convert Rasa response to speech.

Gestures: Predefined gestures (such as waving) accompany the robot’s speech.

