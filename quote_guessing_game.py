import requests
from bs4 import BeautifulSoup
import random 
from pyfiglet import figlet_format


# the function that will take the url it is given and parse it accordingly.
def quote_parser(url):
    # getting the response from the url
    response = requests.get(url)
    # creating a variable to store the markup of the page
    markup = response.text
    # constructing a BeautifulSoup parser
    parser = BeautifulSoup(markup, "html.parser")
    # initializing the list of quotes we will be returning.
    return_quotes = []

    #put all of the quote markup in the quotes_parser list
    quotes_parser = parser.findAll(class_="quote")
    
    for quote_markup in quotes_parser:
        #grab text of the quote
        text = quote_markup.find(class_="text").get_text()
        #grab author of the quote
        author = quote_markup.find(class_="author").get_text()
        #grab href of the link to the person's bio
        author_bio_link = quote_markup.find('a')['href']
        return_quotes.append([text, author, author_bio_link])
    return return_quotes

#MAIN FUNCTIONALITY OF OUR PROGRAM

# setting the base url to be the address of the website we are looking for
base_url = "http://quotes.toscrape.com/"
# if we hit the button next, the next url displayed will be with page/ extension.
quote_url_extension = "page/"

# the second page number is used since the first page is the base_url
quote_url_page_number = 2

# setting up the container for all of the quotes stored on the website
quotes_container = []

# adding the quote elements form the parsing of the base url with quotes
quotes_container.extend(quote_parser(base_url))

# QUOTE SCRAPING FUNCTIONALITY -> FILLS UP 2D ARRAY WITH QUOTES.
while True:
    # try returning the quote parse of the next page page
    temp_list = quote_parser(base_url + quote_url_extension + str(quote_url_page_number))
    
    #however if the page returned an empty list back to us, we need to break from the loop
    if not temp_list:
        break

    #otherwise, we add that temp_list to the overall quotes_container list 
    quotes_container.extend(temp_list)

    #increment the quote_url_page number by one as we moving down through the links
    quote_url_page_number += 1


# GAME FUNCTIONALITY
print(figlet_format("WELCOME TO THE QUOTE GUESSING GAME!"))

print("Your quote is coming up... But here are the rules:")
print("1. You need to guess the author of the quote to win.")
print("2. You have up to 4 guesses!")
print("3. You will receive a hint after each incorrect try.\n\n") 

start_game = input("Ready to play? (y/n)")

while start_game == 'y':
    number_of_guesses = 4 #each user is given 4 guesses
    random_picker = random.randint(0, (len(quotes_container)-1)) #get the random index number to pick a quote
    play_quote_container = quotes_container[random_picker]
    play_quote_text = play_quote_container[0]
    play_quote_author = play_quote_container[1]
    play_quote_author_url = play_quote_container[2]

    print("\n\nYour quote for today is: \n\n" + play_quote_text + '\n')
    while number_of_guesses != 0 and start_game == 'y':
        #request the appropriate author's page
        response = requests.get(base_url + play_quote_author_url)
        markup = response.text
        # constructing a BeautifulSoup parser
        parser = BeautifulSoup(markup, "html.parser")

        tag = parser.find(class_="author-title").get_text()
        tag_split = tag.split()
        name = ""
        # due to bug in the website code need to do something freaky
        for word in tag_split:
            if word == "Born:":
                break
            else:
                name += word + " "
                 
        name_split = name.split()
        lastname_1st_letter = name_split[len(name_split) - 1][0].upper()
        lastname_count = len(name_split[len(name_split) - 1])

        if number_of_guesses == 4:
            # this is the first run of the guess of the user
            # prompt the user to enter his guess.
            guess = input("Who is the author of this quote? ")
            
            # compare the guess to the actual author
            # if matches, user wins, prompt to play again?
            if guess.upper() == play_quote_author.upper(): 
                print("Congratulations! You have guessed the author correctly!!!")
                start_game = input("Would you like to play again? (y/n) ")
                break
            # if does not match we prompt if the user wishes to continue, decrement the number_of_guesses and continue to the next iteration of the loop
            else: 
                number_of_guesses -= 1
                print("Oh no! This is incorrect author! You have " + str(number_of_guesses) + " guesses remaining still.")
                start_game = input("Would you like to keep guessing? (y/n) ")
        elif number_of_guesses == 3:
            #display the author birthdate and birthplace hint
            print("Here is your first hint: \n")
            print("This author was " + parser.find(class_="author-details").p.get_text())
            guess = input("Who is the author of this quote? ")
            if guess.upper() == play_quote_author.upper(): 
                print("Congratulations! You have guessed the author correctly!!!")
                start_game = input("Would you like to play again? (y/n) ")
                break
            else: 
                number_of_guesses -= 1
                print("Oh no! This is incorrect author! You have " + str(number_of_guesses) + " guesses remaining still.")
                start_game = input("Would you like to keep guessing? (y/n) ")   
        elif number_of_guesses == 2:
            #display some other hint
            print("Here is your second hint: \n")
            print("This author has " + str(lastname_count) + " letters in the lastname and it starts with letter " + lastname_1st_letter)
            guess = input("Who is the author of this quote? ")
            
            if guess.upper() == play_quote_author.upper(): 
                print("Congratulations! You have guessed the author correctly!!!")
                start_game = input("Would you like to play again? (y/n) ")
                break
            else: 
                number_of_guesses -= 1
                print("Oh no! This is incorrect author! You have " + str(number_of_guesses) + " guess remaining still.")
                start_game = input("Would you like to keep guessing? (y/n) ")
        elif number_of_guesses == 1:
            # warn that this is the last try, display a hint
            print("Here is your final hint! Be cautious, this is the last one I can give!\n")
            print("Author's first name is: " + name_split[0])
            guess = input("Who is the author of this quote? ")
            
            if guess.upper() == play_quote_author.upper(): 
                print("Congratulations! You have guessed the author correctly!!!\n")
                start_game = input("Would you like to play again? (y/n) ")
                break
            else: 
                print("\nOh no! YOU HAVE LOSTTTTT GAME OVERRRRRR\n")
                print("The correct author was:\n\n " + figlet_format(name))
                print("\nBetter luck next time!!!")
                start_game = input("\nWould you like to play another round? (y/n) ")
                break