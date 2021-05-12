from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
URL = 'https://www.boliga.dk/resultat'
pages = 0

def pages_scrape():
    req = requests.get(URL)
    soup = bs(req.text, 'html.parser')
    css_path = soup.select("div.d-none:nth-child(4) > app-pagination:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > a:nth-child(2)")[0]
    pages = css_path.getText()

def get_all_residence():
  
    for page in pages:
        # pls note that the total number of
        # pages in the website is more than 5000 so i'm only taking the
        # first 10 as this is just an example
    
        req = requests.get(URL + str(page) + '/')
        soup = bs(req.text, 'html.parser')
    
        titles = soup.find_all('div',attrs={'class','head'})
    
        for i in range(4,19):
            if page>1:
                print(f"{(i-3)+page*15}" + titles[i].text)
            else:
                print(f"{i-3}" + titles[i].text)


pages_scrape()