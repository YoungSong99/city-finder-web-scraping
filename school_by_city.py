import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

cityname_file_path = 'city_data.xlsx'
df = pd.read_excel(cityname_file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()
print(citynames)


def get_schools_data(cityname):
    load_dotenv()
    api_key = os.getenv('GREATSCHOOLS_API_KEY')

    url = f'https://gs-api.greatschools.org/schools?city={cityname}&state=IL&limit=50'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        folder_path = os.path.join(os.getcwd(), 'school_data_by_city')
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f'{cityname}.json')
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        # print(f"Data for zipcode {zipcode} saved to {file_path}")
    else:
        print(f"Failed to get data of {cityname}: {response.status_code}")


for city in citynames:
    get_schools_data(city)