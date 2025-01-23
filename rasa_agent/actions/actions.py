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

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionSetInterest(Action):
    def name(self) -> Text:
        return "action_set_interest"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        interest = next(tracker.get_latest_entity_values("interest"), None)
        if interest:
            return [SlotSet("interest", interest)]
        dispatcher.utter_message(text="I didn't catch your interest. Could you please repeat?")
        return []

class ActionSetSkill(Action):
    def name(self) -> Text:
        return "action_set_skill"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        skill = next(tracker.get_latest_entity_values("skill"), None)
        if skill:
            return [SlotSet("skill", skill)]
        dispatcher.utter_message(text="I didn't catch your skill. Could you please repeat?")
        return []


class ActionSetBackground(Action):
    def name(self) -> Text:
        return "action_set_background"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        background = next(tracker.get_latest_entity_values("background"), None)
        if background:
            return [SlotSet("background", background)]
        dispatcher.utter_message(text="I didn't catch your background. Could you please repeat?")
        return []

class ActionSetLifeStyle(Action):
    def name(self) -> Text:
        return "action_set_lifestyle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lifestyle = next(tracker.get_latest_entity_values("lifestyle"), None)
        if lifestyle:
            return [SlotSet("lifestyle", lifestyle)]
        dispatcher.utter_message(text="I didn't catch your lifestyle. Could you please repeat?")
        return []


class ActionSuggestCareer(Action):
    def name(self) -> Text:
        return "action_suggest_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        interest = tracker.get_slot("interest")
        skill = tracker.get_slot("skill")

        if not interest:
            dispatcher.utter_message(text="I need your interest to suggest a career.")
            return []
        if not skill:
            dispatcher.utter_message(text="I need your skill to suggest a career.")
            return []
        
        career_suggestion = self.get_career_suggestion(interest, skill)
        dispatcher.utter_message(text=f"Based on your interest in {interest}, skill in {skill}, I suggest: {career_suggestion}.")
        return []

    @staticmethod
    def get_career_suggestion(interest: Text, skill: Text) -> Text:
       return "X"


