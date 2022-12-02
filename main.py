from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_year = 1920
current_year = int(datetime.strftime(datetime.now(), '%Y'))

rendered_page = template.render(
    existence_time=f'Уже {current_year - foundation_year} лет с вами'
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
print('Starting')
server.serve_forever()
