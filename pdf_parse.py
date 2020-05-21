# Get a pdf file from a url, then parse and return its text

from tika import parser
import requests

def get_remote_pdf_text(url):
    print(f"Getting remote file {url}...")
    f = requests.get(url)
    print("got file")
    raw = parser.from_buffer(f)
    text = raw['content']
    return text


