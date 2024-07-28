import requests
from bs4 import BeautifulSoup 
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC

def search_mtg(card,driver,wait):
    
    try:
        card = x = re.sub("\s", "+", card) # Replacing spaces with + so it matches how the search works
        URL = f'https://www.tcgplayer.com/search/magic/product?productLineName=magic&q={card}&view=grid&inStock=true&page=1&ProductTypeName=Sealed+Products'
    
        # Opening up a tab with selenium (just using requests doesnt work :( )
        driver.get(URL)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='product-card__market-price--value']")))
        html = driver.page_source # Get html for bs4

        # Parsing the object with beautiful soup for the price
        soup = BeautifulSoup(html, "html.parser")
        
        price = soup.find('span', class_='product-card__market-price--value')
        price = float(price.text[1:]) # Getting rid of the $ sign
        
        return price
    
    except:
        print(f"{card} is out of stock")
        return -1


