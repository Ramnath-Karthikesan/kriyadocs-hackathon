import fitz
import numpy as np
import re

filepath = 'test4.pdf'

def index_of_uniq(arr):
    count = {}
    for i in arr:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1
    uniq = []
    j = 0
    for i in count:
        if count[i] == 1:
            uniq.append(j)
        j+=1
    return uniq

def check_hf(filepath):
    doc = fitz.open(filepath)
    headers = []
    footers = []
    for page in doc:
        blocks = page.get_text("blocks", sort=True)
        y0, y1 = blocks[0][1], blocks[0][3]
        print(int(y0), int(y1))
        header_width = int(y1)-int(y0)
        headers.append(header_width)
        # print(f"header height: {header_width}")
        y0, y1 = blocks[len(blocks)-1][1], blocks[len(blocks)-1][3]
        footer_width = int(y1)-int(y0)
        print(int(y0), int(y1))
        footers.append(footer_width)
        # print(f"footer height {footer_width}")
    print(headers)
    uniq_header = index_of_uniq(headers)
    if len(uniq_header) > 0:
        print(f"Headers not present in page: {[x+1 for x in uniq_header]}")
    else: 
        print("Headers are present in all pages")

    uniq_footer = index_of_uniq(footers)
    if len(uniq_footer) > 0:
        print(f"Footers not present in page: {[x+1 for x in uniq_footer]}")
    else: 
        print("Footers are present in all pages")

def content_match_hf(filepath):
    doc = fitz.open(filepath)
    for page in doc:
        blocks = page.get_text("blocks", sort=True)
        header_content = blocks[len(blocks)-1][4].replace(" ", "")
        print(bool(re.match(r'[0-9]sampletestcase', "19sampletestcase")))        
        print(header_content)

    
    

if __name__ == "__main__":
    check_hf(filepath)
    # content_match_hf(filepath)
