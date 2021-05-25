from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import residence
import pandas as pd
import re
import threading
import time
import concurrent.futures

URL = 'https://www.boliga.dk/resultat'


def get_number_of_pages():
    req = requests.get(URL)
    soup = bs(req.text, 'html.parser')
    css_path = soup.select(
        "div.d-none:nth-child(4) > app-pagination:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > a:nth-child(2)")[0]
    pages = css_path.getText()

    return int(pages)


def residences_to_csv(residence_list, file_path):
    file = open(file_path, "w")
    csv_labels = "house_type;house_zip_code;house_rooms;house_square_meters;house_year;house_taxes;house_energy;house_ground_area;house_price"
    file.write(csv_labels + "\n")
    for r in residence_list:
        csv_text = "{house_type};{house_zip_code};{house_rooms};{house_square_meters};{house_year};{house_taxes};{house_energy};{house_ground_area};{house_price};".format(
            house_type=r.house_type, house_price=r.house_price, house_rooms=r.house_rooms, house_square_meters=r.house_square_meters, house_year=r.house_year, house_zip_code=r.house_zip_code, house_taxes=r.house_taxes, house_energy=r.house_energy, house_ground_area=r.house_ground_area)
        file.write(csv_text + "\n")
    file.close()


# Metoden skal ikke længere bruges, da vi henter concurrent nu

residence_list = []

def get_residences(page_number):
    
    zip_num_reg = re.compile(r'\d{4}')
    response = requests.get(URL + "?page=" + str(page_number) + '/')
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        all_houses = soup.find_all("a", {"class": "house-list-item"})
        for house in all_houses:
            try:
                house_type = house.find("span", {"class": "text"}).getText()
                if (house_type == "Helårsgrund" or house_type == "Fritidsgrund" or house_type == "Landejendom" or house_type == "Andet" or house_type == "Fritidshus" or house_type == "Andelsbolig"):
                    continue
                house_price_nan = house.find("div", {
                                               "class": "primary-value d-flex justify-content-end"}).getText().split(" ")[-2].split("k")[0]
                house_price = house_price_nan.replace(u'\xa0', u' ').split(" ")[
                    0].replace(".", "")
                house_rooms = house.find(
                    "span", {"class": "text-nowrap"}).getText().split(" ")[1]
                house_square_meters = house.find_all(
                    "span", {"class": "text-nowrap"})[1].getText().split(" m²")[0].split(" ")[1]
                house_year_date = house.find_all(
                    "span", {"class": "text-nowrap"})[3].getText()
                
                if(house_year_date.__contains__('-')):
                    continue
                house_year = (2021-int(house_year_date))
                house_zip_text = house.find_all(
                    "div", {"class": "secondary-value d-flex flex-wrap"})[0].getText()
                house_zip_code = zip_num_reg.search(house_zip_text).group()
                house_taxes_nan = house.find_all(
                    "span", {"class": "text-nowrap"})[5].getText().split(": ")[1].split(" k")[0]
                
                house_taxes = house_taxes_nan.replace(u'\xa0', u' ').split(" ")[
                    0].replace(".", "")
                house_energy = house.find_all(
                    "span", {"class": "text-nowrap"})[2].getText().split(": ")[1].split(" ")[0]
                if(house_energy.__contains__('-')):
                    continue
                
                house_ground_area_nan = house.find_all(
                    "span", {"class": "text-nowrap"})[4].getText().split(" ")[1].split(" m²")[0]
                house_ground_area = house_ground_area_nan.replace(u'\xa0', u' ').split(" ")[
                    0].replace(".", "")
                
                if(int(house_ground_area) == 0):
                    continue
                print(house_ground_area)
                resObj = residence.Residence(
                    house_type, house_zip_code, house_rooms, house_square_meters, house_year,house_taxes, house_energy, house_ground_area, house_price)
                
                residence_list.append(resObj)
            except:
                pass


# print(len(get_all_residences_to_list()))

def get_residences_sequential():
    start_time = time.perf_counter()
    print(start_time) 
    pages = get_number_of_pages()
    threads = []
    for page in range(pages):
        get_residences(page)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f'Total execution time: {execution_time} secs')



def get_residences_concurrent():
    start_time = time.perf_counter()
    print(start_time) 
    pages = get_number_of_pages()
    threads = []
    for page in range(150):
        t = threading.Thread(target=get_residences, args=(page,))
        threads.append(t)
        t.start()
        t.join()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f'Total execution time: {execution_time} secs')

#get_residences_concurrent()


def get_residences_futures():
    start_time = time.perf_counter()
    print(start_time) 
    pages = get_number_of_pages()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_page = {executor.submit(get_residences, page): page for page in range(pages)}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            print(page)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f'Total execution time: {execution_time} secs')


get_residences_futures()
residences_to_csv(residence_list, "../data/residence.csv")

