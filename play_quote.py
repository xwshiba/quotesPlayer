from random import randint
from csv import DictReader
from bs4 import BeautifulSoup
import requests

base_url = "http://quotes.toscrape.com/"

def start_game(quotes):
	text = [row["text"] for row in quotes]
	author = [row["author"] for row in quotes]
	bio_url = [row["bio_url"] for row in quotes]
	num = randint(0, len(text))
	quote = text[num]
	print("Here's a quote:")
	print(quote)
	print(author[num])

	guess = ''
	remainingNum = 4
	while guess.lower() != author[num].lower() and remainingNum > 0:
		guess = input(f"Who said this quote? Guess remaining {remainingNum}.\n")
		if guess.lower() == author[num].lower():
			print("You win!\n")
			break
		remainingNum -= 1
		print_hint(author[num], bio_url[num], remainingNum)
	again = ""
	while again.lower() not in ("y", "n"):
		again = input("Would you like to play again? (y/n) \n")
	if again.lower() in ("y"):
		print("Ok, You will play again.\n")
		return start_game(quotes)
	else:
		print("Goodbye!\n")

def read_csv(filename):
	with open(filename, "r") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

def print_hint(author, bio_url, remainingNum):
	if remainingNum == 3:
		res = requests.get(f"{base_url}{bio_url}")
		soup = BeautifulSoup(res.text, "html.parser")
		born_date = soup.find(class_ = "author-born-date").get_text()
		born_location = soup.find(class_ = "author-born-location").get_text()
		hint_1 = f"This author was born on {born_date} {born_location}."
		print(hint_1)
	elif remainingNum == 2:
		initial = ".".join([el for el in author if el.isupper()])
		hint_2 = f"The author's initial is {initial}"
		print(hint_2)
	elif remainingNum == 1:
		length = len([el for el in author.upper() if el.isupper()])
		hint_3 = f"The number of the letters in this author's name is {length}."
		print(hint_3)
	else:
		print(f"Sorry you don't have any remaining chances. The answer was {author}.") 

quotes = read_csv("quotes.csv")
start_game(quotes)



