# main program to collect pdf's from Arxiv and then get the text of each
# Starts with an API search, which returns an XML Atom response, then iterate
# through each result and GET it from the server.

# NOTE: if you want to save arrays in json that can be ingested into BigQuery,
# e.g. a list of sentences or words, use this kind of file format, with 
# a record per line, this will produce three BigQuery columns, one of type Array:
#  {"one": 1, "two": 2, "arr": [1,2,3]}
#  {"one": 3, "two": 4, "arr": [4,5,6]}

import xml.etree.ElementTree as ET
import re
import json
import requests
from datetime import datetime
import time

# My modules
import pdf_parse as pdf
import prep_text as prep  

# TODO: see https://docs.scrapy.org/en/latest/topics/selectors.html#removing-namespaces
# which shows how to remove namespaces, which would simplify my code
namespace = {'ns': 'http://www.w3.org/2005/Atom'}
MAX_RESULTS = 3   # Resulted in about 2MB of textual data
SLEEP_SECONDS = 0
SUBJECT = "cs.CR"   # Cyber and Crypto Subject is cs.CR
url = f'http://export.arxiv.org/api/query?search_query=all:{SUBJECT}&start=0&max_results={MAX_RESULTS}'

# Accepts an XML ElementTree (I think) and searches for all the pdf's, returning
# a list of dictionaries containing metadata about each pdf 
def get_pdf_urls_from_root(root):
    out = []
    entries = root.findall('ns:entry', namespace)
    for entry in entries:
        d = dict()
        link = entry.find("ns:link/[@title='pdf']", namespace)
        if link is not None:
            d['url'] = link.attrib.get('href')
            d['scraped_timestamp'] = str(datetime.now())
            d['title'] = entry.find("ns:title", namespace).text
            d['published'] = entry.find("ns:published", namespace).text
            d['source'] = "ArXiv"
            out.append(d)
    return out

# Main
if __name__ == "__main__":
    print(f"Making API call to {url} ...")
    root = ET.fromstring(requests.get(url).text)  # This is the first request to get just a list of documents
    dct = dict()
    with open('all.json', 'w', encoding='utf8') as fout:
        for i, info_dict in enumerate(get_pdf_urls_from_root(root)):
            print(i)
            time.sleep(SLEEP_SECONDS)
            url = info_dict['url']
            text = pdf.get_remote_pdf_text(url).strip()  # This is actually GET'ing a PDF and its text
            # Some articles have no PDF content; skip them
            if not text.startswith("No PDF for "):
                text, sentences, words = prep.clean(text)
                print(text)
                info_dict['text'] = text 
                # Write out a single file in "JSON Lines" format (every line is a json object)
                # which is suitable for BigQuery upload manually from a google storage bucket,
                # which is good for testing (until I write directly to the database)
                json.dump(info_dict, fout, ensure_ascii=False)
                fout.write("\n")  
            
