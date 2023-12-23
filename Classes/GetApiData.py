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
                    continue
            else:
                self.limit = None
                break

    def __repr__(self):
        return f"GetApiDataHeadHunter, {self.params}, {self.limit}"

    def get_api_data(self):
        response = requests.get(self.api, params=self.params)
        if response.status_code == 200:
            vacancies = response.json()
            return vacancies
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")


class GetApiDataSuperJob(GetApiData):
    """Класс данных по api SuperJob"""

    def __init__(self):
        self.api = "https://api.superjob.ru/2.0/vacancies/"
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

    def __repr__(self):
        return f"GetApiDataSuperJob, {self.keyword}, {self.limit}"

    def get_api_data(self):
        headers = {
            "X-Api-App-Id": os.getenv("SJ_API_KEY")
        }
        params = {
            "keyword": self.keyword,
            "count": self.limit
        }
        response = requests.get(self.api, headers=headers, params=params)
        if response.status_code == 200:
            vacancies = response.json()["objects"]
            return vacancies
        else:
            print(f"Доступ к сайту не получен! Код ошибки: {response.status_code}")
