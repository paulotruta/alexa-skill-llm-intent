# -*- coding: utf-8 -*-

# chatGPT Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on
# implementing Alexa features!

import logging

from ask_sdk_core import utils as ask_utils
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response
from revChatGPT.revChatGPT import Chatbot
from utils import load_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = load_config()

# Set up ChatGPT
chatgpt = Chatbot(config)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "Sure, what is the question?"

        chatgpt.reset_chat()
        # Uses the session_token to get a new bearer token
        chatgpt.refresh_session()

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class QuestionIntentHandler(AbstractRequestHandler):
    """Handler for chat GTP to receive a question and provide an answer."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("QuestionIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # Uses the session_token to get a new bearer token
        chatgpt.refresh_session()
        slots = handler_input.request_envelope.request.intent.slots
        voice_prompt = slots["searchQuery"].value
        logger.info("User says: " + voice_prompt)
        response = chatgpt.get_chat_response(voice_prompt)
        logger.info(response)
        logger.info("ChatGPT says: " + response["message"])
        speak_output = response["message"]

        return (
            handler_input.response_builder.speak(speak_output)
            .ask("Can I help you any further?")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "{} {}".format(
            "I'm partnering with chat GPT by Open AI, \
            to be able to answer anyquestions you have in a pertinent way!",
            "How can I help?",
        )

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "Goodbye!"

        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In FallbackIntentHandler")

        speech = "Hmm, I'm not sure I understood correctly. Please try again."
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        chatgpt.reset_chat()

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.

    It will simply repeat the intent the user said.
    You can create custom handlers for your intents by defining them above,
    then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder.speak(speak_output)
            .ask("Can i help you any further?")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors.

    If you receive an error stating the request handler chain is not found,
    you have not implemented a handler for the intent being invoked or included
    it in the skill builder below.
    """

    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error(exception, exc_info=True)

        speak_output = "{} {}".format(
            "Sorry, I had trouble doing what you asked.", "Please try again."
        )

        return (
            handler_input.response_builder.speak(speak_output)
            # .ask(speak_output)
            .response
        )


# The SkillBuilder object acts as the entry point for your skill
# It is basically the router for request / responses
# Declaration order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuestionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# make sure IntentReflectorHandler is last
# (doesn't override your custom handlers)
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
