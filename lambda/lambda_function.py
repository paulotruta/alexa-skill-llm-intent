# -*- coding: utf-8 -*-

# Alexa skill that uses a QuestionIntentHandler to proxy a request to a
# LLM API or Webhook, and provide the answer.
# Developed by @paulotruta and @inverse
# as an exploration of voice powered LLM during the early days.

# Uses Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on
# implementing Alexa features!

import logging

import requests
from ask_sdk_core import utils as ask_utils
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response
from utils import load_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = load_config()


class LLMQuestionProxy:
    """Handler to communicate with an LLM via API or Webhook.
    Ask a question and it shall provide an answer."""

    LLM_URL = config["llm_url"]
    LLM_KEY = config["llm_key"]
    LLM_MODEL = config["llm_model"]

    def api_request(self, question: str) -> dict:
        """Send a request to the LLM API and return the response."""
        url = self.LLM_URL
        headers = {
            "Authorization": f"Bearer {self.LLM_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.LLM_MODEL,
            "question": question,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["text"]
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            # Return an error message, but only say part of the error message
            return {
                "message": f"Sorry, I encontered an error processing your \
                    request: {str(e)[:100]}"
            }

    def webhook_request(self, question: str, session_key: str = None) -> dict:
        """Send a request to the LLM API and return the response."""
        
        payload = {
            "message": question, 
            "token": self.LLM_KEY
        }
        
        if session_key:
            payload["session_key"] = session_key

        try:
            # Send a POST request
            response = requests.post(self.LLM_URL, json=payload)

            # Raise an exception if the request was not successful
            response.raise_for_status()

            # Parse and return response JSON
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            # Return an error message, but only say part of the error message
            return {
                "message": f"Sorry, I encountered an error processing your \
                    request: {str(e)[:100]}"
            }

    def ask(self, question: str, who: str = None) -> dict:
        """Ask a question and get a response."""
        if self.LLM_MODEL != "webhook":
            return self.api_request(question)
        else:
            return self.webhook_request(question, who)


class BaseRequestHandler(AbstractRequestHandler):
    """Base class for request handlers."""

    question = LLMQuestionProxy()

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return True

    def handle(self, handler_input: HandlerInput) -> Response:
        raise NotImplementedError


class LaunchRequestHandler(BaseRequestHandler):
    """
    Handler for Skill Launch.
    This is the first handler that is called when the skill is invoked
    directly. Will only be invoked if the intent does not have
    a LaunchRequest handling in its config.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # TODO: Implement something a bit more dynamic (randomized from a list)
        speak_output = "Sure, what is the question?"

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class QuestionIntentHandler(BaseRequestHandler):
    """
    Main Handler for turn chat question/answer flow. Receive a question
    and provides an answer.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("QuestionIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:

        # Get the question from the user
        slots = handler_input.request_envelope.request.intent.slots
        
        voice_prompt = slots["searchQuery"].value
        
        logger.info(handler_input.request_envelope)
        logger.info("User requests: " + voice_prompt)
        
        user_id = handler_input.request_envelope.session.user.user_id
        logger.info("User id: " + user_id)

        # Ask the LLM for a response
        response = self.question.ask(voice_prompt, user_id)
        logger.info(response)
        logger.info("LLM Response: " + response["message"])

        # Speak the response or fallback message
        # TODO: Implement something a bit more dynamic (randomized from a list)

        speak_output = response.get("message", "I'm not sure what to say.")
        return (
            handler_input.response_builder.speak(speak_output)
            .ask("Can I help you any further?")
            .response
        )


class HelpIntentHandler(BaseRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = "{} {}".format(
            "I'm a friendly and powerful AI assistant tool \
            an I can answer any questions you have in a pertinent way!",
            "How can I help?",
        )

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(BaseRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(
            handler_input
        ) or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # TODO: Implement something a bit more dynamic (randomized from a list)
        speak_output = "Goodbye!"
        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(BaseRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In FallbackIntentHandler")

        # TODO: Find a way to get the last question asked
        # (utterance that triggered this).
        # Due to the way the fallbackintenthandler is structured,
        # this does not seem possible atm.
        voice_prompt = " \
            I'm terribly sorry, I didn't understand that. \
            Could you please repeat it? \
        "
        logger.info("Response:  " + voice_prompt)

        speech = voice_prompt
        reprompt = "Anything else I can help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(BaseRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.response


class IntentReflectorHandler(BaseRequestHandler):
    """
    The intent reflector is used for interaction
    model testing and debugging.

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
            .ask("Can I help you any further?")
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

        return handler_input.response_builder.speak(speak_output).response


# The SkillBuilder object acts as the entry point for your skill
# It is basically the router for request / responses
# Declaration order matters - they're processed top to bottom.

sb = SkillBuilder()

# first add all the request handlers

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuestionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# naking sure IntentReflectorHandler is last
# (doesn't override your custom handlers)

sb.add_request_handler(IntentReflectorHandler())

# finally add the exception handler
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
