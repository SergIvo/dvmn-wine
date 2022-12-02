from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_year = 1920
current_year = int(datetime.strftime(datetime.now(), '%Y'))
years_existing = current_year - foundation_year

def get_year_word(value):
    single_year_word_forms = {1: 'год', 2: 'года', 3: 'года', 4: 'года'}
    is_tenth_years = (value // 10) == 1
    if not is_tenth_years and value % 10 in single_year_word_forms:
        return single_year_word_forms[value % 10]
    else:
        return 'лет'
        
wine_df = pandas.read_excel('wine.xlsx')
wine_df.columns = ['title', 'sort', 'price', 'image']
wine_cards = wine_df.to_dict(orient='records')

rendered_page = template.render(
    wine_cards = wine_cards,
    existence_time=f'Уже {years_existing} {get_year_word(years_existing)} с вами'
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
print('Starting')
server.serve_forever()
