#from Classes.GetApiData import GetApiDataHeadHunter, GetApiDataSuperJob
from Vacancies import Vacancies
from JsonData import JsonData


def user_function():
    print("Привет! Предлагаю поискать работу.")

    while True:
        user_input = input("Какой сайт Вас интересует? Нажмите 1, если HeadHunter, 2, если Superjob, 0 - выход: ")
        if user_input == "1":
            vacancies = Vacancies()
            vac_list = vacancies.vacancies_list_hh()
            json_data = JsonData()
            json_data.add(vac_list)
            second_user_input = input("Хотите вывести результаты в консоль? 1 - да, 2 - нет, 0 - выход: ")
            while True:
                if second_user_input == "1":
                    json_data.read()
                    break
                elif second_user_input == "2":
                    break
                elif second_user_input == "0":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
            third_user_input = input("Хотите удалить результаты поиска? 1 - да, 2 - нет, 0 - выход: ")
            while True:
                if third_user_input == "1":
                    json_data.delete()
                    break
                elif third_user_input == "2":
                    break
                elif third_user_input == "0":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
            fourth_user_input = input("Хотите посмотреть еще вакансии? 1 - да, 2 - нет: ")
            while True:
                if fourth_user_input == "1":
                    break
                elif fourth_user_input == "2":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
        elif user_input == "2":
            vacancies = Vacancies()
            vac_list = vacancies.vacancies_list_sj()
            json_data = JsonData()
            json_data.add(vac_list)
            second_user_input = input("Хотите вывести данные о вакансиях в консоль? 1 - да, 2 - нет, 0 - выход: ")
            while True:
                if second_user_input == "1":
                    json_data.read()
                    break
                elif second_user_input == "2":
                    break
                elif second_user_input == "0":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
            third_user_input = input("Хотите удалить список вакансий? 1 - да, 2 - нет, 0 - выход: ")
            while True:
                if third_user_input == "1":
                    json_data.delete()
                    break
                elif third_user_input == "2":
                    break
                elif third_user_input == "0":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
            fourth_user_input = input("Хотите посмотреть еще вакансии? 1 - да, 2 - нет: ")
            while True:
                if fourth_user_input == "1":
                    break
                elif fourth_user_input == "2":
                    print("Приходите еще!")
                    quit()
                else:
                    print("Введите 1, 2 или 0!")
                    continue
        elif user_input == "0":
            print("Приходите еще!")
            quit()
        else:
            print("Введите 1, 2 или 0!")
            continue

