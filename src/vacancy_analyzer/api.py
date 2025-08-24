from abc import ABC, abstractmethod
import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, search_query: str):
        """
        Абстрактный метод для получения вакансий по поисковому запросу.
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для подключения к API HeadHunter и получения вакансий.
    """
    _BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self._params = {
            'per_page': 100,  # Количество вакансий на странице (макс. 100)
            'area': 113,      # Код региона (113 - Россия)
            'text': None
        }

    def _get_data(self, url, params=None):
        """
        Приватный метод для отправки GET-запроса к API и обработки ответа.
        """
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, search_query: str):
        """
        Публичный метод для получения вакансий по ключевому слову.
        """
        params = self._params.copy()
        params['text'] = search_query

        data = self._get_data(self._BASE_URL, params=params)

        return data.get('items', [])