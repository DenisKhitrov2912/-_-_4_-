import requests
import json

def get_api_data(api_url, params=None, limit=None):
    # Опционально добавьте параметры запроса, если они требуются
    if params is None:
        params = {}

    # Выполните запрос к API
    response = requests.get(api_url, params=params)

    # Проверьте успешность запроса
    if response.status_code == 200:
        # Разберите JSON-ответ
        data = response.json()

        # Примените ограничение по количеству результатов, если указано
        if limit is not None:
            data = data[:limit]

        # Сохраните данные в JSON-файл
        with open('api_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные успешно сохранены в api_data.json")
    else:
        print(f"Ошибка при выполнении запроса. Код: {response.status_code}")

# Пример использования
api_url = 'https://api.hh.ru/vacancies'
words = input()
params = {'text': words}
limit = None  # Укажите желаемое ограничение по количеству результатов

get_api_data(api_url, params=params, limit=limit)