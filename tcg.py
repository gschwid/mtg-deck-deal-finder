import requests
from bs4 import BeautifulSoup 
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def search_mtg(card,driver,wait):
    try:
        card = re.sub("\d+", "", card)

        search_card = x = re.sub("\s", "+", card) # Replacing spaces with + so it matches how the search works
        URL = f'https://www.tcgplayer.com/search/magic/product?productLineName=magic&q={search_card}&view=grid&inStock=true&page=1'
    
        # Opening up a tab with selenium (just using requests doesnt work :( )
        driver.get(URL)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='product-card__market-price--value']")))
        html = driver.page_source # Get html for bs4

        # Parsing the object with beautiful soup for the price
        soup = BeautifulSoup(html, "html.parser")
        
        listings = soup.find_all('div', class_='product-card__content')
        for listing in listings:
            name = listing.find('span', class_='product-card__title truncate')
            name = name.text.lower()

            # Makes sure the product it is looking at is a deck
            if 'deck' not in name:
                continue
            
            # Make sure deck name is in listing
            elif card not in name:
                continue

            # Makes sure the deck is not minimal packaging or collectors version
            elif ('minimal' in name) or ('collector' in name):
                continue
            
            else:
                price = listing.find('span', class_='product-card__market-price--value')
                price = float(price.text[1:]) # Getting rid of the $ sign
                print

        return price
    
    except:
        print(f"{card} is out of stock")
        return -1

# driver = webdriver.Firefox()
# driver.implicitly_wait(7)
# wait = WebDriverWait(driver, timeout=7)
# search_mtg("enhanced evolution", driver, wait)