from facebook import run_facebook_script
from tcg import search_mtg
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from datetime import datetime
import string

def main():
    count=0
    driver = webdriver.Firefox()
    driver.implicitly_wait(7)
    wait = WebDriverWait(driver, timeout=7)
    precon_market_vs_listing = {}

    found_precons = run_facebook_script(driver,wait,"magic the gathering commander precon", 0) # Getting the dictionary of all the found 

    f = open("found deals.md", "w") # File where all the good deals are written to

    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"# Last Updated {formatted_now}\n\n")

    # Comparing listing prices to official market values, creating a dictionary
    for key, value in found_precons.items():
        market_price = search_mtg(key,driver,wait)
        listing_price = value[0]

        diff = market_price - listing_price # Calculate the difference
        percentage_saved = (diff / market_price) * 100

        key = string.capwords(key, sep = None) # Makes name have capitals again

        precon_market_vs_listing[key] = [market_price, listing_price, value[1], value[2], int(percentage_saved)]

    # Looping through the newly created dictionary to add to the text file
    f.write(f"## Listings That Are 20% Off Or Greater\n\n")
    for key, value in precon_market_vs_listing.items():
        if value[4] >= 20:
            key = ''.join([i for i in key if not i.isdigit()]) # Removes numbers
            f.write(f"**{key}**, Listing: {value[1]}, Market: {value[0]}, Percent Saved: {value[4]}%, [Link]({value[2]})\n\n")
        
    f.write(f"## Listings That Are 10% Off Or Greater\n\n")
    for key, value in precon_market_vs_listing.items():
        if value[4] >= 10 and value[4] < 20:
            key = ''.join([i for i in key if not i.isdigit()]) # Removes numbers
            f.write(f"**{key}**, Listing: {value[1]}, Market: {value[0]}, Percent Saved: {value[4]}%, [Link]({value[2]})\n\n")

    f.write(f"## The Rest Of The Listings\n")
    for key, value in precon_market_vs_listing.items():
        if value[4] < 10:
            key = ''.join([i for i in key if not i.isdigit()]) # Removes numbers
            f.write(f"**{key}**, Listing: {value[1]}, Market: {value[0]}, Percent Saved: {value[4]}%, [Link]({value[2]})\n\n")

    f.close()
    driver.quit() # Nicely close an\ browser open

if __name__ == '__main__':
    main()



