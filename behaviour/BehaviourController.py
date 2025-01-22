from qibullet import SimulationManager, PepperVirtual
import pyttsx3
import time

class BehaviourController:
    def __init__(self, gui=True):
        # Initialize simulation and Pepper
        self.sim_manager = SimulationManager()
        self.client = self.sim_manager.launchSimulation(gui=gui)
        self.pepper = self.sim_manager.spawnPepper(self.client, spawn_ground_plane=True)
        self.pepper.goToPosture("Stand", 0.6)

        # Text-to-speech setup
        self.tts_engine = pyttsx3.init(driverName='espeak')
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)

    def greet_user(self, user_name=None):
        """Generates a multi-modal greeting."""
        if user_name:
            message = f"Hello, {user_name}! I am your career advisor. How can I help you?"
        else:
            message = "Hello! I am your career advisor. How can I help you?"

        self.wave()
        self.speak(message)

    def speak(self, text):
        """Makes Pepper speak the given text."""
        print(text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def wave(self):
        """Makes Pepper perform a waving motion."""
        arm_joints = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll']
        wave_positions = [
            [1.5, 0.1, -1.0, -0.4],  # Start: arm up, open palm position
            [-1.0, 1.0, -1.0, -0.8],
            [-1.0, 1.0, -1.0, 0.8],
            [-1.0, 1.0, -1.0, -0.8],
            [1.5, 0.1, -1.0, -0.4]  # Return to initial position
        ]

        for position in wave_positions:
            self.pepper.setAngles(arm_joints, position, 1.0)
            time.sleep(0.2)


    def say_goodbye(self):
        """Generates a goodbye message and wave."""
        self.speak("Thank you for visiting! Goodbye and good luck with your career.")
        self.wave()

    def stop_simulation(self):
        """Stops the simulation."""
        self.sim_manager.stopSimulation(self.client)