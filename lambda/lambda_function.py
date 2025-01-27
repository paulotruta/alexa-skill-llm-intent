# -*- coding: utf-8 -*-

# Alexa skill that uses a QuestionIntentHandler to proxy a request to a
# LLM API or Webhook, and provide the answer.
# Developed by @paulotruta and @inverse
# as an exploration of voice powered LLM during the early days.

# Uses Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on
# implementing Alexa features!

import logging

import requests  # noqa: E402
from ask_sdk_core import utils as ask_utils
from ask_sdk_core.dispatch_components import (
    AbstractExceptionHandler,
    AbstractRequestHandler,
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response
from llm_intent.llm_client import LLMClient
from llm_intent.utils import CannedResponse, load_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = load_config()
canned_response = CannedResponse("en-US")

LLM_URL = config["llm_url"]
LLM_KEY = config["llm_key"]
LLM_MODEL = config["llm_model"]
LLM_SYSTEM_PROMPT = config.get(
    "llm_system_prompt",
    """
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
""",
)


class LLMQuestionProxy:
    """Handler to communicate with an LLM via API or Webhook.
    Ask a question and it shall provide an answer."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def api_request(self, question: str) -> dict:
        """Send a request to the LLM API and return the response."""
        logger.info(
            "API Request - " + self.llm_client.url + " - " + self.llm_client.model
        )

        try:
            response = self.llm_client.api_request(LLM_SYSTEM_PROMPT, question)

            logger.info(response)

            return {"message": response["choices"][0]["message"]["content"]}
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            # Return an error message, but only say part of the error message
            return {
                "message": f"Sorry, I encountered an error thinking about your request: {str(e)[:100]}"
            }

    def webhook_request(self, question: str, context: dict) -> dict:
        """Send a request to the LLM API and return the response."""
        try:
            response = self.llm_client.webhook_request(question, context)

            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            # Return an error message, but only say part of the error message
            return {
                "message": f"Sorry, I encountered an error processing your \
                    request: {str(e)[:100]}"
            }

    def ask(self, question: str, context: dict = {}) -> dict:
        """Ask a question and get a response."""
        if LLM_MODEL != "webhook":
            logger.info("Using API request")
            return self.api_request(question)
        else:
            logger.info("Using Webhook request")
            return self.webhook_request(question, context)


class BaseRequestHandler(AbstractRequestHandler):
    """Base class for request handlers."""

    question = LLMQuestionProxy(LLMClient(LLM_URL, LLM_KEY, LLM_MODEL))

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
        speak_output = canned_response.get_launch_handler_phrase()

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class QuestionIntentHandler(BaseRequestHandler):
    """
    Main Handler for turn chat question/answer flow. Receive a question and provides an answer.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("QuestionIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # Get the question from the user
        slots = handler_input.request_envelope.request.intent.slots

        voice_prompt = slots["searchQuery"].value

        logger.info(handler_input.request_envelope)
        logger.info("User requests: " + voice_prompt)

        context_data = {
            "user_id": handler_input.request_envelope.session.user.user_id,
            "device_id": handler_input.request_envelope.context.system.device.device_id,
            "application_id": handler_input.request_envelope.context.system.application.application_id,
            "api_access_token": handler_input.request_envelope.context.system.api_access_token,
            "api_endpoint": handler_input.request_envelope.context.system.api_endpoint,
            "locale": handler_input.request_envelope.request.locale,
            "intent": handler_input.request_envelope.request.intent.name,
        }

        logger.info(context_data)

        # Ask the LLM for a response
        response = self.question.ask(voice_prompt, context_data)

        logger.info(response)
        logger.info("LLM Response: " + response["message"])

        # Speak the response or fallback message
        # TODO: Implement something a bit more dynamic (randomized from a list)

        speak_output = response.get("message", canned_response.get_no_message_phrase())
        return (
            handler_input.response_builder.speak(speak_output)
            .ask(canned_response.get_reprompt_phrase())
            .response
        )


class HelpIntentHandler(BaseRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speak_output = canned_response.get_help_phrase()

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(canned_response.get_reprompt_phrase())
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
        speak_output = canned_response.get_goodbye_phrase()
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
        voice_prompt = canned_response.get_fallback_handler_phrase()
        logger.info("Response:  " + voice_prompt)

        speech = voice_prompt
        reprompt = canned_response.get_reprompt_phrase()

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
            .ask(canned_response.get_reprompt_phrase())
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

        speak_output = canned_response.get_fallback_handler_phrase()

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
