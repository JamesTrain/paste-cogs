# Import HTML scraping tools to pull insults
import lxml
import requests
import lxml.html
# Import random to choose random insult from list
import random

# 5x5 * letter dictionary for insult output
letters = {         
    'a':['  *  ',' * * ','*****','*   *','*   *'],
    'b':['**** ','*   *','*****','*   *','**** '],
    'c':[' ****','*    ','*    ','*    ',' ****'],
    'd':['**** ','*   *','*   *','*   *','**** '],
    'e':['*****','*    ','*****','*    ','*****'],
    'f':['*****','*    ','*****','*    ','*    '],
    'g':['*****','*    ','* ***','*   *','*****'],
    'h':['*   *','*   *','*****','*   *','*   *'],
    'i':['*****','  *  ','  *  ','  *  ','*****'],
    'j':['***  ','  *  ','  *  ','  *  ','***  '],
    'k':['*   *','* *  ','*    ','* *  ','*   *'],
    'l':['*    ','*    ','*    ','*    ','*****'],
    'm':['*   *','** **','* * *','*   *','*   *'],
    'n':['*   *','**  *','* * *','*  **','*   *'],
    'o':[' *** ','*   *','*   *','*   *',' *** '],
    'p':['**** ','*   *','**** ','*    ','*    '],
    'q':[' *** ','*   *','* * *','*  * ',' ** *'],
    'r':['**** ','*   *','**** ','* *  ','*  **'],
    's':[' ****','*    ',' *** ','    *','**** '],
    't':['*****','  *  ','  *  ','  *  ','  *  '],
    'u':['*   *','*   *','*   *','*   *',' *** '],
    'v':['*   *','*   *',' * * ',' * * ','  *  '],
    'w':['*   *','*   *','* * *','* * *',' * * '],
    'x':['*   *',' * * ','  *  ',' * * ','*   *'],
    'y':['*   *',' * * ','  *  ','  *  ','  *  '],
    'z':['*****','   * ','  *  ',' *   ','*****'],
    ',':['     ','     ','   **','   **','  *  '],
    ':':['     ','  *  ','     ','  *  ','     '],
    '|':['*****','*****','*****','*****','*****'],
    ' ':['','','','','']
    }

# HTML scrape to pull insults from insult.wiki
html = requests.get('https://www.insult.wiki/list-of-insults')
doc = lxml.html.fromstring(html.content)
insults_list = doc.xpath('//html/body/ol/li/a/@href')
insult_string = ''.join(insults_list)
remove_html = 'https://www.insult.wiki/insult/'
result = insult_string.replace(remove_html,' ')
final_list = []

# Function to create 5x5 * letters for insult
def big_letters(self):
        insult_out = ''
        # Start code block in discord for embedding
        insult_out += ('```py\n')
        # Turn insult input into 5x5 * letters
        for i in range(len(letters['|'])):  
            for j in range(len(self)):       
                insult_out +=  letters[self[j]][i] + "   "#end = " ")
            insult_out += '\n'
        # Finish code block in discord for embedding
        insult_out += ('```')
        return insult_out
    
# Pull insults from html scrape if insult is 12 or less characters ( <=12 is the reasonable limit for a fullscreen 1080p discord application)
def final(self):
        final_list = []
        # Split list of insults by space and output insult with <= 12 characters to list
        for word in result.split(' '):
            if len(word) <= 12:
                final_list.append(word)
            else:
                pass
        # Pick random insult from final list of insults with <= 12 characters
        return random.choice(final_list)
    
