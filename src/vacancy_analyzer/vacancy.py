class Vacancy:
    """
    Класс для представления вакансии.
    """

    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: dict | None, description: str):
        """
        Инициализатор объекта Вакансия.
        """
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description if description else "Описание не предоставлено"

    def __repr__(self):
        return f"Vacancy({self.title}, {self.url}, {self.salary})"

    def __str__(self):
        return f"{self.title} | {self.salary} | {self.url}"

    def _validate_salary(self, salary_data: dict | None) -> str:
        """
        Приватный метод для валидации и форматирования данных о зарплате.
        """
        if salary_data is None:
            return "Зарплата не указана"

        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")
        currency = salary_data.get("currency", "руб.")

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
        """
        if self.salary == "Зарплата не указана":
            return (0, self.salary)

        parts = self.salary.split()
        try:
            for part in parts:
                if part.isdigit():
                    return (int(part), self.salary)
        except (ValueError, AttributeError):
            pass
        return (0, self.salary)

    def __gt__(self, other) -> bool:
        """Больше (greater than) >"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты Vacancy")
        return self._get_salary_numeric()[0] > other._get_salary_numeric()[0]

    def __lt__(self, other) -> bool:
        """Меньше (less than) <"""
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
        """
        vacancies_list = []
        for vacancy_data in vacancies_data:
            title = vacancy_data.get("name")
            url = vacancy_data.get("alternate_url") or vacancy_data.get("url")
            salary = vacancy_data.get("salary")  # Это словарь!
            description = vacancy_data.get("snippet", {}).get("requirement", "")

            vacancy = cls(title, url, salary, description)
            vacancies_list.append(vacancy)

        return vacancies_list
