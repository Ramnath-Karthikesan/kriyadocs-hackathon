import fitz
from operator import itemgetter

def index_of_uniq(arr):
    count = {}
    for i in arr:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1
    uniq = []
    j = 1
    for i in count:
        if count[i] == 1:
            uniq.append(j)
        j+=1
    return uniq

def get_parafont(doc, granularity=False):
    styles = {}
    font_counts = {}
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if granularity:
                            identifier = "{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                            styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                                  'color': s['color']}
                        else:
                            identifier = "{0}".format(int(s['size']))
                            styles[identifier] = {'size': int(s['size']), 'font': s['font']}

                        font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage

    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles

def get_pagefont(doc, granularity, page_no):
    styles = {}
    font_counts = {}
    blocks = doc[page_no].get_text("dict")["blocks"]
    for b in blocks:  # iterate through the text blocks
        if b['type'] == 0:  # block contains text
            for l in b["lines"]:  # iterate through the text lines
                for s in l["spans"]:  # iterate through the text spans
                    if granularity:
                        identifier = "{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                        styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                              'color': s['color']}
                    else:
                        identifier = "{0}".format(int(s['size']))
                        styles[identifier] = {'size': int(s['size']), 'font': s['font']}
                    font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage
    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles

def get_potential_hf(doc, index):
    font_counts, styles = get_parafont(doc)
    major_size = int((font_counts[0][0]))
    ind = 0
    flag = 0
    major_font = (styles[str(major_size)]['font'])
    msg = ""
    if index == 0:
        msg = "header"
    else:
        msg = "footer"
    for page in doc:
        ind += 1
        blocks = page.get_text("dict", sort=True)["blocks"]
        index = len(blocks)-1 if index != 0 else 0
        if "image" not in blocks[index]:
            size = blocks[index]['lines'][0]['spans'][0]['size']
            font = blocks[index]['lines'][0]['spans'][0]['font']
            if size != major_size and font != major_font:
                flag = 1
                blocks = page.get_text('blocks', sort=True)
                data = blocks[index][4]
                # print(blocks[index])
                if data.isspace():
                    flag = 0
                    continue
                info = (data[:75] + '..') if len(data) > 75 else data
                print(f"potential {msg} found at page {ind}: {info}\n")
        else:
            flag = 1
            print(f"Found an image as {msg} at page {ind}\n")
            
    print("====================================================================")

    if flag == 0:
        print(f"No {msg} found at any pages")
        return -1
    else:
        return 1
    
def get_hf_index(doc, uniq_header, uniq_footer):
    if len(uniq_header) == len(doc) and len(uniq_footer) == len(doc):
        print("Didn't find any unique header or footer ")
        print("Searching for possible headers and footers ...")
        h_flag = get_potential_hf(doc, 0)
        f_flag = get_potential_hf(doc, -1)
        if h_flag == 1 and f_flag == 1:
            print("Enter the page no: ")
            page_no = int(input())
            if page_no > len(doc):
                print("Invalid page no entered")
            else:
                uniq_header.remove(page_no)
                uniq_footer.remove(page_no)
                get_hf_index(doc, uniq_header, uniq_footer)
        else:
            if h_flag == -1 and f_flag == -1:
                print("No headers and footers found")
            elif h_flag == -1:
                print("No headers found")
            else:
                print("No footers found")
    elif len(uniq_header) == 0 and  len(uniq_footer) == 0:
        print("Header and footer present at all pages")
    else:
        print(f"missing headers at page: {uniq_header}")
        print(f"missing footers at page: {uniq_footer}")
    return uniq_header, uniq_footer



def check_hf(doc):
    headers = []
    footers = []
    for page in doc:
        blocks = page.get_text("blocks", sort=True)
        y0, y1 = int(blocks[0][1]), int(blocks[0][3])
        headers.append((y0, y1))
        y0, y1 = int(blocks[len(blocks)-1][1]), int(blocks[len(blocks)-1][3])
        footers.append((y0, y1))
    # print(headers)
    # print(footers)
    uniq_header = index_of_uniq(headers)
    uniq_footer = index_of_uniq(footers)
    # checking font related info only if the header starting and ending postion mismatches in all pages
    no_header, no_footer = get_hf_index(doc, uniq_header, uniq_footer)
    return no_header, no_footer


def check_font_family(doc):
    invalid_font = []
    for page in range(len(doc)):
        _, fonts = get_pagefont(doc, True, page)
        valid_fonts = ['classicalgaramond', 'frutigerltpro', 'frutigerltstd', 'symbol', 'timesnewroman', 'times new roman', 'arial']
        font_list = []
        for i in fonts:
            if fonts[i]['font'].split('-')[0].lower() not in font_list:
                font_list.append(fonts[i]['font'].split('-')[0].lower())
        # print(font_list)
        for font in font_list:
            flag = 0
            for valid_font in valid_fonts:
                if font.startswith(valid_font):
                    flag = 1
            if flag == 0:
                invalid_font.append({"page_no": str(page+1),"font_family": font})
    if len(invalid_font) > 0:
        print(f"Found invalid font {invalid_font}")
    else:
        print(f"Font check passed! All fonts used are valid.")

def check_minlines_blank(doc, no_header, no_footer):
    min_lines = [] 
    blank_page = []
    for page in range(len(doc)):
        image_flag = 0
        blocks = doc[page].get_text("blocks", sort=True)
        if page not in no_header:
            blocks.pop(0)
        if page not in no_footer:
            blocks.pop(len(blocks)-1)
        content = ""
        for i in range(len(blocks)):
            line = blocks[i][4]
            if(line[1:6] != "image"):
                content += line
            else:
                image_flag += 1
        content_list = content.split('\n')
        
        content_list = [data.strip() for data in content_list]
        while("" in content_list):
            content_list.remove("")
        if len(content_list) < 5:
            min_lines.append(page+1)
        if len(content_list) == 0 and image_flag == 0:
            blank_page.append(page+1)
    
    if len(min_lines) > 0:
        print(f"Minimum no of lines test failed at pages: {min_lines}")
    else:
        print("Minimum no of lines test case passed")
    
    if len(blank_page) > 0:
        print(f"Blank page found at pages: {blank_page}")
    else:
        print("Blank page test case passed")
    
        
def check_short_column(doc):
    print("\n")
    for page in range(4,5):
        # blocks = doc[page].get_text("blocks", sort=True)
        # print(blocks[len(blocks)-1])
        # print("\n")
        # print(blocks[len(blocks)-2])
        blocks = doc[4].get_text("blocks", sort=True)
        print(blocks[len(blocks)-3])
        print("\n")
        print(blocks[0])
        print("\n")
        print(blocks[len(blocks)-1])
        # print("\n")
        # print(blocks[len(blocks)-4])

if __name__ == "__main__":
    filepath = 'test1.pdf'
    
    # try:
    #     doc = fitz.open(filepath)
    #     print("\nGenerating Report... \n")
    #     check_font_family(doc)
    #     no_header, no_footer = check_hf(doc)
    #     check_minlines_blank(doc, no_header, no_footer)
    # except:
    #     print("Error Occured while genrating report")
    doc = fitz.open(filepath)
    check_short_column(doc)
    
    
    

