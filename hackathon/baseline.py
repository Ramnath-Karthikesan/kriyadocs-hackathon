import fitz
import cv2

def find_margin_width(img, w, h):
    margin_width = [] 
    for i in range(w):
        line_width = 0
        for j in range(h):
            if img[i, j] != 255:
                
                margin_width.append(line_width)
                break
            else:
                line_width += 1
    print(margin_width)
    return min(margin_width)

def check_baseline(filename):
    doc = fitz.open(filename)
    for page_no in range(1,2):
        page = doc.load_page(page_no)
        pix = page.get_pixmap()
        output = "page.png"
        pix.save(output)
        # Read the original image
        image = cv2.imread("page.png")
        rot = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        gray = cv2.cvtColor(rot, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray_scale', gray)
        # cv2.waitKey(0)
        w , h = gray.shape
        # print(w, h)
        left_margin_width = find_margin_width(gray, w, h)

if __name__ == "__main__":
    filename = "test2.pdf"
    check_baseline(filename)