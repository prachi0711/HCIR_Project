import time
import requests
from soupsieve.css_match import Inputs

from behaviour import BehaviourController
from face_detection import FaceDetection


class PepperCareerAdvisor:
    def __init__(self, rasa_url="http://localhost:5005/webhooks/rest/webhook"):
        # Rasa webhook URL
        self.rasa_url = rasa_url
        self.session_id = None
        self.behaviour_controller = BehaviourController.BehaviourController(gui=True)


    def start_conversation(self, username):
        """Handles continuous conversation with the user."""
        self.behaviour_controller.greet_user(username)

        try:
            while True:
                user_input = input("You: ")  # Get input from the user
                if user_input.lower() in ["exit", "quit", "bye"]:
                    break  # End the conversation if the user types exit or quit

                self.process_user_input(user_input)

        except KeyboardInterrupt:
            print("\nConversation ended.")

        finally:
            self.behaviour_controller.say_goodbye()
            self.behaviour_controller.stop_simulation()

    def process_user_input(self, user_input):
        """Processes the user input via Rasa and triggers appropriate actions."""
        rasa_response = self.send_message_to_rasa(user_input)

        if rasa_response:
            # Handle the response, here we assume Rasa sends a text response
            for response in rasa_response:
                if 'text' in response:
                    response_text = response['text']
                    self.behaviour_controller.speak(response_text)

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

if __name__ == "__main__":
    advisor = PepperCareerAdvisor()

    user_input = input("Would you like to start conversation? (Yes/No):")
    if user_input.lower() in ["yes", "y"]:
        face_detection = FaceDetection.FaceDetection()
        user_name = face_detection.run_face_detection()
        advisor.start_conversation(user_name)
    else:
        print("See you!")
