import requests
from scrapy import Selector

def get_example_sentences(key, value):
    """ Scrape example sentences """
    url = 'https://www.wanikani.com' + value
    html = requests.get( url ).content
    sel = Selector(text = html)
    
    divs = sel.css("div.context-sentence-group > p::text").extract()

    jp = [div for div in divs[::2]]
    en = [div for div in divs[1::2]]

    character = key[0]
    pronunciation = key[1]
    meaning = key[2]
    
    theme = (character, meaning + " (" + pronunciation + ")")

    return [theme, *zip(jp,en)]


def get_input():
    """ Collect all input from the user"""
    sentences = 0
    pronunciation_incl = 0
    print("Choose element type:")
    element_choice = int(input("1: radicals\n2: kanji\n3: vocabulary\n"))
    if element_choice == 1:
        element_type = "radicals"
    elif element_choice == 2:
        element_type = "kanji"
    elif element_choice == 3:
        element_type = "vocabulary"
        sentences_choice = input("Would you like to download example sentences? (y/n)\n")
        if sentences_choice == "y":
            sentences = 1
    else:
        return 1


    print("Choose difficulty:")
    difficulty_choice = int(input("1: 快 Pleasant Levels 01-10\n2: 苦 Painful Levels 11-20\n3: 死 Death Levels 21-30\n4: 地獄 Hell Levels 31-40\n5: 天国 Paradise Levels 41-50\n6: 現実 Reality\n"))
    if difficulty_choice == 1:
        difficulty ="pleasant"
    elif difficulty_choice == 2:
        difficulty = "painful"
    elif difficulty_choice == 3:
        difficulty ="death"
    elif difficulty_choice == 4:
        difficulty = "hell"
    elif difficulty_choice == 5:
        difficulty ="paradise"
    else:
        difficulty = "reality"

    level = input("Choose level:\n")
    if element_choice == 2 or element_choice == 3 and sentences == 0:
        pronunciation_choice = input("Do you want to include pronunciation data? (y/n)")
        if pronunciation_choice == "y":
            pronunciation_incl = 1

    print(f"Scraping {element_type} at {difficulty} difficulty from level {level} ...")
    return [element_type, difficulty, level, pronunciation_incl, sentences]
