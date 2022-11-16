"""This is the example of a module. Please write the documentation along with your code."""
import logging

import requests
from aganitha_base_utils import logconfig
from aganitha_base_utils import Config
import os
import urllib
import typer

app = typer.Typer()

logger = logging.getLogger(__name__)
log_settings = Config().params("logging")
logconfig.setup_logging()


# def uri_exists_stream(uri: str) -> bool:
#     try:
#         with requests.get(uri) as response:
#             try:
#                 response.raise_for_status()
#                 return True
#             except requests.exceptions.HTTPError:
#                 return False
#     except requests.exceptions.ConnectionError:
#         return False


@app.command()
def download(input_file: str, output_dir: str):
    print(input_file)
    with open(input_file) as files:
        urls1: list[str] = [line.rstrip() for line in files]
    
    output_path: str = '/Users/amani/Documents/'+str(output_dir)+'/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)  # create folder if it does not exist

    for url in urls1:
        # r = requests.get(url)
        file_name: str = str(urls1.index(url)+1)+'.txt'
        file_path: str = os.path.join(output_path, file_name)
        # status = uri_exists_stream(url)
        ret = requests.head(url)
        print(ret.status_code)
        if ret.status_code < 400:
            urllib.request.urlretrieve(url, file_path)
            print("Writing to file: ", file_path)
        else:
            print("Website doesn't exists")
        

if __name__ == '__main__':
    app()
