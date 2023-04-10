import fitz

filepath = 'test1.pdf'
doc = fitz.open(filepath)

page_no = []
j = 0 
for page in doc :
    j += 1
    blocks = page.get_text("blocks", sort=True)

    content = ""
    for i in range(len(blocks)):
        line = blocks[i][4]
        if(line[1:6] != "image"):
            content += line

    content_list = content.split('\n')
    if len(content_list) < 5:
        page_no.append(j)

if(len(page_no)) > 0:
    print(f"Alert: min no of lines test case failed at page {page_no}")
else:
    print("Success: min no of lines test case passed")