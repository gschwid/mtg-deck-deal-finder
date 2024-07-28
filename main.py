from facebook import run_facebook_script
from tcg import search_mtg
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(7)
    wait = WebDriverWait(driver, timeout=7)
    precon_market_vs_listing = {}

    found_precons = run_facebook_script(driver,wait,"magic the gathering commander precon", 25) # Getting the dictionary of all the found 
    
    print(found_precons)

    # Finding the good deals
    for key, value in found_precons.items():
        market_price = search_mtg(key,driver,wait)
        listing_price = value[0]
        precon_market_vs_listing[key] = [market_price, listing_price, value[1]]

        if market_price != -1:
            # Calculating the amount saved
            diff = market_price - listing_price # Calculate the difference
            percentage_saved = (diff / market_price) * 100

            # Creating a final dictionary of all the good deals
            if percentage_saved >= 20:

                print(f"{key}, Market: {market_price}, Listing: {listing_price}, Percentage Saved: {percentage_saved}, Link: {value[1]}")

    # Printing out everything at the end
    for key,value in precon_market_vs_listing.items():
        print(f'precon: {key}\nmarket price: {value[0]}\nlisting price: {value[1]}\nlink: {value[2]}\n---------------------')

    driver.quit() # Nicely close any browser open

if __name__ == '__main__':
    main()



