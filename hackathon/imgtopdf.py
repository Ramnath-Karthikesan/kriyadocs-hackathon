from PIL import Image
import img2pdf
import os
import fitz
import cv2

page_no = 1
pdffile = "test1.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(page_no-1)  # number of page
pix = page.get_pixmap()
output = "page0.png"
pix.save(output)


image = cv2.imread("page0.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
w, h = gray.shape   
for i in range(w):
  for j in range(h):
      if gray[i, j] != 255:
        gray[i, j] = 0
cv2.imwrite(f"bw2.png", gray)

image = Image.open('bw2.png')
pdf_bytes = img2pdf.convert(image.filename)

with open("pdf_bw2.pdf", "wb") as f:
    f.write(pdf_bytes)

doc = fitz.open('pdf_bw2.pdf')
blocks = doc[0].get_text('blocks')
print(blocks)