from unittest import TestCase
from unittest.mock import mock_open, patch

from llm_intent.utils import CONFIG_FILE, load_config


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
