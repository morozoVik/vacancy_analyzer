import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .vacancy import Vacancy


class Storage(ABC):
    """
    Абстрактный класс для работы с хранилищем данных (файл, БД и т.д.).
    Определяет обязательные методы для добавления, получения и удаления данных.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Any):
        """Абстрактный метод для добавления вакансии в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict) -> list:
        """Абстрактный метод для получения вакансий из хранилища по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Any):
        """Абстрактный метод для удаления вакансии из хранилища"""
        pass


class JSONSaver(Storage):
    """
    Класс для сохранения и загрузки данных о вакансиях в JSON-файл.
    Наследуется от абстрактного класса Storage.
    """

    def __init__(self, file_name: str = "vacancies.json"):
        """
        :param file_name: Имя JSON-файла для сохранения данных
        """
        self._file_name = Path("data") / file_name  # Сохраняем в папку data
        self._file_name.parent.mkdir(exist_ok=True)
        if not self._file_name.exists():
            self._file_name.write_text("[]", encoding="utf-8")

    def _read_file(self) -> list:
        """Приватный метод для чтения всего файла и возврата списка данных."""
        with open(self._file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_file(self, data: list):
        """Приватный метод для записи списка данных в файл."""
        with open(self._file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавляет одну вакансию в файл, если ее там еще нет.
        """
        data = self._read_file()
        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
        }

        for vac in data:
            if vac["url"] == vacancy_dict["url"]:
                return

        data.append(vacancy_dict)
        self._write_file(data)

    def get_vacancies(self, criteria: dict = None) -> list:
        """
        Возвращает список вакансий, отфильтрованных по критериям.
        """
        if criteria is None:
            criteria = {}

        all_vacancies = self._read_file()
        filtered_vacancies = all_vacancies

        if "salary_min" in criteria:
            filtered_vacancies = [
                v for v in filtered_vacancies if v["salary"] != "Зарплата не указана"
            ]

        if "keywords" in criteria:
            keywords = criteria["keywords"]
            filtered_vacancies = [
                v
                for v in filtered_vacancies
                if all(
                    keyword.lower() in v["description"].lower() for keyword in keywords
                )
            ]

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Удаляет вакансию из файла по совпадению ссылки.
        """
        data = self._read_file()
        # Оставляем в списке только те вакансии, ссылка которых не совпадает с удаляемой
        new_data = [v for v in data if v["url"] != vacancy.url]
        self._write_file(new_data)
