from Classes.GetApiData import GetApiDataHeadHunter, GetApiDataSuperJob


class Vacancies:
    """Класс обработки вакансий"""

    def __init__(self):
        self.vacancies_sorting = []
        self.vacancies_sorted = []
        self.vacancies_list = []

    def __repr__(self):
        return f"""Конечный список вакансий: {self.vacancies_list}
Сортируемые вакансии: {self.vacancies_sorting}
Отсортированные вакансии: {self.vacancies_sorted}"""

    def salary_comparison_hh(self):
        """Сортировка списка вакансий по максимальной зарплате"""
        vacancies = GetApiDataHeadHunter.get_api_data()
        salary_sorting = sorted(list(vacancies.values()), reverse=True)
        for salary in salary_sorting:
            for key, value in vacancies.items():
                if salary == value:
                    self.vacancies_sorting.append(key)
        for i in self.vacancies_sorting:
            if i not in self.vacancies_sorted:
                self.vacancies_sorted.append(i)
        return self.vacancies_sorted

    def salary_comparison_sj(self):
        """Сортировка списка вакансий по максимальной зарплате"""
        vacancies = GetApiDataSuperJob.get_api_data()
        salary_sorting = sorted(list(vacancies.values()), reverse=True)
        for salary in salary_sorting:
            for key, value in vacancies.items():
                if salary == value:
                    self.vacancies_sorting.append(key)
        for i in self.vacancies_sorting:
            if i not in self.vacancies_sorted:
                self.vacancies_sorted.append(i)
        return self.vacancies_sorted

    def vacancies_list_hh(self):
        """Обработка отсортированных вакансий hh"""
        for vacancies in self.salary_comparison_hh():
            vacancies_dict = {"id вакансии": vacancies.split(",  ")[0], "название": vacancies.split(",  ")[1],
                              "начальная зарплата": vacancies.split(",  ")[2],
                              "конечная зарплата": vacancies.split(",  ")[3],
                              "валюта": vacancies.split(",  ")[4],
                              "город": vacancies.split(",  ")[5], "работодатель": vacancies.split(",  ")[6],
                              "ссылка на вакансию": vacancies.split(",  ")[7]}
            self.vacancies_list.append(vacancies_dict)
        return self.vacancies_list

    def vacancies_list_sj(self):
        """Обработка отсортированных вакансий sj"""
        for vacancies in self.salary_comparison_sj():
            vacancies_dict = {"id вакансии": vacancies.split(",  ")[0], "название": vacancies.split(",  ")[1],
                              "начальная зарплата": vacancies.split(",  ")[2],
                              "конечная зарплата": vacancies.split(",  ")[3],
                              "валюта": vacancies.split(",  ")[4], "город": vacancies.split(",  ")[5],
                              "ссылка на вакансию": vacancies.split(",  ")[6]}
            self.vacancies_list.append(vacancies_dict)
        return self.vacancies_list
