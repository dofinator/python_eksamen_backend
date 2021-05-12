from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
URL = 'https://www.boliga.dk/resultat'

def pages_scrape():
    req = requests.get(URL)
    soup = bs(req.text, 'html.parser')
    css_path = soup.select("div.d-none:nth-child(4) > app-pagination:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > a:nth-child(2)")[0]
    pages = css_path.getText()

    return int(pages)

def get_all_residences():
    pages = pages_scrape()

    #for page in range(pages):
        # pls note that the total number of
        # pages in the website is more than 5000 so i'm only taking the
        # first 10 as this is just an example
    
    req = requests.get(URL + "?page=" + "1" + '/')
    soup = bs(req.text, 'html.parser')
        
    #all_houses = soup.select(".housing-list-results > app-housing-list-results:nth-child(1) > div:nth-child(1) > div:nth-child(2)")
    
    all_houses = soup.find_all("a", {"class": "house-list-item"})

    for house in all_houses:
        house_type = house.find("span", {"class": "text"}).getText()
        house_price = house.find("div", {"class": "primary-value d-flex justify-content-end"}).getText().split("  ")[1].split("k")[0]
        house_rooms = house.find("span", {"class": "text-nowrap"}).getText().split(" ")[1]
        house_square_meters = house.find_all("span", {"class": "text-nowrap"})[1].getText().split(" m²")[0]
        house_year = house.find_all("span", {"class": "text-nowrap"})[3].getText()
        house_zip_code = house.find_all("div", {"class": "secondary-value d-flex flex-wrap"})[0].getText().split(",")[1].split(" ")[0]

get_all_residences()