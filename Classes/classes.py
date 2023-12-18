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
        self.params = {'text': input("Поиск по профессиям на сайте HeadHunter: ")}
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
            vacancies = response.json()
            return vacancies
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class GetApiDataSuperJob(GetApiData):

    def __init__(self):
        self.keyword = input("Поиск по профессиям на сайте SuperJob: ")
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
            return vacancies

        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class Vacancies:
    def __init__(self, class_instance):
        self.salary = None
        self.class_instance = class_instance

    def get_object_data(self):
        dict_vacations = {}
        if isinstance(self.class_instance, GetApiDataHeadHunter):
            data = self.class_instance.get_api_data()
            keys = ["items"]
            filtered_data = {k: data[k] for k in keys}
            if self.class_instance.limit is not None:
                counter = 0
                while True:
                    for v in filtered_data["items"]:
                        if counter < self.class_instance.limit:
                            counter += 1
                            if v['salary'] is None:
                                salary = "Зарплата не указана"
                                salary_to = ''
                                salary_currency = ''
                                self.salary = 0
                            else:
                                if v['salary']['from'] is None:
                                    salary = ''
                                    self.salary = v['salary']['to']
                                else:
                                    salary = f"от {v['salary']['from']}"
                                    self.salary = v['salary']['to']
                                if v['salary']['to'] is None:
                                    salary_to = ''
                                    self.salary = v['salary']['from']
                                else:
                                    salary_to = f"до {v['salary']['to']}"
                                    self.salary = v['salary']['to']
                                salary_currency = v['salary']['currency']
                            if v["address"] is None:
                                city_address = "Город не указан"
                            else:
                                city_address = v["address"]["city"]
                            key = f"{v['id']}, {v['name']}, {salary} {salary_to} {salary_currency}, {v['alternate_url']}, {city_address}, {v['employer']['name']}, {v['employer']['alternate_url']}"
                            dict_vacations[key] = self.salary
                    else:
                        break
            return dict_vacations
        else:
            for vacancy in self.class_instance.get_api_data():
                if vacancy["payment_from"] == 0 and vacancy["payment_to"] == 0:
                    vacancy["payment_from"] = "зарплата"
                    vacancy["payment_to"] = "не указана"
                    self.salary = 0
                    vacancy["currency"] = ''
                elif vacancy["payment_from"] == 0:
                    vacancy["payment_from"] = "до"
                    self.salary = vacancy["payment_to"]
                elif vacancy["payment_to"] == 0:
                    self.salary = vacancy["payment_from"]
                    vacancy["payment_from"] = f"от {vacancy['payment_from']}"
                    vacancy["payment_to"] = ''
                elif vacancy["payment_to"] != 0 and vacancy["payment_from"] != 0:
                    self.salary = vacancy["payment_to"]
                key = f'{vacancy["id"]}, {vacancy["profession"]}, {vacancy["payment_from"]} {vacancy["payment_to"]} {vacancy["currency"]}, {vacancy["town"]["title"]}, ссылка: {vacancy["client"]["link"]}'
                dict_vacations[key] = self.salary
            return dict_vacations

    def salary_comparison(self):
        vacations_sorted = []
        salary_sorting = sorted(list(self.get_object_data().values()), reverse=True)
        for salary in salary_sorting:
            for key, value in self.get_object_data().items():
                if salary == value:
                    vacations_sorted.append(key)
        return vacations_sorted


class AppData(ABC):

    @abstractmethod
    def data_add(self):
        pass

    @abstractmethod
    def data_read(self):
        pass

    @abstractmethod
    def data_del(self):
        pass


class JsonData(AppData):
    def __init__(self, class_object):
        self.class_object = class_object

    def data_add(self):
        with open('api_data.json', 'a', encoding='utf-8') as json_file:
            json.dump(self.class_object.get_api_data(), json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в api_data.json")

    def data_read(self):
        with open('api_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def data_del(self):
        os.remove(os.path.join("api_data.json"))
        print("Файл 'api_data.json' успешно удален.")


b = GetApiDataHeadHunter()
c = Vacancies(b)
print(c.salary_comparison())
