import json
from os.path import exists

CONFIG_FILE = "config.json"

CANNED_RESPONSES = {
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
        "fallbackHandlerPhrases": [
            "I'm sorry, I didn't understand that. Let's try again? Just say 'yes' to continue.",
            "I'm not sure what you're asking. Let's try again? Just say 'yes' to continue.",
            "I'm sorry, I didn't catch that. Let's try again? Just say 'yes' to continue.",
        ],
    }
}


def load_config() -> dict:
    if not exists(CONFIG_FILE):
        raise ValueError(f"Config file does not exist")

    with open(CONFIG_FILE) as f:
        return json.load(f)
