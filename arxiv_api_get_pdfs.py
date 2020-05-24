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
# a list of URL's to each PDF
def get_pdf_urls_from_tree(tree):
    out = []
    for link_el in tree.findall("ns:entry/ns:link", namespace):
        if link_el.attrib.get('title') == 'pdf':
            out.append(link_el.attrib.get('href'))
    return out

# Main
if __name__ == "__main__":
    print(f"Making API call to {url} ...")
    tree = ET.fromstring(requests.get(url).text)
    dct = dict()
    with open('all.json', 'w', encoding='utf8') as fout:
        for idx, url in enumerate(get_pdf_urls_from_tree(tree)):
            print(url)
            text = pdf.get_remote_pdf_text(url).strip()
            sentences, words = prep.clean(text)
            dct['timestamp'] = str(datetime.now())
            dct['url'] = url
            dct['text'] = text
            # print(json.dumps(dct))        
            # Write out a single file in "JSON Lines" format (every line is a json object)
            # which is suitable for BigQuery upload manually from a google storage bucket,
            # which is good for testing
            json.dump(dct, fout, ensure_ascii=False)
            fout.write("\n")  
            




        