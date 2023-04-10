
import numpy as np
import fitz
import cv2

page_no = 1
pdffile = "test1.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(page_no-1)  # number of page
pix = page.get_pixmap()
output = "bw.png"
pix.save(output)


# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('bw.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

w, h = gray.shape
for i in range(w):
  for j in range(h):
      if gray[i, j] != 255:
        gray[i, j] = 0

blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (7,1))
dilate = cv2.dilate(thresh, kernel, iterations=4)

# Find contours and draw rectangle
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 1)

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey()

cv2.imwrite(f"page{page_no}_bbox_mod.png", image)