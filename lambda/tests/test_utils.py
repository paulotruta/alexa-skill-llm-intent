import json
from unittest import TestCase
from unittest.mock import mock_open, patch

from llm_intent.utils import CONFIG_FILE, DEFAULT_PROMPT, CannedResponse, load_config
from pydantic import ValidationError


class TestLoadConfig(TestCase):
    MINIMUM_CONFIG = {
        "llm_url": "http://example.org",
        "llm_key": "llm_key",
        "llm_model": "llm_model",
    }

    COMPLETE_CONFIG = {
        "llm_url": "http://example.org",
        "llm_key": "llm_key",
        "llm_model": "llm_model",
        "llm_system_prompt": "llm_prompt",
    }

    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps(COMPLETE_CONFIG)
    )
    @patch("llm_intent.utils.exists", return_value=True)
    def test_load_config_success(self, mock_exists, mock_open_file):
        """Test loading configuration successfully."""
        config = load_config()
        self.assertEqual(config.llm_url, TestLoadConfig.COMPLETE_CONFIG["llm_url"])
        self.assertEqual(config.llm_key, TestLoadConfig.COMPLETE_CONFIG["llm_key"])
        self.assertEqual(config.llm_model, TestLoadConfig.COMPLETE_CONFIG["llm_model"])
        self.assertEqual(
            config.llm_system_prompt,
            TestLoadConfig.COMPLETE_CONFIG["llm_system_prompt"],
        )
        mock_exists.assert_called_once_with(CONFIG_FILE)
        mock_open_file.assert_called_once_with(CONFIG_FILE)

    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps(MINIMUM_CONFIG)
    )
    @patch("llm_intent.utils.exists", return_value=True)
    def test_load_config_default_prompt(self, mock_exists, mock_open_file):
        """Test loading configuration with default successfully."""
        config = load_config()
        self.assertEqual(config.llm_url, TestLoadConfig.COMPLETE_CONFIG["llm_url"])
        self.assertEqual(config.llm_key, TestLoadConfig.COMPLETE_CONFIG["llm_key"])
        self.assertEqual(config.llm_model, TestLoadConfig.COMPLETE_CONFIG["llm_model"])
        self.assertEqual(config.llm_system_prompt, DEFAULT_PROMPT)
        mock_exists.assert_called_once_with(CONFIG_FILE)
        mock_open_file.assert_called_once_with(CONFIG_FILE)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({}))
    @patch("llm_intent.utils.exists", return_value=True)
    def test_load_config_missing_fields(self, mock_exists, mock_open_file):
        """Test loading configuration missing fields."""
        with self.assertRaises(ValidationError):
            load_config()
        mock_exists.assert_called_once_with(CONFIG_FILE)
        mock_open_file.assert_called_once_with(CONFIG_FILE)

    @patch("llm_intent.utils.exists", return_value=False)
    def test_load_config_file_not_found(self, mock_exists):
        """Test loading configuration when file does not exist."""
        with self.assertRaises(ValueError) as context:
            load_config()
        self.assertEqual(str(context.exception), "Config file does not exist")
        mock_exists.assert_called_once_with(CONFIG_FILE)


class TestCannedResponse(TestCase):
    def test_invalid_locale(self):
        canned_response = CannedResponse("invalid_locale")
        self.assertEqual(canned_response.locale, "en-US")

    def test_get_help_phrase(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_help_phrase(), str)

    def test_get_no_message_phrase(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_no_message_phrase(), str)

    def test_get_goodbye_phrase(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_goodbye_phrase(), str)

    def test_get_reprompt_phrase(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_fallback_handler_phrase(), str)

    def test_get_launch_handler_phrase(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_launch_handler_phrase(), str)

    def test_get_fallback_handler_phrasee(self):
        canned_response = CannedResponse("en-US")
        assert isinstance(canned_response.get_fallback_handler_phrase(), str)
