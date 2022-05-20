from scrapy import Selector
import pandas as pd
import requests
from helper import get_input
from helper import get_example_sentences

# get and parse input from the user
raw_input = get_input()

element_type = raw_input[0]
difficulty = raw_input[1]
level = raw_input[2]
pronunciation_incl = raw_input[3]
sentences = raw_input[4]
url = "https://www.wanikani.com/" + element_type + "?difficulty=" + difficulty

# connect to the website
html = requests.get( url ).content

# create scrapy selector
sel = Selector(text = html)

level_items = sel.css("section#level-" + str(level) + " > ul li.character-item > a > span.character::text").extract()
level_pronunciations = sel.css("section#level-" + str(level) + " > ul li.character-item > a > ul > li:nth-of-type(1)::text").extract()
level_meanings = sel.css("section#level-" + str(level) + " > ul li.character-item > a > ul > li:nth-of-type(2)::text").extract()
level_links = sel.css("section#level-" + str(level) + " > ul li.character-item > a::attr(href)").extract()

character = [item.strip() for item in level_items]
pronunciation = [pron.strip() for pron in level_pronunciations]
meaning = [meaning.strip() for meaning in level_meanings]
link = [link for link in level_links]



# If user chose to download example sentences, invoke get_example_sentences function
if sentences == 1:
    dictionary = dict(zip(zip(character, pronunciation, meaning), link))
    result = [*map(get_example_sentences, dictionary.keys(), dictionary.values())]
    # flatten the results list
    flat = [item for sublist in result for item in sublist]

    # split into columns
    jp = [word[0] for word in flat]
    en = [word[1] for word in flat]

    # create pandas data frame
    df = pd.DataFrame(list(zip(jp, en)), columns = ["Japanese", "English"])
else:
    if pronunciation_incl == 0:
        df = pd.DataFrame([*zip(character, meaning)], columns = ["Japanese", "English"])
    else:
        meaning_pronunciation = ([*zip(meaning, pronunciation)])
        meaning_pronunciation = [x +" (" + y +")" for x, y in meaning_pronunciation]
        df = pd.DataFrame([*zip(character, meaning_pronunciation)], columns = ["Japanese", "English | Pronunciation"])

df.to_excel("_".join([element_type, difficulty, level]) + ".xlsx")
print("File saved")

