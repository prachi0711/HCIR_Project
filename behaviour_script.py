from qibullet import SimulationManager, PepperVirtual
import pyttsx3
import time
import requests

class PepperCareerAdvisor:
    def __init__(self, gui=True, rasa_url="http://localhost:5005/webhooks/rest/webhook"):
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
        
        # Rasa webhook URL
        self.rasa_url = rasa_url
        self.session_id = None

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

    def send_message_to_rasa(self, message):
        """Sends user message to Rasa and returns the response."""
        payload = {
            "message": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        if not self.session_id:
            # Start a new session with Rasa if one doesn't exist
            self.session_id = str(int(time.time()))  # Use timestamp as session id

        payload["sender"] = self.session_id  # Pass the session id for tracking

        response = requests.post(self.rasa_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"text": "I'm sorry, I couldn't process that request."}

    def process_user_input(self, user_input):
        """Processes the user input via Rasa and triggers appropriate actions."""
        rasa_response = self.send_message_to_rasa(user_input)
        
        if rasa_response:
            # Handle the response, here we assume Rasa sends a text response
            for response in rasa_response:
                if 'text' in response:
                    response_text = response['text']
                    self.speak(response_text)
    
    def start_conversation(self):
        """Handles continuous conversation with the user."""
        self.greet_user(user_name="Alex")
        
        try:
            while True:
                user_input = input("You: ")  # Get input from the user
                if user_input.lower() in ["exit", "quit", "bye"]:
                    break  # End the conversation if the user types exit or quit
                
                self.process_user_input(user_input)
            
        except KeyboardInterrupt:
            print("\nConversation ended.")
        
        finally:
            self.say_goodbye()
            self.stop_simulation()

if __name__ == "__main__":
    advisor = PepperCareerAdvisor(gui=True)
    advisor.start_conversation()
