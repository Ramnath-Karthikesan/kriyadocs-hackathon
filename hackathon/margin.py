import cv2
import fitz

def get_freq(arr):
    freq = {}
    for i in arr:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

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
    # print(margin_width)
    # freq = get_freq(margin_width)
    # print(freq)
    # print(max(freq.values()))
    return min(margin_width)

def check_margin(filename):
    doc = fitz.open(filename)
    for page_no in range(len(doc)):
        page = doc.load_page(page_no)
        pix = page.get_pixmap()
        output = "page.png"
        pix.save(output)
        # Read the original image
        image = cv2.imread("page.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray_scale', gray)
        # cv2.waitKey(0)
        w , h = gray.shape
        # print(w, h)
        left_margin_width = find_margin_width(gray, w, h)
        gray_h = cv2.flip(gray, 1)
        right_margin_width = find_margin_width(gray_h, w, h)
        print(f"page{page_no+1} - left margin width: {left_margin_width} and right margin width: {right_margin_width}")
        if left_margin_width <= right_margin_width:
            print("margin width test case passed")
        else:
            print("margin width does not match or content exceeding margin")
            

if __name__ == "__main__":
    filename = "test15.pdf"
    check_margin(filename)
    

