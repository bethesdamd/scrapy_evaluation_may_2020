import xml.etree.ElementTree as ET
import re
import requests
import pdf_parse as pdf

import prep_text as prep

namespace = {'ns': 'http://www.w3.org/2005/Atom'}
MAX_RESULTS = 3
url = f'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results={MAX_RESULTS}'
print(f"Making API call to {url} ...")
tree = ET.fromstring(requests.get(url).text)

def get_pdf_urls_from_tree(tree):
    out = []
    for link_el in tree.findall("ns:entry/ns:link", namespace):
        if link_el.attrib.get('title') == 'pdf':
            out.append(link_el.attrib.get('href'))
    return out


for url in get_pdf_urls_from_tree(tree):
    text = pdf.get_remote_pdf_text(url)
    sentences, words = prep.clean(text)
    print(sentences)
    print(words)



        