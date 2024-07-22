import requests
import pandas as pd
from bs4 import BeautifulSoup

file_path = 'city_data.xlsx'
df = pd.read_excel(file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()

data_to_excel = []

for city in citynames:
    cityname = city.replace(' ', '-')
    response = requests.get(f'https://www.neighborhoodscout.com/il/{cityname}/schools')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if soup.select('.row.updated-idx-card'):
        score_table = soup.select('.row.updated-idx-card')
        scores = score_table[0].find_all('h1', class_='score')
        score_compared_to_il = int(scores[0].text.strip())
        score_compared_to_us = int(scores[1].text.strip())

        data_to_excel.append([city, score_compared_to_il, score_compared_to_us])
    else:
        print(f'No data found for {city}')

# print(data_to_excel)

df = pd.DataFrame(data_to_excel, columns=['city_name', 'score_compared_to_il', 'score_compared_to_us'])
df.to_excel('school_score.xlsx', index=False)
