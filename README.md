# Magic The Gathering Commander Deck Deal Finder

## Project Overview
This personal project aims to find deals on  Magic: The Gathering decks by analyzing listings on Facebook Marketplace. By comparing these listings with prices on TCGPlayer, the project identifies opportunities where decks are being sold for less than their market value. This is a script specific to my set up, so it likely wont work if you download it and try to run it.

## How It Works
Since neither Facebook Marketplace nor TCGPlayer offers APIs, this project uses web scraping to gather data from both sites. The Selenium library, a tool for browser automation, drives the process. Here’s a step-by-step breakdown:

1. Login and Search: The script logs into my Facebook account, searches for Magic: The Gathering decks, and scrolls through listings.

2. Listing Parsing: It parses the titles of the listings and identifies those that might contain sealed decks. If a listing has multiple decks, the script clicks into the listing to examine the description for individual deck names and prices. Since Facebook Marketplace has no description standard, it does not work all the time, but if the price is on the same line as the deck name it is found.

3. Price Extraction: For each relevant listing, the script checks if it’s local to Minnesota or available for shipping. It calculates the final price by including shipping costs if applicable. If the listing is outside of Minnesota it is not considered a valid option

4. Market Comparison: It then searches TCGPlayer for the official market prices of the identified decks.

5. Deal Detection: By comparing the Facebook Marketplace prices with TCGPlayer prices, the script calculates the percentage discount. the deals are then defined in [this](https://github.com/gschwid/mtg-deck-deal-finder/blob/main/found%20deals.md) text file. 

## Biggest challenges
1) **Deck Name Variability**: Listings often contained misspelled or varied representations of deck names, which led to missed deals when using simple substring matching. To tackle this, I employed the `difflib` library to find close matches between words. By breaking down both the listing titles and deck names into individual words and comparing them, I counted matches to determine if a listing was relevant. This approach significantly improved the accuracy of identifying deck names despite variations in spelling or phrasing.

2) **Parsing Issues**: Listings sometimes included multiple numbers, such as quantities of decks and prices, within their descriptions. This made it difficult to distinguish the actual price from other numbers. Initially, relying on numerical values alone proved problematic. To resolve this, I modified the script to extract all numbers and then select the highest value, which is most likely to be the correct price. Additionally, the script checks for keywords indicating that a listing is marked as sold, ensuring that such listings are not included in the results.

3) **TCGPlayer Search Accuracy**: Initially, TCGPlayer’s search filters for sealed products led to inaccurate stock information, with many decks being misclassified as out of stock. To address this, I began by searching for decks on TCGPlayer without applying any filters, focusing on the first product listing containing "deck" in the title. While this approach helped retrieve a broader range of relevant products, it also included variations such as collector’s editions and minimal packaging, which could distort pricing. To enhance accuracy, I implemented a further sorting step to exclude these collector’s items and minimal packaging options. This additional filtering ensured that only standard decks were considered, improving the relevance and reliability of the pricing information.


