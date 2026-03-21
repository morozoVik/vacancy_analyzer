from unittest.mock import Mock, patch

from vacancy_analyzer.api import HeadHunterAPI


def test_hh_api_get_vacancies_success():
    """Тест успешного запроса к API HH"""
    api = HeadHunterAPI()
    mock_response = Mock()

    mock_response.json.return_value = {"items": [{"name": "Python dev"}]}
    mock_response.raise_for_status.return_value = None

    with patch("vacancy_analyzer.api.requests.get", return_value=mock_response):
        vacancies = api.get_vacancies("Python")

    assert vacancies == [{"name": "Python dev"}]
