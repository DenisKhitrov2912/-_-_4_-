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
        keys = ["items"]
        filtered_data = {k: data[k] for k in keys}
        counter = 0
        while True:
            for v in filtered_data["items"]:
                if counter < limit:
                    counter += 1
                    if v['salary'] is None:
                        salary = "Зарплата не указана"
                        salary_to = ''
                        salary_currency = ''
                    if v['salary'] is not None:
                        if v['salary']['from'] is None:
                            salary = ''
                        else:
                            salary = f"от {v['salary']['from']}"
                        if v['salary']['to'] is None:
                            salary_to = ''
                        else:
                            salary_to = f"до {v['salary']['to']}"
                        salary_currency = v['salary']['currency']
                    if v["address"] is None:
                        city_address = "Город не указан"
                    else:
                        city_address = v["address"]["city"]
                    print(v['id'], v['name'], salary, salary_to, salary_currency, v['alternate_url'], city_address, v['employer']['name'], v['employer']['alternate_url'])
            else:
                break


        # Сохраните данные в JSON-файл
        with open('api_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные успешно сохранены в api_data.json")
    else:
        print(f"Ошибка при выполнении запроса. Код: {response.status_code}")


# Пример использования
api_url = 'https://api.superjob.ru/vacancies'
api_key = "v3.r.138027493.de3940650341c40e73bce40058da6ac022f850d0.78bba7fe34dbe518fd654d088f8a1d465eec97f8"
words = input("Поиск по профессиям: ")
params = {'text': input("Поиск по профессиям: ")}
while True:
    try:
        limit = int(input("Введите количество результатов. Максимальное число результатов на странице - 20 "))
        break
    except ValueError:
        print("Введите число!")


get_api_data(api_url, params=params, limit=limit)
