from abc import ABC, abstractmethod

import json
import os
import requests


class GetApiData(ABC):

    @abstractmethod
    def get_api_data(self):
        pass


class GetApiDataHeadHunter(GetApiData):
    def __init__(self):
        self.api = 'https://api.hh.ru/vacancies'
        self.params = {'text': input("Поиск по профессиям: ")}
        while True:
            lim = input("Введите желаемое количество результатов выдачи (целое число) или нажмите Enter: ")
            if lim != '':
                try:
                    self.limit = int(lim)
                    break
                except ValueError:
                    print("Введите число!")
            else:
                self.limit = None
                break

    def get_api_data(self):

        # Выполните запрос к API
        response = requests.get(self.api, params=self.params)

        # Проверьте успешность запроса
        if response.status_code == 200:
            # Разберите JSON-ответ
            data = response.json()
            keys = ["items"]
            filtered_data = {k: data[k] for k in keys}
            if self.limit is not None:
                counter = 0
                while True:
                    for v in filtered_data["items"]:
                        if counter < self.limit:
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
                            print(v['id'], v['name'], salary, salary_to, salary_currency, v['alternate_url'], city_address,
                                  v['employer']['name'], v['employer']['alternate_url'])
                    else:
                        break

            # Сохраните данные в JSON-файл
            with open('api_data.json', 'a', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Данные успешно сохранены в api_data.json")
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class GetApiDataSuperJob(GetApiData):

    def __init__(self):
        self.keyword = input("Поиск по профессиям: ")
        while True:
            lim = input("Введите желаемое количество результатов выдачи (целое число) или нажмите Enter: ")
            if lim != '':
                try:
                    self.limit = int(lim)
                    break
                except ValueError:
                    print("Введите число!")
            elif lim == "0":
                self.limit = None
                break
            else:
                self.limit = None
                break

    def get_api_data(self):
        api_url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {
            "X-Api-App-Id": os.getenv("SJ_API_KEY")
        }

        params = {
            "keyword": self.keyword,
            "count": self.limit
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            vacancies = response.json()["objects"]
            with open('api_data.json', 'a', encoding='utf-8') as json_file:
                json.dump(vacancies, json_file, ensure_ascii=False, indent=4)
            print(f"Данные успешно сохранены в api_data.json")
            for vacancy in vacancies:
                if vacancy["payment_from"] == 0 and vacancy["payment_to"] == 0:
                    vacancy["payment_from"] = "зарплата"
                    vacancy["payment_to"] = "не указана"
                    vacancy["currency"] = ''
                if vacancy["payment_from"] == 0:
                    vacancy["payment_from"] = "до"
                if vacancy["payment_to"] == 0:
                    vacancy["payment_from"] = f"от {vacancy['payment_from']}"
                    vacancy["payment_to"] = ''
                print(
                    f'{vacancy["id"]}, {vacancy["profession"]}, {vacancy["payment_from"]} {vacancy["payment_to"]} {vacancy["currency"]}, {vacancy["town"]["title"]}, ссылка: {vacancy["client"]["link"]}')
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class TreatmentData:
    def __init__(self, data_json, file_name):
        self.data_json = data_json
        self.file_name = file_name

    def append_data(self):
        with open(self.file_name, 'a', encoding='utf-8') as json_file:
            json.dump(GetApiData.get_api_data, json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в api_data.json")


a=GetApiDataHeadHunter()
a.get_api_data()