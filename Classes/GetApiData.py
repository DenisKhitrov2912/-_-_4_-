from abc import ABC, abstractmethod
import requests
import os


class GetApiData(ABC):
    """Абстрактный класс на получение данных по api"""

    @abstractmethod
    def get_api_data(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class GetApiDataHeadHunter(GetApiData):
    """Класс данных по api HeadHunter"""
    api = 'https://api.hh.ru/vacancies'
    salary = None

    @classmethod
    def __repr__(cls):
        return f"{cls.api}"

    @classmethod
    def get_api_data(cls):
        dict_vacancies = {}
        response = requests.get(cls.api, params={'text': input("Поиск по профессиям на сайте HeadHunter: ")})
        if response.status_code == 200:
            data = response.json()
            keys = ["items"]
            filtered_data = {k: data[k] for k in keys}
            while True:
                lim = input("Введите желаемое количество результатов выдачи (целое число) или нажмите Enter: ")
                if lim != '':
                    try:
                        limit = int(lim)
                        break
                    except ValueError:
                        print("Введите число!")
                        continue
                else:
                    limit = None
                    break
            if limit is not None:
                counter = 0
                while True:
                    for v in filtered_data["items"]:
                        if counter < limit:
                            counter += 1
                            if v['salary'] is None:
                                salary = "Зарплата не указана"
                                salary_to = ''
                                salary_currency = ''
                                cls.salary = 0
                            else:
                                if v['salary']['from'] is None:
                                    salary = ''
                                    cls.salary = v['salary']['to']
                                else:
                                    salary = f"от {v['salary']['from']}"
                                    cls.salary = v['salary']['to']
                                if v['salary']['to'] is None:
                                    salary_to = ''
                                    cls.salary = v['salary']['from']
                                else:
                                    salary_to = f"до {v['salary']['to']}"
                                    cls.salary = v['salary']['to']
                                salary_currency = v['salary']['currency']
                            if v["address"] is None:
                                city_address = "Город не указан"
                            else:
                                city_address = v["address"]["city"]
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']},  {v['name']},  {salary},  {salary_to},  {salary_currency},  {city_address},  {v['employer']['name']},  {link}"
                            dict_vacancies[key] = cls.salary
                    else:
                        break
            return dict_vacancies
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class GetApiDataSuperJob(GetApiData):
    """Класс данных по api SuperJob"""

    api = "https://api.superjob.ru/2.0/vacancies/"
    salary = None

    @classmethod
    def __repr__(cls):
        return f"{cls.api}"

    @classmethod
    def get_api_data(cls):
        dict_vacancies = {}
        param_word = input("Поиск по профессиям на сайте SuperJob: ")
        while True:
            lim = input("Введите желаемое количество результатов выдачи (целое число) или нажмите Enter: ")
            if lim != '':
                try:
                    limit_res = int(lim)
                    break
                except ValueError:
                    print("Введите число!")
            elif lim == "0":
                limit_res = None
                break
            else:
                limit_res = None
                break
        headers = {
            "X-Api-App-Id": os.getenv("SJ_API_KEY")
        }
        params = {
            "keyword": param_word,
            "count": limit_res
        }
        response = requests.get(cls.api, headers=headers, params=params)
        if response.status_code == 200:
            vacancies = response.json()["objects"]
            for vacancy in vacancies:
                if vacancy["payment_from"] == 0 and vacancy["payment_to"] == 0:
                    vacancy["payment_from"] = "зарплата"
                    vacancy["payment_to"] = "не указана"
                    cls.salary = 0
                    vacancy["currency"] = ''
                elif vacancy["payment_from"] == 0:
                    vacancy["payment_from"] = "до"
                    cls.salary = vacancy["payment_to"]
                elif vacancy["payment_to"] == 0:
                    cls.salary = vacancy["payment_from"]
                    vacancy["payment_from"] = f"от {vacancy['payment_from']}"
                    vacancy["payment_to"] = ''
                elif vacancy["payment_to"] != 0 and vacancy["payment_from"] != 0:
                    cls.salary = vacancy["payment_to"]
                key = f'{vacancy["id"]},  {vacancy["profession"]},  {vacancy["payment_from"]},  {vacancy["payment_to"]},  {vacancy["currency"]},  {vacancy["town"]["title"]},  {vacancy["link"]}'
                dict_vacancies[key] = cls.salary
            return dict_vacancies
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")
