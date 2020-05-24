# main program to collect pdf's from Arxiv and then get the text of each
# Starts with an API search, which returns an XML Atom response, then iterate
# through each result and GET it from the server.

import xml.etree.ElementTree as ET
import re
import json
import requests
from datetime import datetime

# My modules
import pdf_parse as pdf
import prep_text as prep  

namespace = {'ns': 'http://www.w3.org/2005/Atom'}
MAX_RESULTS = 3
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
            d['title'] = entry.find("ns:title", namespace).text
            d['published'] = entry.find("ns:published", namespace).text
            out.append(d)
    return out

# Main
if __name__ == "__main__":
    print(f"Making API call to {url} ...")
    root = ET.fromstring(requests.get(url).text)  # This is the first request to get just a list of documents
    dct = dict()
    with open('all.json', 'w', encoding='utf8') as fout:
        for info_dict in get_pdf_urls_from_root(root):
            url = info_dict['url']
            text = pdf.get_remote_pdf_text(url).strip()  # This is actually GET'ing a PDF and its text
            sentences, words = prep.clean(text)
            dct['timestamp'] = str(datetime.now())
            dct['title'] = info_dict['title']
            dct['published'] = info_dict['published']
            dct['url'] = url
            dct['text'] = text
            
            # print(json.dumps(dct))        
            # Write out a single file in "JSON Lines" format (every line is a json object)
            # which is suitable for BigQuery upload manually from a google storage bucket,
            # which is good for testing
            json.dump(dct, fout, ensure_ascii=False)
            fout.write("\n")  
            
