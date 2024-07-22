import requests
import pandas as pd
from bs4 import BeautifulSoup

file_path = 'city_data.xlsx'
df = pd.read_excel(file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()

data_to_excel = []

for city in citynames:
    cityname = city.replace(' ', '-')
    response = requests.get(f'https://www.neighborhoodscout.com/il/{cityname}/crime')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if soup.select('.crime-data-container'):
        crime_data = soup.select('.crime-data-container')

        for data in crime_data:
            crime_index = int(data.select_one('.score').text.strip())
            crime_rates = data.find_all('td', class_='text-center')
            violent_crime_rate = float(crime_rates[3].text.strip())
            property_crime_rate = float(crime_rates[4].text.strip())

            data_to_excel.append([city, crime_index, violent_crime_rate, property_crime_rate])
    else:
        print(f'No data found for {city}')

df = pd.DataFrame(data_to_excel, columns=['city_name', 'crime_index', 'violent_crime_rate', 'property_crime_rate'])
df.to_excel('city_crime_data.xlsx', index=False)
