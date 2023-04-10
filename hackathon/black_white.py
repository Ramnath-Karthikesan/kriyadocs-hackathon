import fitz
import cv2

page_no = 5
pdffile = "test1.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(page_no-1)  # number of page
pix = page.get_pixmap()
output = "bw.png"
pix.save(output)

image = cv2.imread("bw.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
w, h = gray.shape




cv2.imwrite(f"page{page_no}_bw.png", gray)

blur = cv2.GaussianBlur(gray, (9,9), 0)
cv2.imwrite(f"page{page_no}_blur.png", blur)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
cv2.imwrite(f"page{page_no}_kernel.png", kernel)

# blur = cv2.GaussianBlur(gray, (7,7), 0)
# cv2.imwrite(f"page{page_no}_blur.png", blur)

thresh = cv2.threshold(blur, 0, 255 , cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
cv2.imwrite(f"page{page_no}_thresh.png", thresh)

dilate = cv2.dilate(thresh, kernel, iterations=1)
cv2.imwrite(f"page{page_no}_dilate.png", dilate)

# cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

# coordinates = []
# for c in cnts:
#     x, y, w, h = cv2.boundingRect(c)
#     if h>0 and w>0:
#         print(x, y, w, h)
#         coordinates.append([x, y, w, h])
#         cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 1)

# cv2.imwrite(f"page{page_no}_bbox_1.png", image)

# page0 = doc[page_no-1]
# for i in coordinates:
#     x, y, w, h = i[0], i[1], i[2], i[3]
#     rect = fitz.Rect(x, y, x+w, y+h)  
#     print(f"coordinates : {x} {y} {x+w} {y+h}")
#     text = page.get_textbox(rect)  # get text from rectangle
#     clean_text = ' '.join(text.split())
#     print(clean_text)