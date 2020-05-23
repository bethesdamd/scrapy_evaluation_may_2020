# Get a pdf file from a url, then parse and return its text

from tika import parser
import requests

def get_remote_pdf_text(url):
    # print(f"Getting remote file {url}...")
    text = parser.from_file(url)["content"]
    return text


