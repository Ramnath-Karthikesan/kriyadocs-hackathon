import pytesseract
import cv2

import fitz
page_no = 2
pdffile = "test2.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(page_no-1)  # number of page
pix = page.get_pixmap()
output = "page0.png"
pix.save(output)


image = cv2.imread("page0.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# w, h = gray.shape   
# for i in range(w):
#   for j in range(h):
#       if gray[i, j] != 255:
#         gray[i, j] = 0
cv2.imwrite(f"page{page_no}_gray_1.png", gray)
blur = cv2.GaussianBlur(gray, (7,7), 0)
cv2.imwrite(f"page{page_no}_blur_1.png", blur)

thresh = cv2.threshold(blur, 0, 255 , cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
cv2.imwrite(f"page{page_no}_thresh_1.png", thresh)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 9))
cv2.imwrite(f"page{page_no}_kernel_1.png", kernel)

dilate = cv2.dilate(thresh, kernel, iterations=1)
cv2.imwrite(f"page{page_no}_dilate_1.png", dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h>0 and w>0:
        print(x, y, w, h)
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 1)

cv2.imwrite(f"page{page_no}_bbox_2.png", image)

# page0 = doc[4]
# x, y, w, h = 144, 471, 200, 282
# rect = fitz.Rect(x, y, x+w, y+h)  
# text = page.get_textbox(rect)  # get text from rectangle
# clean_text = ' '.join(text.split())

# print(clean_text)


doc.close()

