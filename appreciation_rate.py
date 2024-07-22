import requests
import pandas as pd
from bs4 import BeautifulSoup

file_path = 'city_data.xlsx'
df = pd.read_excel(file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()

data_to_excel = []

for city in citynames:
    cityname = city.replace(' ', '-')
    response = requests.get(f'https://www.neighborhoodscout.com/il/{cityname}/real-estate')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if soup.select('.trends-table__container'):
        rate_table = soup.select('.trends-table__container')

        for rate in rate_table:
            appreciation_rate = rate.find_all('span', class_='dyn')

            latest_quater = appreciation_rate[1].text.strip().replace('%', '')
            last_12months = appreciation_rate[3].text.strip().replace('%', '')
            last_2years = appreciation_rate[5].text.strip().replace('%', '')
            last_5years = appreciation_rate[7].text.strip().replace('%', '')
            last_10years = appreciation_rate[9].text.strip().replace('%', '')
            since_2000 = appreciation_rate[11].text.strip().replace('%', '')

            data_to_excel.append(
                [city, latest_quater, last_12months, last_2years, last_5years, last_10years, since_2000])
    else:
        print(f'No data found for {city}')

df = pd.DataFrame(data_to_excel, columns=['city_name', 'latest_quater', 'last_12months', 'last_2years', 'last_5years', 'last_10years', 'since_2000'])
df.to_excel('appreciation_rate_data.xlsx', index=False)