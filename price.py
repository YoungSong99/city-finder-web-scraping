import requests
import pandas as pd
from bs4 import BeautifulSoup

file_path = 'city_data.xlsx'
df = pd.read_excel(file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()

data_to_excel = []


def clean_value(value):
    cleaned_value = value.replace('$', '').replace(',', '').split()[0]
    return int(cleaned_value)


for city in citynames:
    cityname = city.replace(' ', '-')
    response = requests.get(f'https://www.neighborhoodscout.com/il/{cityname}/real-estate')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    values = soup.find_all('p',
                           class_='report-card-text text-center text-cl-black text-2xl font-weight-semi-bold mt-2 mb-0')

    if len(values) >= 3:
        median_home_value = clean_value(values[0].text.strip())
        rental_value = clean_value(values[2].text.strip())
        data_to_excel.append([cityname, median_home_value, rental_value])

df = pd.DataFrame(data_to_excel, columns=['city_name', 'median_home_value','rental_value'])

df.to_excel('price.xlsx', index=False)