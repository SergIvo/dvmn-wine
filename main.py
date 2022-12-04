from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from collections import defaultdict

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_word(value):
    single_year_word_forms = {1: 'год', 2: 'года', 3: 'года', 4: 'года'}
    is_tenth_years = (value // 10) == 1
    if not is_tenth_years and value % 10 in single_year_word_forms:
        return single_year_word_forms[value % 10]
    else:
        return 'лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    foundation_year = 1920
    current_year = datetime.now().year
    winery_age = current_year - foundation_year
        
    drink_df = pandas.read_excel('wine3.xlsx')
    drink_df.columns = ['category', 'title', 'sort', 'price', 'image', 'profitable']
    drink_df.fillna('', inplace=True)
    drink_cards = drink_df.to_dict(orient='records')

    drink_cards_grouped = defaultdict(list)
    for card in drink_cards:
        drink_cards_grouped[card['category']].append(card)

    rendered_page = template.render(
        drink_cards = drink_cards_grouped,
        existence_time=f'Уже {winery_age} {get_year_word(winery_age)} с вами'
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
    
    
if __name__ == '__main__':
    main()

