from unittest import TestCase
from unittest.mock import mock_open, patch

from llm_intent.utils import CONFIG_FILE, CannedResponse, load_config


class TestLoadConfig(TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("llm_intent.utils.exists", return_value=True)
    def test_load_config_success(self, mock_exists, mock_open_file):
        """Test loading configuration successfully."""
        expected_config = {"key": "value"}
        config = load_config()
        self.assertEqual(config, expected_config)
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
