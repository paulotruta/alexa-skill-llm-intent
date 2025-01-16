import json
import random
from os.path import exists

from pydantic import BaseModel

CONFIG_FILE = "config.json"

DEFAULT_PROMPT = """
    You are a helpful AI assistant that responds by voice.
    Your answers should be simple and quick.
    Don't speak back for more than a couple of sentences.
    If you need to say more things, say that you're happy to continue,
    and wait for the user to ask you to continue.
    Remember, your objective is to reply as if your are having a natural
    conversation, so be relatively brief, and keep that in mind when replying.
    You were created by jpt.land as part of a personal exploration project.
    Paulo Truta is a software engineer that worked hard to make you easy!
    If the user asks about you, tell him you are the Alexa AI Skill.
    You're an helpful and funny artificial powered assistant,
    ready to answer any questions a person may have, right on Amazon Alexa.
"""


class Config(BaseModel):
    llm_url: str
    llm_key: str
    llm_model: str
    llm_system_prompt: str = DEFAULT_PROMPT


def load_config() -> Config:
    if not exists(CONFIG_FILE):
        raise ValueError("Config file does not exist")

    with open(CONFIG_FILE) as f:
        return Config.model_validate(json.load(f))


class CannedResponse:
    RESPONSES = {
        "en-US": {
            "helpPhrases": [
                "I'm a friendly and powerful AI assistant tool an I can answer any questions you have in a pertinent way! How can I help?",
                "I'm jpt.land AI, here to help you with any questions you have! What can I do for you?",
            ],
            "noMessagePhrases": [
                "Hum, I'm not sure what to say.",
                "Looks like I have no answer for that.",
            ],
            "goodbyePhrases": [
                "Goodbye! Have a great day!",
                "Goodbye! I hope I was able to help you!",
                "Goodbye! I'm here if you need me!",
                "Goodbye! I'm always here to help you!",
                "Goodbye! Was a pleasure to help you!",
            ],
            "repromptPhrases": [
                "Anything else I can help you with?",
                "What else can I help you with?",
                "What else would you like to know?",
                "Is there anything else you need help with?",
                "What else can I assist you with?",
                "If you wanna know more, just ask!",
                "Anything else you need help with?",
                "Can I help you any further?",
                "What else can I do for you?",
            ],
            "launchHandlerPhrases": [
                "Sure. What's your question?",
                "Sure. What can I help you with?",
                "Sure. What do you need help with?",
                "Sure. What can I assist you with?",
                "Sure. What's your query?",
                "Sure. What's your request?",
                "Sure. How can I be helpful?",
            ],
            "fallbackHandlerPhrases": [
                "I'm sorry, I didn't understand that. Let's try again? Just say 'yes' to continue.",
                "I'm not sure what you're asking. Let's try again? Just say 'yes' to continue.",
                "I'm sorry, I didn't catch that. Let's try again? Just say 'yes' to continue.",
            ],
        }
    }

    def __init__(self, locale: str):
        if locale not in self.RESPONSES:
            locale = "en-US"

        self.locale = locale
        self.data = self.RESPONSES[locale]

    def get_random_data_item(self, key: str) -> str:
        return random.choice(self.data[key])

    def get_help_phrase(self) -> str:
        return self.get_random_data_item("helpPhrases")

    def get_no_message_phrase(self) -> str:
        return self.get_random_data_item("noMessagePhrases")

    def get_goodbye_phrase(self) -> str:
        return self.get_random_data_item("goodbyePhrases")

    def get_reprompt_phrase(self) -> str:
        return self.get_random_data_item("repromptPhrases")

    def get_launch_handler_phrase(self) -> str:
        return self.get_random_data_item("launchHandlerPhrases")

    def get_fallback_handler_phrase(self) -> str:
        return self.get_random_data_item("fallbackHandlerPhrases")

    def get_response(self, key: str) -> str:
        return self.get_random_data_item(key)

    def get_response_list(self, key: str) -> list:
        return self.data.get(key, [])
