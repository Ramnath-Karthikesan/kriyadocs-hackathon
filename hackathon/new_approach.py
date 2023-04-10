import cv2

import fitz
page_no = 5
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
cv2.imwrite('bw1.png', gray)
