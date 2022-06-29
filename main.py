import os
import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep


chrome_driver_path = "/Users/mhatem/Documents/Development/chromedriver"
FORM_LINK = os.environ["FORM_LINK"]
header = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9"
}

params = {
    "pagination":{"currentPage":1}
}

response = requests.get("https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.60121382666016%2C%22east%22%3A-122.26544417333984%2C%22south%22%3A37.67155587510676%2C%22north%22%3A37.87888168056233%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D", headers=header)
response.raise_for_status()

html = response.text

soup = BeautifulSoup(html, "html.parser")

link_elements = soup.select(".list-card-top a")
links = []

for link in link_elements:
    href = link["href"]
    if "http" not in href:
        links.append(f"https://zillow.com/{href}")
    else:
        links.append(href)

price_elements = soup.select(".list-card-info .list-card-heading .list-card-price")
prices = []

for price in price_elements:
    prices.append(price.text.split()[0])

address_elements = soup.select(".list-card-info a")
addresses = []

for address in address_elements:
    addresses.append(address.text)

serve = Service(chrome_driver_path)
driver = webdriver.Chrome(service=serve)

for n in range(len(links)):
    driver.get(FORM_LINK)
    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_of_property = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(addresses[n])
    price_of_property.send_keys(prices[n])
    link.send_keys(links[n])
    submit.click()



