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
params = {'text': input("Поиск по профессиям: ")}
while True:
    try:
        limit = int(input("Введите количество результатов. Максимальное число результатов на странице - 20 "))
        break
    except ValueError:
        print("Введите число!")


get_api_data(api_url, params=params, limit=limit)

class Vacancies:
    def __init__(self, class_instance):
        self.salary = None
        self.class_instance = class_instance

    def get_object_data(self):
        dict_vacancies = {}
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
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']},  {v['name']},  {salary},  {salary_to},  {salary_currency},  {city_address},  {v['employer']['name']},  {link}"
                            dict_vacancies[key] = self.salary
                    else:
                        break
            return dict_vacancies
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
                key = f'{vacancy["id"]},  {vacancy["profession"]},  {vacancy["payment_from"]},  {vacancy["payment_to"]},  {vacancy["currency"]},  {vacancy["town"]["title"]},  {vacancy["link"]}'
                dict_vacancies[key] = self.salary
            return dict_vacancies

    def salary_comparison(self):
        vacancies_sorted = []
        list_values = sorted(list(self.get_object_data().values()), reverse=True)
        for val in list_values:
            for key, value in self.get_object_data().items():
                if val == value:
                    vacancies_sorted.append(key)
            return vacancies_sorted

        #for key in self.get_object_data().keys():
            #for value in list_values:
                #if value == self.salary:
                    #vacancies_sorted.append(key)
            #return vacancies_sorted

    def vacancies_list(self):
        vacancies_list = []
        if isinstance(self.class_instance, GetApiDataHeadHunter):
            for vacancies in self.salary_comparison():
                vacancies_dict = {"id": vacancies.split(",  ")[0], "name": vacancies.split(",  ")[1],
                                  "start_salary": vacancies.split(",  ")[2], "end_salary": vacancies.split(",  ")[3],
                                  "currency": vacancies.split(",  ")[4],
                                  "town": vacancies.split(",  ")[5], "employer": vacancies.split(",  ")[6],
                                  "link": vacancies.split(",  ")[7]}
                vacancies_list.append(vacancies_dict)
        else:
            for vacancies in self.salary_comparison():
                vacancies_dict = {"id": vacancies.split(",  ")[0], "name": vacancies.split(",  ")[1],
                                  "start_salary": vacancies.split(",  ")[2], "end_salary": vacancies.split(",  ")[3],
                                  "currency": vacancies.split(",  ")[4], "town": vacancies.split(",  ")[5],
                                  "link": vacancies.split(",  ")[6]}
                vacancies_list.append(vacancies_dict)
        return vacancies_list


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
        with open('api_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.class_object.vacancies_list(), json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в api_data.json")

    def data_read(self):
        with open('api_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def data_del(self):
        os.remove(os.path.join("api_data.json"))
        print("Файл 'api_data.json' успешно удален.")


b = GetApiDataSuperJob()
c = Vacancies(b)
print(c.salary_comparison())
#d = JsonData(c)
#d.data_add()
