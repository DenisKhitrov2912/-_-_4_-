import requests
import json

def get_api_data():
    api_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": "v3.r.138027493.de3940650341c40e73bce40058da6ac022f850d0.78bba7fe34dbe518fd654d088f8a1d465eec97f8"
    }

    params = {
        "keyword": "python",
        "count": 5
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        vacancies = response.json()["objects"]
        with open('api_data.json', 'w', encoding='utf-8') as json_file:
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
            print(f'{vacancy["id"]}, {vacancy["profession"]}, {vacancy["payment_from"]} {vacancy["payment_to"]} {vacancy["currency"]}, {vacancy["town"]["title"]}, ссылка: {vacancy["client"]["link"]}')
    else:
        print("Error fetching vacancies from Superjob API")
        return []

get_api_data()


def vacancies_dict(self):
    vacancies_dict = {}
    if isinstance(self.class_instance, GetApiDataHeadHunter):
        for vacancies in self.salary_comparison():
            vacancies_dict["id"] = vacancies.split(", ")[0]
            vacancies_dict["name"] = vacancies.split(", ")[1]
            vacancies_dict["start_salary"] = vacancies.split(", ")[2]
            vacancies_dict["end_salary"] = vacancies.split(", ")[3]
            vacancies_dict["currency"] = vacancies.split(", ")[4]
            vacancies_dict["link"] = vacancies.split(", ")[5]
            vacancies_dict["town"] = vacancies.split(", ")[6]
            vacancies_dict["employer"] = vacancies.split(", ")[7]
            vacancies_dict["link_employer"] = vacancies.split(", ")[8]
    else:
        for vacancies in self.salary_comparison():
            vacancies_dict["id"] = vacancies.split(", ")[0]
            vacancies_dict["name"] = vacancies.split(", ")[1]
            vacancies_dict["start_salary"] = vacancies.split(", ")[2]
            vacancies_dict["end_salary"] = vacancies.split(", ")[3]
            vacancies_dict["currency"] = vacancies.split(", ")[4]
            vacancies_dict["town"] = vacancies.split(", ")[5]
            vacancies_dict["link"] = vacancies.split(", ")[6]
    return vacancies_dict

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
            json.dump(self.class_object.vacancies_dict, json_file)
        print(f"Данные успешно сохранены в api_data.json")

    def data_read(self):
        with open('api_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def data_del(self):
        os.remove(os.path.join("api_data.json"))
        print("Файл 'api_data.json' успешно удален.")

    def get_object_data(self):
        list_vacations = []
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
                            link = f'https://hh.ru/vacancy/{v["id"]}'
                            key = f"{v['id']},  {v['name']},  {salary},  {salary_to},  {salary_currency},  {city_address},  {v['employer']['name']},  {link}"
                            dict_vacations[key] = self.salary
                    else:
                        break
            list_vacations.append(dict_vacations)
            return list_vacations
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
                dict_vacations[key] = self.salary
            list_vacations.append(dict_vacations)
            return list_vacations

    def salary_comparison(self):
        for salary in self.get_object_data():
            for key, value in salary.items():
                if value == self.salary:
                    vacations_sorting.append(self.get_object_data().items())
        for salary in vacations_sorted:
            if
