class Vacancy:
    """
    Класс для представления вакансии.
    """
    # __slots__ для экономии памяти и ограничения атрибутов
    __slots__ = ('title', 'url', 'salary', 'description', '_validate_salary')

    def __init__(self, title: str, url: str, salary: dict | None, description: str):
        """
        Инициализатор объекта Вакансия.
        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Словарь с данными о зарплате от API HH
        :param description: Описание/требования вакансии
        """
        self.title = title
        self.url = url
        # Зарплата передается в виде сложного объекта, валидируем и преобразуем ее
        self.salary = self._validate_salary(salary)
        self.description = description if description else "Описание не предоставлено"

    def __repr__(self):
        return f"Vacancy({self.title}, {self.url}, {self.salary})"

    def __str__(self):
        return f'{self.title} | {self.salary} | {self.url}'

    def _validate_salary(self, salary_data: dict | None) -> str:
        """
        Приватный метод для валидации и форматирования данных о зарплате.
        :param salary_data: Словарь с данными о зарплате от API HH
        :return: Отформатированная строка с зарплатой или "Зарплата не указана"
        """
        if salary_data is None:
            return "Зарплата не указана"

        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency', 'руб.')

        # Логика обработки разных случаев
        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return "Зарплата не указана"

    def _get_salary_numeric(self) -> tuple:
        """
        Приватный метод для преобразования строки зарплаты в числовое значение для сравнения.
        Использует нижнюю границу (from) или 0, если ее нет.
        :return: Кортеж (числовое значение для сравнения, оригинальная строка)
        """
        # Вспомогательный метод для методов сравнения
        if self.salary == "Зарплата не указана":
            return (0, self.salary)

        # Очень наивный парсинг. Можно улучшить с помощью регулярных выражений.
        parts = self.salary.split()
        try:
            # Пытаемся найти первое число в строке
            for part in parts:
                if part.isdigit():
                    return (int(part), self.salary)
        except (ValueError, AttributeError):
            pass
        return (0, self.salary)

    # Методы сравнения (магические методы)
    def __gt__(self, other) -> bool:
        """Больше (greater than) > """
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self._get_salary_numeric()[0] > other._get_salary_numeric()[0]

    def __lt__(self, other) -> bool:
        """Меньше (less than) < """
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self._get_salary_numeric()[0] < other._get_salary_numeric()[0]

    def __ge__(self, other) -> bool:
        """Больше или равно (greater or equal) >="""
        return self > other or self == other

    def __le__(self, other) -> bool:
        """Меньше или равно (less or equal) <="""
        return self < other or self == other

    def __eq__(self, other) -> bool:
        """Равно (equal) =="""
        if not isinstance(other, Vacancy):
            return False
        return self._get_salary_numeric()[0] == other._get_salary_numeric()[0]

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list[dict]) -> list:
        """
        Классовый метод для преобразования списка словарей (из API) в список объектов Vacancy.
        :param vacancies_data: Список словарей с данными о вакансиях
        :return: Список экземпляров класса Vacancy
        """
        vacancies_list = []
        for vacancy_data in vacancies_data:
            # Извлекаем нужные данные из структуры HH API
            title = vacancy_data.get('name')
            url = vacancy_data.get('alternate_url') or vacancy_data.get('url')
            salary = vacancy_data.get('salary')  # Это словарь!
            # Берем snippet или требуемый опыт, если описания нет
            description = vacancy_data.get('snippet', {}).get('requirement', '')

            # Создаем объект и добавляем в список
            vacancy = cls(title, url, salary, description)
            vacancies_list.append(vacancy)

        return vacancies_list