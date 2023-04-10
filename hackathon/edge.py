import cv2
import fitz
page_no = 2
pdffile = "test2.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(page_no-1)  # number of page
pix = page.get_pixmap()
output = "page0.png"
pix.save(output)
 
# Read the original image
img = cv2.imread('page0.png') 
# Display original image
# cv2.imshow('Original', img)
# cv2.waitKey(0)
 
# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# w, h = img_gray.shape
# for i in range(w):
#   for j in range(h):
#       if img_gray[i, j] != 255:
#         img_gray[i, j] = 0
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
 
# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=1) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# Display Sobel Edge Detection Images
# cv2.imshow('Sobel x', sobely)
# cv2.waitKey(0)
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 9))
cv2.imwrite("sobelx.png", sobely)
sobelx_img = cv2.imread("sobelx.png")

gray = cv2.cvtColor(sobelx_img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray", gray)
# blur = cv2.GaussianBlur(gray, (7,7), 0)

# thresh = cv2.threshold(blur, 0, 255 , cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
dilate = cv2.dilate(gray, kernel, iterations=1)
# cv2.imshow("dialated", dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h>0 and w>0:
        print(x, y, w, h)
        cv2.rectangle(img, (x, y), (x+w, y+h), (36, 255, 12), 1)
# cv2.imshow('marked', img)
cv2.imwrite(f'page{page_no}_baseline.png', img)
# cv2.imshow('Sobel Y', sobely)
# cv2.waitKey(0)
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# cv2.waitKey(0)
 
# Canny Edge Detection
 # Canny Edge Detection
# Display Canny Edge Detection Image
# cv2.imshow('Canny Edge Detection', edges)
# cv2.waitKey(0)
 
cv2.destroyAllWindows()

page0 = doc[page_no-1]
x, y, w, h = 132, 732, 205, 30
rect = fitz.Rect(x, y, x+w, y+h)  
text = page.get_textbox(rect)  # get text from rectangle
clean_text = ' '.join(text.split())

x, y, w, h = 342, 730, 205, 30
rect = fitz.Rect(x, y, x+w, y+h)  
text = page.get_textbox(rect)  # get text from rectangle
clean_text = ' '.join(text.split())
print(clean_text)

x, y, w, h = 28, 735, 205, 30
rect = fitz.Rect(x, y, x+w, y+h)  
text = page.get_textbox(rect)  # get text from rectangle
clean_text = ' '.join(text.split())
print(clean_text)

