from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging

class ActionProvideFormulaInfo(Action):
    def name(self) -> Text:
        return "action_provide_formula_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Extract the formula type from the intent or slot
            entities = tracker.latest_message.get("entities", [])
            formula_type = next((entity.get("value") for entity in entities if entity.get("entity") == "formula_type"), None)

            # Define the utterance templates mapping from the domain
            utterance_templates = domain.get("utterances", {}).get("formulas", {})

            # Check if the formula type is supported and the corresponding utterance template exists
            if formula_type and formula_type in utterance_templates:
                dispatcher.utter_message(template=utterance_templates[formula_type])
            else:
                dispatcher.utter_message(text="Sorry, I don't have information about that formula type.")
        
        except Exception as e:
            logging.exception("An error occurred in ActionProvideFormulaInfo: {}".format(str(e)))
            dispatcher.utter_message(text="Sorry, I encountered an error while processing your request. Please try again later.")

        return []
    
class ActionOpenStarTopology(Action):

    def name(self) -> Text:
        return "action_open_star_topology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Sure, opening the Star-Topology Analysis window.", custom={"command": "OPEN_STAR_TOPOLOGY"})
        return []

class ActionOpenDaisyChainTopology(Action):

    def name(self) -> Text:
        return "action_open_daisy_chain_topology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Sure, opening the DaisyChain-Topology Analysis window.", custom={"command": "OPEN_DAISY_CHAIN"})
        return []
