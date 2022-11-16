import csv
import requests
from bs4 import BeautifulSoup
import typer
from aganitha_base_utils import logconfig
from aganitha_base_utils import Config
import logging
import urllib

app = typer.Typer()
logger = logging.getLogger(__name__)
log_settings = Config().params("logging")
logconfig.setup_logging()
logging.basicConfig(filename='page-miner.log', level=logging.DEBUG)


@app.command()
def urls_mine(url_file: str):
    with open(url_file) as files:
        urls: list[str] = [line.rstrip() for line in files]

    titles: list[str] = []
    url_list = []
    for url in urls:
        u = urllib.request.urlopen(url)
        if u.headers.gettype() == 'text/html':
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            titles_h1: str = soup.find('h1').get_text()
            if len(titles_h1) > 1:
                titles.append(titles_h1)
                url_list.append(url)
            elif soup.title is not None:
                titles.append(soup.title.text)
                url_list.append(url)
            else:
                continue
        else:
            logging.info('Not a html/txt page')
            continue

    logging.debug("Writing to csv file Titles.csv")
    with open('Titles.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(("urls", "titles"))
        for i in range(len(url_list)):
            writer.writerow((url_list[i], titles[i]))


if __name__ == '__main__':
    app()
