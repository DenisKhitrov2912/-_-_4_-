from GetApiData import GetApiDataHeadHunter


class Vacancies:
    """Класс обработки вакансий"""

    def __init__(self, class_instance):
        self.salary = None
        self.class_instance = class_instance

    def __repr__(self):
        return f"Список вакансий объекта {self.class_instance}"

    def get_object_data(self):
        """Получение данных о вакансиях"""
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
        """Сортировка списка вакансий по максимальной зарплате"""
        vacancies_sorting = []
        vacancies_sorted = []
        salary_sorting = sorted(list(self.get_object_data().values()), reverse=True)
        for salary in salary_sorting:
            for key, value in self.get_object_data().items():
                if salary == value:
                    vacancies_sorting.append(key)
        for i in vacancies_sorting:
            if i not in vacancies_sorted:
                vacancies_sorted.append(i)
        return vacancies_sorted

    def vacancies_list(self):
        """Обработка отсортированных вакансий"""
        vacancies_list = []
        if isinstance(self.class_instance, GetApiDataHeadHunter):
            for vacancies in self.salary_comparison():
                vacancies_dict = {"id вакансии": vacancies.split(",  ")[0], "название": vacancies.split(",  ")[1],
                                  "начальная зарплата": vacancies.split(",  ")[2],
                                  "конечная зарплата": vacancies.split(",  ")[3],
                                  "валюта": vacancies.split(",  ")[4],
                                  "город": vacancies.split(",  ")[5], "работодатель": vacancies.split(",  ")[6],
                                  "ссылка на вакансию": vacancies.split(",  ")[7]}
                vacancies_list.append(vacancies_dict)
        else:
            for vacancies in self.salary_comparison():
                vacancies_dict = {"id вакансии": vacancies.split(",  ")[0], "название": vacancies.split(",  ")[1],
                                  "начальная зарплата": vacancies.split(",  ")[2],
                                  "конечная зарплата": vacancies.split(",  ")[3],
                                  "валюта": vacancies.split(",  ")[4], "город": vacancies.split(",  ")[5],
                                  "ссылка на вакансию": vacancies.split(",  ")[6]}
                vacancies_list.append(vacancies_dict)
        return vacancies_list
