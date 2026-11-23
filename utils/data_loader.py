import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_irrigation_data():
    json_path = os.path.join(BASE_DIR, 'data', 'irigasi.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_weather_data():
    csv_path = os.path.join(BASE_DIR, 'data', 'curah_hujan.csv')
    weather_list = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            weather_list.append(row)
    return weather_list