# Magic The Gathering Commander Deck Deal Finder (Work in progress)

## Project Overview
This personal project aims to help discover great deals on sealed Magic: The Gathering decks by analyzing listings on Facebook Marketplace. By comparing these listings with prices on TCGPlayer, the project identifies opportunities where decks are being sold for less than their market value.

## How It Works
Since neither Facebook Marketplace nor TCGPlayer offers APIs, this project uses web scraping to gather data from both sites. The Selenium library, a tool for browser automation, drives the process. Here’s a step-by-step breakdown:

1. Login and Search: The script logs into your Facebook account, searches for Magic: The Gathering decks, and scrolls through listings.

2. Listing Parsing: It parses the titles of the listings and identifies those that might contain sealed decks. If a listing has multiple decks, the script clicks into the listing to examine the description for individual deck names and prices.

3. Price Extraction: For each relevant listing, the script checks if it’s local to Minnesota or available for shipping. It calculates the final price by including shipping costs if applicable.

4. Market Comparison: It then searches TCGPlayer for the official market prices of the identified decks.

5. Deal Detection: By comparing the Facebook Marketplace prices with TCGPlayer prices, the script calculates the percentage discount and highlights the best deals.

This process ensures the best possible prices for sealed Magic: The Gathering Commander decks are found for the Minnesota area.
