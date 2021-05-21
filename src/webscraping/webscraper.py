from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import residence
import pandas as pd
import re
import threading
import time

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
    csv_labels = "house_type;house_zip_code;house_rooms;house_square_meters;house_year;house_price"
    file.write(csv_labels + "\n")
    for r in residence_list:
        csv_text = "{house_type};{house_zip_code};{house_rooms};{house_square_meters};{house_year};{house_price};".format(
            house_type=r.house_type, house_price=r.house_price, house_rooms=r.house_rooms, house_square_meters=r.house_square_meters, house_year=r.house_year, house_zip_code=r.house_zip_code)
        file.write(csv_text + "\n")
    file.close()


# Metoden skal ikke længere bruges, da vi henter concurrent nu
def get_all_residences_to_list():
    residence_list = []
    #pages = get_number_of_pages()
    pages = 50
    zip_num_reg = re.compile(r'\d{4}')

    for page in range(pages):
        response = requests.get(URL + "?page=" + str(page) + '/')

        soup = bs(response.text, 'html.parser')
        all_houses = soup.find_all("a", {"class": "house-list-item"})

        for house in all_houses:
            try:
                house_type = house.find("span", {"class": "text"}).getText()
                if (house_type == "Helårsgrund" or house_type == "Fritidsgrund" or house_type == "Landejendom" or house_type == "Andet"):
                    continue
                house_price_space = house.find("div", {
                                               "class": "primary-value d-flex justify-content-end"}).getText().split(" ")[-2].split("k")[0]
                house_price = house_price_space.replace(u'\xa0', u' ').split(" ")[
                    0].replace(".", "")

                house_rooms = house.find(
                    "span", {"class": "text-nowrap"}).getText().split(" ")[1]
                house_square_meters = house.find_all(
                    "span", {"class": "text-nowrap"})[1].getText().split(" m²")[0]
                house_year = house.find_all(
                    "span", {"class": "text-nowrap"})[3].getText()
                if(house_year.__contains__('-')):
                    continue
                house_zip_text = house.find_all(
                    "div", {"class": "secondary-value d-flex flex-wrap"})[0].getText()
                house_zip_code = zip_num_reg.search(house_zip_text).group()

                resObj = residence.Residence(
                    house_type, house_zip_code, house_rooms, house_square_meters, house_year, house_price)
                residence_list.append(resObj)
            except:
                pass

    return residence_list



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
                if (house_type == "Helårsgrund" or house_type == "Fritidsgrund" or house_type == "Landejendom" or house_type == "Andet"):
                    continue
                house_price_space = house.find("div", {
                                               "class": "primary-value d-flex justify-content-end"}).getText().split(" ")[-2].split("k")[0]
                house_price = house_price_space.replace(u'\xa0', u' ').split(" ")[
                    0].replace(".", "")
                
                #n = 2
                #house_price_split = [house_price_string[i:i+n] for i in range(0, len(house_price_string), n)]
                #house_price = house_price_split[0]
                house_rooms = house.find(
                    "span", {"class": "text-nowrap"}).getText().split(" ")[1]
                house_square_meters = house.find_all(
                    "span", {"class": "text-nowrap"})[1].getText().split(" m²")[0]
                house_year = house.find_all(
                    "span", {"class": "text-nowrap"})[3].getText()
                if(house_year.__contains__('-')):
                    continue
                house_zip_text = house.find_all(
                    "div", {"class": "secondary-value d-flex flex-wrap"})[0].getText()
                house_zip_code = zip_num_reg.search(house_zip_text).group()
                resObj = residence.Residence(
                    house_type, house_zip_code, house_rooms, house_square_meters, house_year, house_price)
                residence_list.append(resObj)
            except:
                pass


# print(len(get_all_residences_to_list()))


def get_residences_concurrent():
    pages = get_number_of_pages()
    threads = []
    for page in range(pages):
        t = threading.Thread(target=get_residences, args=(page,))
        threads.append(t)
        t.start()
        t.join()


get_residences_concurrent()
residences_to_csv(residence_list, "../data/residence.csv")
