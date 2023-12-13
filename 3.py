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