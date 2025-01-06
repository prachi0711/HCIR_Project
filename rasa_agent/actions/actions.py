# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import random  # Placeholder for Bayesian network-based career choice

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

class ActionGetCareerChoice(Action):
    def name(self):
        return "action_get_career_choice"
    
    def run(self, dispatcher, tracker, domain):
        # Extract user preferences from slots
        skills = tracker.get_slot('skills')
        interests = tracker.get_slot('interests')
        education = tracker.get_slot('education')

        

        return 'doctor'

