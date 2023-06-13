# Date: 2023-5-13
# Author: Generated by GoCodeo.
import json
from unittest.mock import MagicMock, patch

import pytest

from autogpt.commands.audio_text import read_audio


class TestReadAudio:
    @patch("requests.post")
    def test_positive_read_audio(self, mock_post, config):
        # Positive Test
        audio_data = b"test_audio_data"
        mock_response = MagicMock()
        mock_response.content.decode.return_value = json.dumps(
            {"text": "Hello, world!"}
        )
        mock_post.return_value = mock_response

        config.huggingface_api_token = "testing-token"
        result = read_audio(audio_data, config)
        assert result == "The audio says: Hello, world!"
        mock_post.assert_called_once_with(
            f"https://api-inference.huggingface.co/models/{config.huggingface_audio_to_text_model}",
            headers={"Authorization": f"Bearer {config.huggingface_api_token}"},
            data=audio_data,
        )

    @patch("requests.post")
    def test_negative_read_audio(self, mock_post, config):
        # Negative Test
        audio_data = b"test_audio_data"
        mock_response = MagicMock()
        mock_response.content.decode.return_value = json.dumps({"text": ""})
        mock_post.return_value = mock_response
        config.huggingface_api_token = "testing-token"
        result = read_audio(audio_data, config)
        assert result == "The audio says: "
        mock_post.assert_called_once_with(
            f"https://api-inference.huggingface.co/models/{config.huggingface_audio_to_text_model}",
            headers={"Authorization": f"Bearer {config.huggingface_api_token}"},
            data=audio_data,
        )

    def test_error_read_audio(self, config):
        # Error Test
        config.huggingface_api_token = None
        with pytest.raises(ValueError):
            read_audio(b"test_audio_data", config)

    def test_edge_read_audio_empty_audio(self, config):
        # Edge Test
        with pytest.raises(ValueError):
            read_audio(b"", config)
