# -*- coding: utf-8 -*-

# Alexa skill that uses a QuestionIntentHandler to proxy a request to a
# LLM API or Webhook, and provide the answer.
# Developed by @paulotruta and @inverse
# as an exploration of voice powered LLM during the early days.

# Uses Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on
# implementing Alexa features!

import json
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
from utils import CannedResponse, load_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = load_config()
canned_response = CannedResponse()


class LLMQuestionProxy:
    """Handler to communicate with an LLM via API or Webhook.
    Ask a question and it shall provide an answer."""

    LLM_URL = config["llm_url"]
    LLM_KEY = config["llm_key"]
    LLM_MODEL = config["llm_model"]

    LLM_SYSTEM_PROMPT = """
        You are a helpful AI assistant that respoonds by voice.
        Your answers should be simple and quick.
        Don't speak back for more than 5 seconds.
        If you need to say more things, say that you're happy to continue and wait for the user to ask you to continue.
        Remember, your objective is to reply in as little time as possible, so keep that in mind and don't think a lot about the answer.
        You were created by jpt.land as part of a personal exploration project. Paulo Truta worked to make you easy to use!
        If the user asks about you, tell him ou are the Alexa Artificial Intelligence Skill.
        You're an helpful and funny artificial intelligente powered assistant ready to answer any questions a person may have, right on Amazon Alexa.
    """

    def api_request(self, question: str, context: dict = {}) -> dict:
        """Send a request to the LLM API and return the response."""
        logger.info("API Request - " + self.LLM_URL + " - " + self.LLM_MODEL)

        url = self.LLM_URL

        headers = {
            "Authorization": f"Bearer {self.LLM_KEY}",
            "Content-Type": "application/json",
            "HTTP_Referer": "wordpress.jpt.land/ai",
            "X-Title": "jpt.land AI",
        }

        payload = {
            "model": self.LLM_MODEL,
            "question": question,
        }

        try:
            response = requests.post(
                url=self.LLM_URL,
                headers=headers,
                data=json.dumps(
                    {
                        "model": self.LLM_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": [
                                    {"type": "text", "text": self.LLM_SYSTEM_PROMPT}
                                ],
                            },
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": question}],
                            },
                        ],
                    }
                ),
            )

            response.raise_for_status()

            logger.info(response.json())

            return {"message": response.json()["choices"][0]["message"]["content"]}
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            # Return an error message, but only say part of the error message
            return {
                "message": f"Sorry, I encontered an error thinking about your \
                    request: {str(e)[:100]}"
            }

    def webhook_request(self, question: str, context: dict) -> dict:
        """Send a request to the LLM API and return the response."""

        local_payload = {
            "token": self.LLM_KEY,
            "question": question,
        }

        payload = {**context, **local_payload}

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

    def ask(self, question: str, context: dict = {}) -> dict:
        """Ask a question and get a response."""
        if self.LLM_MODEL != "webhook":
            logger.info("Using API request")
            return self.api_request(question)
        else:
            logger.info("Using Webhook request")
            return self.webhook_request(question, context)


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
        speak_output = canned_response.get_launch_handler_phrase()

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
