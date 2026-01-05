# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:43:17 2024

@author: ALI CAN
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

cities = ["Adana", "Adiyaman-Turkey", "Afyon-Turkey", "Agri-Turkey", "Amasya-Turkey", "Ankara", "Antalya", 
          "Artvin-Turkey", "Aydin-Turkey", "Balikesir-Turkey", "Bilecik-Turkey", "Bingol-Turkey", "Bitlis-Turkey", "Bolu-Turkey", 
          "Burdur-Turkey", "Bursa", "Canakkale-Turkey", "Corum-Turkey", "Denizli", "Diyarbakir-Turkey", 
          "Edirne-Turkey", "Elazig-Turkey", "Erzincan-Turkey", "Erzurum-Turkey", "Eskisehir", "Gaziantep", "Giresun-Turkey", 
          "Hakkari-Turkey", "Isparta-Turkey", "Istanbul", "Izmir", 
          "Kars-Turkey", "Kastamonu-Turkey", "Kayseri-Turkey", "Kirklareli-Turkey", "Kirsehir-Turkey", "Kocaeli", "Konya", 
          "Kutahya-Turkey", "Malatya-Turkey", "Manisa-Turkey", "Kahramanmaras-Turkey", "Mardin-Turkey", "Mugla-Turkey", "Mus-Turkey", 
          "Nevsehir-Turkey", "Nigde-Turkey", "Ordu-Turkey", "Rize-Turkey", "Sakarya-Turkey", "Samsun", "Siirt-Turkey", "Sinop-Turkey", 
          "Sivas-Turkey", "Tekirdag-Turkey", "Tokat-Turkey", "Trabzon-Turkey", "Tunceli-Turkey", "Sanliurfa-Turkey", "Usak-Turkey", 
          "Van-Turkey", "Yozgat-Turkey", "Zonguldak-Turkey", "Aksaray-Turkey", "Bayburt-Turkey", "Karaman-Turkey", "Kirikkale-Turkey", 
          "Batman-Turkey", "Sirnak-Turkey", "Bartin-Turkey", "Ardahan-Turkey", "Yalova-Turkey", "Karabuk-Turkey", 
          "Kilis-Turkey", "Osmaniye-Turkey", "Duzce-Turkey"]


def get_item_names(city):
    # Function that gets name of all features
    
    try:
        url = f"https://www.numbeo.com/cost-of-living/in/{city}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_="data_wide_table new_bar_table")
        rows = table.find_all('tr')
        item_names = [row.find_all('td')[0].get_text(strip=True) for row in rows if len(row.find_all('td')) >= 2]
        return item_names
    except Exception as e:
        print(f"Error fetching item names for {city}: {e}")
        return []


def get_item_prices(city):
    # Function that gets 
  
    try:
        url = f"https://www.numbeo.com/cost-of-living/in/{city}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_="data_wide_table new_bar_table")
        rows = table.find_all('tr')
        item_prices = [row.find_all('td')[1].get_text(strip=True) for row in rows if len(row.find_all('td')) >= 2]
        return item_prices
    except AttributeError:
        return None


def scrape_data(cities):
    # Creating a dataframe and then scrapping the data for each city

    item_names = get_item_names(cities[0])
    df = pd.DataFrame({"Item": item_names})
    
    error_cities = []
    for city in cities:
        item_prices = get_item_prices(city)
        if item_prices:
            df[city] = item_prices
        else:
            error_cities.append(city)
        print(f"Data scrapped for the city: {city}.")  
    return df, error_cities


def save_to_excel(df, filename="cost_of_living_Turkey_Excel.xlsx"):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        
        df.to_excel(full_path, index=False)
        print(f"Dataset successfully saved: {full_path}")
        
    except Exception as e:
        print(f"Error occured!: {e}")



# Main execution
if __name__ == "__main__":
    df, error_cities = scrape_data(cities)
    print(df.head())
    
    if error_cities:
        print("The data couldn't found for':", error_cities)
    
    save_to_excel(df)
