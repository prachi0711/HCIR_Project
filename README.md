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
# Bayesian Network Model

## Objective:

The purpose of this model is to provide career recommendations by utilizing probabilistic reasoning. The system considers user preferences as input and outputs the most likely career option based on the Bayesian Network’s inference.

---

## 1. Components of the Network

The Bayesian Network in this project is composed of the following components:

- **User Preferences:** 
  - **Interest:** Represents the user's interest in a specific field (Science, Arts, or Technology).
  - **Skill:** Represents the user's skill level (Analytical, Creative, or Communicative).
  - **Background:** Represents the user's educational background (STEM, Humanities, or Commerce).
  - **Lifestyle:** Represents the user's preferred lifestyle (Flexible, Fixed Hours, or Traveling).
- **Career Choices:**
  - **Career:** Represents the possible career options (Data Scientist, Writer, or Manager).

Each of these nodes is a **LabelizedVariable** where the values are discrete, and each variable has three possible outcomes, represented as integers (0, 1, 2).

---

## 2. Relationships and Dependencies

In a Bayesian Network, relationships are defined by **directed edges (arcs)** between nodes, indicating dependency or influence between variables. In this network, the relationships and dependencies are as follows:

- **Interest → Career:** The user's interest in a particular field (Science, Arts, or Technology) directly influences the possible career options they may pursue.
- **Skill → Career:** The user's skill level (Analytical, Creative, or Communicative) also has a direct impact on career recommendations.
- **Background → Career:** The user's educational background (STEM, Humanities, or Commerce) is another factor influencing career choices.
- **Lifestyle → Career:** The user's preferred lifestyle (Flexible, Fixed Hours, or Traveling) affects the recommended career options.

These dependencies are encoded in the structure of the Bayesian Network, where **Career** is the child node of the other four variables (Interest, Skill, Background, and Lifestyle), implying that Career depends on these four variables.

---

## 3. Conditional Probability Table (CPT)

The Conditional Probability Table (CPT) defines the probability of each possible outcome for a node, given the values of its parent nodes. For each variable in the network (Interest, Skill, Background, Lifestyle), a prior probability distribution is defined. 

For example:
- The **CPT for Interest** might define the probability distribution of the user's interest in Science, Arts, or Technology, with values such as:
  - Interest = Science (0.4), Arts (0.3), Technology (0.3).
  
- The **CPT for Skill** defines the probability distribution for the user's skill type, e.g.:
  - Skill = Analytical (0.3), Creative (0.4), Communicative (0.3).

For the **Career** variable, the CPT defines the probabilities of each career option (Data Scientist, Writer, or Manager) based on different combinations of the values for **Interest**, **Skill**, **Background**, and **Lifestyle**. These probabilities are assigned manually, reflecting how likely each career is given different combinations of user preferences.

For example:
- If the user’s interest is in Science, their skill level is Analytical, and their background is in STEM, the probability of them being recommended as a **Data Scientist** might be very high (e.g., 0.9), with lower probabilities for Writer and Manager (e.g., 0.05 each).

--- 

## 4. Inference Process

The inference process in a Bayesian Network is the calculation of the posterior probabilities of certain variables, given evidence (observed values) for other variables. The process involves updating the probabilities of the **Career** node based on the user’s inputs (the evidence provided for Interest, Skill, Background, and Lifestyle).

### Steps of Inference:

1. **Set Evidence:** The user’s preferences for Interest, Skill, Background, and Lifestyle are input as evidence. These inputs set the values for the corresponding nodes in the network.

2. **Make Inference:** Once the evidence is set, the Bayesian Network calculates the posterior probability distribution for the **Career** node. This process uses the dependencies and CPTs defined in the network to propagate the evidence through the network and calculate the likelihood of each career option.

3. **Rank Career Options:** After inference, the system outputs the posterior probabilities for each career option (Data Scientist, Writer, Manager). These probabilities are used to rank the careers in order of likelihood, with the most probable career being the highest ranked.

The **LazyPropagation** algorithm in pyAgrum is used for efficient inference. It ensures that the network is updated and the posterior probabilities are computed accurately, given the observed evidence.

--- 

## Manager Class: PepperCareerAdvisor

The `PepperCareerAdvisor` class integrates various modules, such as Rasa, Bayesian networks, Face Detection, Behavior Control, and a GUI interface.

### Features
- Combines Rasa for conversational AI and behavior control for dynamic responses.
- Includes a GUI built with Tkinter for user interaction.
- Uses Face Detection to authenticate users and personalize conversations.
- Displays real-time webcam feed with user greetings.

### Code Overview
The main functionalities of the `PepperGUI` class include:

#### `initialize_console()`
- Sets up the GUI console for displaying messages and receiving user input.

#### `initialize_webcam()`
- Configures the webcam feed area in the GUI.

#### `process_input(event)`
- Handles user input from the console.
- Starts the webcam for user authentication or processes chatbot queries based on input.

#### `start_webcam()`
- Activates the webcam and uses the `FaceDetection` module to identify users.
- Updates the GUI with the authenticated user's name and starts the conversation.

#### `update_webcam_feed(frame)`
- Updates the webcam feed on the GUI with real-time video frames.

#### `process_user_input(user_input)`
- Sends user input to the Rasa server and displays the chatbot's response in the GUI.

#### `send_message_to_rasa(message)`
- Sends a message to the Rasa server via REST API and returns the chatbot's response.

#### `close_app()`
- Safely terminates the application and releases resources.

### Dependencies
The `PepperGUI` module depends on the following:
- Tkinter: For creating the graphical user interface.
- OpenCV: For handling video streams.
- Rasa: For conversational AI.
- `face_detection.FaceDetection`: For user authentication.
- `behaviour.BehaviourController`: For behavior management and dynamic responses.

### Notes
- Ensure the Rasa server is running and accessible at the specified `rasa_url`.
- Webcam access is required for the face detection feature.
---


## Running the Project

The custom actions are defined in the actions.py file. To run the action server, use the following command:

    rasa run actions

Start the Rasa server to enable the robot to communicate with Rasa:

    rasa run --enable-api --cors "*"

The server will be accessible at http://localhost:5005.

Run the pepper simulation script


    python PepperCareerAdvisor.py

This will launch the Qibullet simulation, start the Pepper robot, and enable the conversation to begin.


Continuous Dialogue: The conversation can continue with the user providing input, and Rasa will process and generate appropriate responses.

Text-to-Speech: The robot uses pyttsx3 for speech synthesis to convert Rasa response to speech.

Gestures: Predefined gestures (such as waving) accompany the robot’s speech.

