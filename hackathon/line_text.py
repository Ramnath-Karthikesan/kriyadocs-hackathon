import fitz

doc = fitz.open('test1.pdf')

data = doc[0].get_text("line")
print(data)