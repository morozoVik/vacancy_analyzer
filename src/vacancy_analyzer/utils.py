from typing import List

from .vacancy import Vacancy


def filter_vacancies(
    vacancies_list: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрует список вакансий по ключевым словам в описании.
    """
    if not filter_words:
        return vacancies_list

    filtered_vacancies = []
    for vacancy in vacancies_list:
        if any(word.lower() in vacancy.description.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(
    vacancies_list: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.
    """
    if not salary_range:
        return vacancies_list

    try:
        salaries = salary_range.split("-")
        min_desired = int(salaries[0].strip())
        max_desired = int(salaries[1].strip()) if len(salaries) > 1 else float("inf")
    except (ValueError, IndexError):
        print(
            "Неверный формат диапазона зарплат. Используйте, например: '100000 - 150000'"
        )
        return vacancies_list

    ranged_vacancies = []
    for vacancy in vacancies_list:
        salary_num, _ = vacancy._get_salary_numeric()
        if min_desired <= salary_num <= max_desired:
            ranged_vacancies.append(vacancy)

    return ranged_vacancies


def sort_vacancies(vacancies_list: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты.
    """
    return sorted(vacancies_list, reverse=True)


def get_top_vacancies(vacancies_list: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий из отсортированного списка.
    """
    return vacancies_list[:top_n]


def print_vacancies(vacancies_list: List[Vacancy]):
    """
    Выводит отформатированный список вакансий в консоль.
    """
    if not vacancies_list:
        print("По вашему запросу вакансий не найдено.")
        return

    print("\n" + "=" * 50)
    for i, vacancy in enumerate(vacancies_list, 1):
        print(f"{i}. {vacancy.title}")
        print(f"   Зарплата: {vacancy.salary}")
        print(f"   Ссылка: {vacancy.url}")
        print(f"   Требования: {vacancy.description[:100]}...")  # Обрезаем описание
        print("-" * 50)
