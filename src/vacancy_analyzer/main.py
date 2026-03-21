from src.vacancy_analyzer.api import HeadHunterAPI
from src.vacancy_analyzer.json_saver import JSONSaver
from src.vacancy_analyzer.utils import (filter_vacancies, get_top_vacancies,
                                        get_vacancies_by_salary,
                                        print_vacancies, sort_vacancies)
from src.vacancy_analyzer.vacancy import Vacancy


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    Запрашивает параметры, получает данные, фильтрует, сортирует и выводит результат.
    """
    # 1. Получаем запрос у пользователя
    search_query = input(
        "Введите поисковый запрос (например, 'Python разработчик'): "
    ).strip()

    # 2. Создаем экземпляр API и получаем вакансии
    hh_api = HeadHunterAPI()
    print("Ищем вакансии...")
    hh_vacancies = hh_api.get_vacancies(search_query)

    # 3. Преобразуем сырые данные в список объектов
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(f"Найдено вакансий: {len(vacancies_list)}")

    # 4. Сохраняем все найденные вакансии в файл
    json_saver = JSONSaver()
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)
    print("Вакансии сохранены в файл.")

    # 5. Запрашиваем параметры для фильтрации и вывода
    top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
    filter_words = input(
        "Введите ключевые слова для фильтрации вакансий (через пробел): "
    ).split()
    salary_range = input(
        "Введите диапазон зарплат (например, '100000 - 150000'): "
    ).strip()

    # 6. Применяем фильтры и сортировку
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # 7. Выводим результат
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
