# Quote-Guessing-Game
The game is focused around scraping a popular quote website, analyzing the author of the quote, and a game that prompts the user to guess who the author of the quote is.


## Scraping
Scraping is done through BeautifulSoup library. I intended to scrape the entire quote contents of the website quotes.toscrape.com

Function quote_parser is responsible for taking in the intended url of the website, and going through multiple pages of quotes, identifying the blocks of data for the quote.

Each quote will consist of the content, author's name, the url of Author's page (used in producing game hints). The function returns a 2D array of the information about every quote on the webpage

## Game Interface and Gameplay
Game functionality is done through the main loop.

At first, it goes through the webpage and collects all the quotes, then displays the main menu for the player.

Once the player agrees to start the game, he is prompted with a randomized quote and asked to guess the author. If the player gets the option wrong, he is given up to 3 hints about the author (where he/she was born, what letter starts their last name, how many letters are in their last name).

Once the player guesses the quote correctly, he can play again, or quit the game. Upon failed answer, the user is prompted to play with a new quote or quit the game.

## Tutorial
The program requires pyfiglet and bs4 libraries (use pip install for both).

Once you have the required libraries, simply run with python3.
