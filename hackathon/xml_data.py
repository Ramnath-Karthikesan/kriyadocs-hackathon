import fitz

doc = fitz.open('test1.pdf')

data = doc[4].get_textbox("html")
print(data)