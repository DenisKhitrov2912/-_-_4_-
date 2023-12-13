from abc import ABC, abstractmethod
import requests
import json
import os


class GetApiData(ABC):
    @abstractmethod
    def get_api_data(self):
        pass


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


a = GetApiDataSuperJob()
a.get_api_data()