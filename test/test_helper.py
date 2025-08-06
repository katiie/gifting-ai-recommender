import unittest
from unittest.mock import patch, MagicMock
from src.helpers import get_countries


class TestGetCountries(unittest.TestCase):
    @patch("src.helpers.requests.get")
    def test_get_countries_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "1": {"country": "Canada"},
                "2": {"country": "Nigeria"},
                "3": {"country": "Ghana"}
            }
        }
        mock_get.return_value = mock_response
        get_countries.cache_clear()

        result = get_countries()
        self.assertEqual(result, ['Canada', 'Ghana', 'Nigeria'])

    def test_get_countries_cache_confirm(self):
        get_countries.cache_clear()
        with patch("src.helpers.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": {
                    "1": {"country": "Canada"},
                    "2": {"country": "Nigeria"},
                    "3": {"country": "Ghana"}
                }
            }
            mock_get.return_value = mock_response

            result1 = get_countries()
            self.assertEqual(result1, ['Canada', 'Ghana', 'Nigeria'])
            mock_get.assert_called_once()

        with patch("src.helpers.requests.get") as mock_get2:
            result2 = get_countries()
            self.assertEqual(result2, ['Canada', 'Ghana', 'Nigeria'])
            mock_get2.assert_not_called()

    @patch("src.helpers.requests.get")
    def test_get_countries_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        get_countries.cache_clear()

        result = get_countries()
        self.assertIsNone(result)
