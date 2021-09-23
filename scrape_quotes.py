from bs4 import BeautifulSoup
import requests
from csv import DictWriter
from time import sleep

base_url = "http://quotes.toscrape.com/"

def scrape_quotes():
	next_url = "/page/1"
	all_quotes = []
	while next_url:	
		destination = f"{base_url}{next_url}"
		response = requests.get(destination)
		print(destination)
		soup = BeautifulSoup(response.text, "html.parser")
		quote_block = soup.select(".quote")

		for quote in quote_block:
			all_quotes.append({
				"text": quote.find(class_="text").get_text(),
				"author": quote.find(class_ = "author").get_text(),
				"bio_url": quote.find("a")["href"]
				})
			
		next_btn = soup.find(class_ = "next")
		next_url = next_btn.find("a")["href"] if next_btn else None
		sleep(1)
	return all_quotes

def write_csv(quotes):
	with open("quotes.csv", "w", newline = "\n") as file:
		headers = ["text", "author", "bio_url"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for quote in quotes:
			csv_writer.writerow(quote)

quotes = scrape_quotes()
write_csv(quotes)