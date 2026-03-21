from src.vacancy_analyzer.vacancy import Vacancy


def test_vacancy_creation():
    """Тест корректного создания объекта Vacancy."""
    vac = Vacancy("Test", "http://test.com", None, "Test description")
    assert vac.title == "Test"
    assert vac.url == "http://test.com"
    assert vac.salary == "Зарплата не указана"
    assert vac.description == "Test description"


def test_vacancy_salary_validation():
    """Тест валидации зарплаты."""
    salary_data = {"from": 100000, "to": 150000, "currency": "RUR"}
    vac = Vacancy("Test", "http://test.com", salary_data, "")
    assert vac.salary == "100000 - 150000 RUR"

    salary_data_to = {"to": 150000, "currency": "RUR"}
    vac2 = Vacancy("Test2", "http://test2.com", salary_data_to, "")
    assert vac2.salary == "до 150000 RUR"

    vac3 = Vacancy("Test3", "http://test3.com", None, "")
    assert vac3.salary == "Зарплата не указана"


def test_vacancy_comparison():
    """Тест сравнения вакансий по зарплате."""
    vac_low = Vacancy("Low", "url1", {"from": 50000}, "")
    vac_high = Vacancy("High", "url2", {"from": 100000}, "")
    vac_no_salary = Vacancy("NoSalary", "url3", None, "")

    assert vac_high > vac_low
    assert vac_low < vac_high
    assert vac_no_salary < vac_low  # Вакансия без зарплаты считается с 0
    assert vac_low != vac_high


def test_cast_to_object_list():
    """Тест преобразования данных API в список объектов."""
    api_data = [
        {
            "name": "Test1",
            "alternate_url": "url1",
            "salary": {"from": 1000},
            "snippet": {"requirement": "desc1"},
        },
        {
            "name": "Test2",
            "url": "url2",
            "salary": None,
            "snippet": {},
        },  # Проверяем разные случаи
    ]
    vacancies = Vacancy.cast_to_object_list(api_data)
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Test1"
    assert vacancies[1].description == "Описание не предоставлено"
