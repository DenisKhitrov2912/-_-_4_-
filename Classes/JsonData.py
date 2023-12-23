from abc import ABC, abstractmethod
import json
import os


class AppData(ABC):
    """Абстрактный класс на добавление данных"""

    @abstractmethod
    def __repr__(self):
        pass

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
    """Класс на обработку json-файлов из requests"""

    def __init__(self, class_object):
        self.class_object = class_object

    def __repr__(self):
        return f"Файл {self.class_object}"

    def data_add(self):
        with open('api_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.class_object.vacancies_list(), json_file, ensure_ascii=False, indent=4)
        print(f"Список вакансий успешно сохранен в api_data.json")

    def data_read(self):
        with open('api_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            count = True
            while count:
                user_input = input("""Введите цифру для выбора критериев отображения:
1: id вакансии, конечная зарплата, валюта, ссылка на вакансию;
2: название вакансии, конечная зарплата, город, ссылка на вакансию;
3: полный список. """)
                if user_input != "1" and user_input != "2" and user_input != "3":
                    print("Введите 1, 2 или 3!")
                else:
                    for dat in data:
                        print("")
                        if user_input == "1":
                            count = False
                            print(f'''"id вакансии": {dat["id вакансии"]}
"конечная зарплата": {dat["конечная зарплата"]}
"город": {dat["город"]}
"ссылка на вакансию": {dat["ссылка на вакансию"]}''')
                        elif user_input == "2":
                            count = False
                            print(f'''"название": {dat["название"]}
"конечная зарплата": {dat["конечная зарплата"]}
"валюта": {dat["валюта"]}
"ссылка на вакансию": {dat["ссылка на вакансию"]}''')
                        elif user_input == "3":
                            count = False
                            for k, v in dat.items():
                                print(f"{k}: {v}")
                        print("")

    def data_del(self):
        os.remove(os.path.join("api_data.json"))
        print("Файл 'api_data.json' успешно удален.")
