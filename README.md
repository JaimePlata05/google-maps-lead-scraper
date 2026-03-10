# Google Maps Lead Scraper

A Python scraper that extracts business information from Google Maps.

This tool can collect hundreds of businesses including their contact information and export them into an Excel file.

## Features

- Scrapes business data from Google Maps
- Extracts business name
- Extracts address
- Extracts phone number
- Extracts rating and reviews
- Extracts website
- Extracts email (if available)
- Extracts business hours
- Saves results to Excel

## Technologies Used

- Python
- Playwright
- Pandas
- Geopy

## Installation

Clone the repository:

git clone https://github.com/JaimePlata05/google-maps-lead-scraper.git

Go to the project folder:

cd google-maps-lead-scraper

Install dependencies:

pip install -r requirements.txt

Install Playwright browser:

playwright install

## Usage

Run the scraper:

python scraper.py

The program will ask:

- Business type
- City
- Number of results

Example:

Dentists  
Miami  
500

## Output

The scraper generates an Excel file containing:

- name
- address
- phone
- rating
- reviews
- website
- email
- business hours
- Google Maps link

Example output file:

dentists_miami.xlsx

## Disclaimer

This project is for educational purposes only.
Make sure to respect Google Maps terms of service when using it.

## Author

Jaime Plata
