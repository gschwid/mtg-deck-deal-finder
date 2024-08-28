from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from precon_list import precon_list
import difflib
import re
import pyautogui # This import is for clicking the annoying would you allow ads on facebook
from info import email, password

URL = "https://www.facebook.com/marketplace/minneapolis"
found_precon_dictionary = {}

def facebook_login(driver, wait):
    
    # Opens up firefox and goes to facebook marketplace
    driver.get(url=URL)
    wait.until(EC.presence_of_element_located((By.ID, ':r10:')))

    # inputting the email
    driver.find_element(By.ID, ":r10:").clear()
    driver.find_element(By.ID, ":r10:").send_keys(email)

    # Inputting the password
    driver.find_element(By.ID, ":r13:").clear()
    driver.find_element(By.ID, ":r13:").send_keys(password)

    # Clicking the login button
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[5]/div").click()
    time.sleep(2)

def facebook_search(driver, wait, card, scrolls):
    deck_found = False
    in_description = False
     
    # Finding the search bar and searching for a card.

    search_bar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/span/div/div/div/div/label/input")
    search_bar.send_keys(card)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(4) # Works for now, I need to find a better solution
    # wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='search-loading-indicator']"))) # Waits until it is done loading

    # Clicking the block ads pop up if it appears
    try:
        location = pyautogui.locateOnScreen("block.png")
        pyautogui.click(location)
    
    except:
        print("No pop ups requested")

    finally:

        # Scrolling down on the website to load options
        for i in range (scrolls):
            driver.execute_script('window.scrollBy(0, 2000)')
            time.sleep(1)

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME) # Goes back to the top of the page
        time.sleep(1)

        # Loop that opens up each relevant listing
        html_list = (driver.find_elements(By.XPATH, './/div[@class = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24"]'))
        del html_list[-8:] # Delete the last 8 elements, some bug causes one class to have 8 more than the other
        for listing in html_list:
            time.sleep(0.5) # Avoid getting detected

            deck_found = False # No deck has bee found yet
            in_description = False # Does not know if its in the description
            shipping = False
            shipping_cost = 0 # Default to 0

            # Parsing all of the important info on the main page          
            listing_link = listing.find_element(By.XPATH, './/a[@class = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv"]').get_attribute('href')
            listing_price = listing.find_element(By.XPATH, './/span[@class = "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u"]').text
            
            # Getting rid of any comas or $ symbols in the listing price
            price_list = re.findall(r'\d+', listing_price)
            listing_price = "" 
            for i in price_list: # Reconstruct the string
                listing_price = listing_price + i
            
            if listing_price == "": # If listing is set to free
                listing_price = 0
              
            listing_price = float(listing_price) # Convert it into an int for comparison later

            listing_name = listing.find_element(By.XPATH, './/span[@class = "x1lliihq x6ikm8r x10wlt62 x1n2onr6"]').text
            listing_name = listing_name.lower()
            listing_location = listing.find_element(By.XPATH, './/span[@class = "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]').text

            # Ensuring the listing location is either in MN or shipped to me
            if ("MN" not in listing_location):
                if("Ships to you" != listing_location):
                    continue # Skips to next loop, not worth doing all the parsing if it is not near me 

            # Create dictionary of values with matches
            for precon_name in precon_list:
                if find_similar_substring(precon_name, listing_name):

                    # Checking if it is being shipped, if so it will get the shipping cost
                    if listing_location == "Ships to you":
                        shipping_cost = get_shipping_cost(listing, wait, driver, False)
                    
                    add_to_dict(precon_name, [(listing_price + shipping_cost), listing_link, listing_location, in_description])
                    #found_precon_dictionary[precon_name] = [(listing_price + shipping_cost), listing_link, listing_location, in_description]
                    deck_found = True # this ensures it doesnt go into the next loop

                    print(f"match found in listing name: {precon_name}")
                    break
            
            # Checking if the title contains keywords that would imply they are selling multiple decks
            if (("deck" in listing_name) or ("sealed" in listing_name)) and (deck_found == False):
                listing.click() # Click into listing if it has those keywords
                wait.until(EC.invisibility_of_element_located,(By.XPATH, './/span[@class = "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u"]'))

                try: # If description is found
                    # Grabbing the description and splitting it by newline for parsing
                    description = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div[2]/div[1]/div/span').text.lower()
                    description_split_by_newline = re.split('\n', description) 

                    # Getting shipping cost if necessary
                    if listing_location == "Ships to you":
                        shipping = True
                        count_for_ship = 0

                    # Loop through the list again, extracting names and new price values 
                    for precon_name in precon_list: 
                        for description_line in description_split_by_newline:
                            description_line = re.sub(r'-(\d)', r' -\1', description_line)
                            if find_similar_substring(precon_name, description_line):
                                print(f"{precon_name} {description_line}")
                            #if precon_name in description_line:

                                # Get shipping cost (This system is janky)
                                if (shipping) and (count_for_ship == 0):
                                    shipping_cost = get_shipping_cost(listing,wait, driver,True)
                                    count_for_ship = 1 # Doing this count so this doesnt execute multiple times 
                                
                                if (re.search("sold", description_line) == None): # Checking if the deck has not been sold
                                    listing_price_new = re.findall(r'\d+', description_line)
                                    
                                    # Case where no number is in the description
                                    if listing_price_new == []:
                                        listing_price_new = [listing_price]

                                    in_description = True
    
                                    # Sometimes multiple numbers are picked up if the listing has multiple decks
                                    max = 0
                                    for i in listing_price_new:
                                        if (float(i) > max) and (float(i) < 200) and (float(i) > 14):
                                            max = float(i)
                                    max = float(max)

                                    # Case where number is found but is too small or big to be accurate
                                    if max == 0:
                                        max = listing_price

                                    print(f"match found in description: {precon_name}")

                                    add_to_dict(precon_name, [(max + shipping_cost), listing_link, listing_location, in_description])
                                    #found_precon_dictionary[precon_name] = [(max + shipping_cost), listing_link, listing_location, in_description]
                    time.sleep(1)
                    driver.back()
                    wait.until(EC.visibility_of,(By.XPATH, './/div[@class = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24"]'))
                
                except: # If it is not found
                    print("No description in listing")
                    driver.back()
                    wait.until(EC.visibility_of,(By.XPATH, './/div[@class = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24"]'))
        print(found_precon_dictionary)
        print(len(found_precon_dictionary))
        return found_precon_dictionary
    
def get_shipping_cost(listing, wait, driver,in_listing):
    if not in_listing:
        listing.click()
        wait.until(EC.invisibility_of_element_located,(By.XPATH, '//span[@class = "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u"]')) 
    
    time.sleep(1) # Time added to prevent detection

    # Finds the shipping description and extracts the number, which is returned
    try:                                                            
        shipping_desc = listing.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/span/span').text # Gets the shipping cost
        shipping_cost = float((re.findall(r'\d+\.\d+', shipping_desc))[0]) # extracts the price value

        if not in_listing:
            driver.back()
    
        return shipping_cost
    
    except:
        if not in_listing:
            driver.back()

        print("No shipping cost found") # This case also triggers with free shipping
        return 0 

def run_facebook_script(driver, wait, search, scrolls):
    facebook_login(driver, wait)
    return facebook_search(driver, wait, search, scrolls)

# Function for finding deck names in listing, finding "close enough" matches if the deck name isnt spelled exactly correct
def find_similar_substring(deck_name,listing):
    listing_words = listing.split()
    deck_words = deck_name.split()
    count = 0

    for i in deck_words:
        matching_result = difflib.get_close_matches(i, listing_words, n=1, cutoff=0.8)

        if matching_result: # Match for word found
            count +=1
    
    if count == len(deck_words):
        return True
    
    else:
        return False

# Finding best offer between decks when multiple offers are found
def add_to_dict(key,value):
    if key in found_precon_dictionary.keys():
        print(f"{found_precon_dictionary[key][0]} {value[0]}")
        if found_precon_dictionary[key][0] > value[0]:
            found_precon_dictionary[key] = value
    else:
        found_precon_dictionary[key] = value

    #     count = 1
    #     while f'{key} {str(count)}' in found_precon_dictionary.keys():
    #         count += 1
    #     found_precon_dictionary[f'{key}{str(count)}'] = value
    # else:
    #     found_precon_dictionary[key] = value


