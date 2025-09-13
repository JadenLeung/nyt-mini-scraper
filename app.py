from bs4 import BeautifulSoup
import requests
import re
import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_crossword():
    response = requests.get("https://dazepuzzle.com/nyt-mini-crossword/")
    soup = BeautifulSoup(response.content, 'html.parser')
    crossword = soup.find('div', class_='cr-crossword-board')
    text = soup.prettify()
    # print(crossword.prettify())

    ul_element = crossword.find('ul')
    style = ul_element['style']
    rows = int(re.search(r'--Grid-Cols:\s*(\d+);', style).group(1))

    grid = [["*" for _ in range(rows)] for _ in range(rows)]
    # print(grid)

    for row in range(rows):
        for col in range(rows):
            div_element = soup.find('div', attrs={'data-index': row * rows + col})
            if div_element['class'][0] != "cr-empty":
                span_element = div_element.find('span')
                grid[row][col] = span_element.get_text()




    hints = soup.find('div', id='tab_clues')
    rownums = list(map(lambda x: x.find('span').get_text(), hints.find_all('div', class_='cr-left')))
    clues = list(map(lambda x: x.find('a').get_text().strip(), hints.find_all('div', class_='cr-right')))
    all_dict = dict(zip(rownums, clues))
    down_dict = {key: value for key, value in all_dict.items() if not str(key).endswith('A')}
    down_dict = {key[:-1]: value.replace(" Crossword Clue", "") for key, value in down_dict.items()}
    across_dict = {key: value for key, value in all_dict.items() if not str(key).endswith('D')}
    across_dict = {key[:-1]: value.replace(" Crossword Clue", "") for key, value in across_dict.items()}
    # print(down_dict)
    # print(across_dict)
    json_dict = json.dumps({"title": "NYT Mini Crossword", "solution": grid, "across": across_dict, "down": down_dict, "message": "Good job!"})
    return json_dict


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/crossword')
def hello_name():
   return get_crossword()

# main driver function
if __name__ == '__main__':
    app.run()
