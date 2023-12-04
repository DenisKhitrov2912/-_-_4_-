import requests
import json


class GetApiData:
    def __init__(self, api, params):
        self.api = api
        self.params = params

    def get_api_data(self):
        response = requests.get(self.api, params=self.params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка при выполнении запроса. Код: {response.status_code}")


class TreatmentData:
    def __init__(self, data_json, file_name):
        self.data_json = data_json
        self.file_name = file_name

    def append_data(self):
        with open(self.file_name, 'w', encoding='utf-8') as json_file:
            json.dump(GetApiData.get_api_data, json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в api_data.json")
