import requests
import pandas as pd
from bs4 import BeautifulSoup

file_path = 'city_data.xlsx'
df = pd.read_excel(file_path, sheet_name='city', usecols='A', skiprows=1, nrows=1563)
citynames = df[df.columns[0]].tolist()

# print(citynames)
data_to_excel = []

for city in citynames:
    cityname = city.replace(' ', '-')
    response = requests.get(f'https://www.neighborhoodscout.com/il/{cityname}/demographics')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    diversity_section = soup.select('#top-languages-chart')
    if diversity_section:
        languages_elements = diversity_section[0].find_all('span', class_='horiz-bar-label-span')
        percentages_div = diversity_section[0].find_all('div',
                                                        class_='horiz-bar-chart-label horiz-bar-chart-label-outer')

        top_languages = [span.text.strip() for span in languages_elements[:5]]
        percentages = [div.text.strip() for div in percentages_div[:5]]

        top_percentages = [float(p.replace('%', '')) for p in percentages]

        for _ in range(5):
            language_data = [city, top_languages[_], top_percentages[_]]
            data_to_excel.append(language_data)

        # print(data_to_excel)
    else:
        print(f'No data found for {city}')

df = pd.DataFrame(data_to_excel, columns=['city_name', 'language', 'percentage'])
# print(df)
df.to_excel('language_data.xlsx', index=False)
