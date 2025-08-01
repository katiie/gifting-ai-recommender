# flake8:noqa
import unittest
from src.app import AIClient
from unittest.mock import Mock, patch, mock_open, MagicMock
import json


class AIClientTest(unittest.TestCase):
    def setUp(self):
        self.ai_client = AIClient("OPENAI_API_KEY")

    def test_get_image_success(self):
        with patch.object(self.ai_client.client.images, 'generate') as mock_generate:
            # Setup mock response
            mock_response = Mock()
            mock_data_item = Mock()
            mock_data_item.url = "https://fake.image.url/generated.png"
            mock_response.data = [mock_data_item]
            mock_generate.return_value = mock_response

            result = self.ai_client.get_image("A beautiful landscape")
            self.assertEqual(result, "https://fake.image.url/generated.png")

    def test_get_image_failure(self):
        with patch.object(self.ai_client.client.images, 'generate') as mock_generate:
            # Setup mock response
            mock_response = Mock()
            mock_response.data = []
            mock_generate.return_value = mock_response

            result = self.ai_client.get_image("A beautiful landscape")
            self.assertIsNone(result)

    def test_get_gift_ideas_success(self):
        # chat.completions.create
        with patch.object(self.ai_client.client.chat.completions, 'create') as mock_create:
            with patch.object(self.ai_client.client.images, 'generate') as mock_generate:
                # Setup mock response
                sample_json_response = {
                    "gift_recommendations": [
                        {
                            "name": "Wine Opender",
                            "summary": "A fancy wine opender based on the given preference",
                            "image": "sample url"
                        },
                        {
                            "name": "Wine Opener",
                            "summary": "A fancy wine opender based on the given preference",
                            "image": "sample url"
                        }
                    ]
                }
                # response.choices[0].message.content
                mock_response = Mock()
                mock_response_item = Mock()
                mock_response_content = Mock()
                mock_response_content.content = json.dumps(sample_json_response)
                mock_response_item.message = mock_response_content
                mock_response_item.finish_reason = "stop"
                mock_response.choices = [mock_response_item]
                mock_create.return_value = mock_response

                g_mock_response = Mock()
                g_mock_data_item = Mock()
                g_mock_data_item.url = "https://fake.image.url/generated.png"
                g_mock_response.data = [g_mock_data_item]
                mock_generate.return_value = g_mock_response


                result = self.ai_client.get_gift_ideas(2,"friend",100,"Canada","Art", "")
                mock_create.assert_called_once()
                mock_generate.assert_called

                self.assertIsNotNone(result)
                self.assertEqual(len(result), 2)

    def test_get_gift_ideas_failure(self):
        # chat.completions.create
        with patch.object(self.ai_client.client.chat.completions, 'create') as mock_create:
            with patch.object(self.ai_client.client.images, 'generate') as mock_generate:
                # Setup mock response
                sample_json_response = {
                    "error": "pune intended"
                }
                # response.choices[0].message.content
                mock_response = Mock()
                mock_response_item = Mock()
                mock_response_content = Mock()
                mock_response_content.content = json.dumps(sample_json_response)
                mock_response_item.message = mock_response_content
                mock_response_item.finish_reason = "stop"
                mock_response.choices = [mock_response_item]
                mock_create.return_value = mock_response

                g_mock_response = Mock()
                g_mock_data_item = Mock()
                g_mock_data_item.url = "https://fake.image.url/generated.png"
                g_mock_response.data = [g_mock_data_item]
                mock_generate.return_value = g_mock_response


                result = self.ai_client.get_gift_ideas(2,"friend",100,"Canada","Art", "")
                mock_create.assert_called_once()
                mock_generate.assert_called

                self.assertIsNone(result)
