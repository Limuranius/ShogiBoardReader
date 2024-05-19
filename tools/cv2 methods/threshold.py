from Elements import *
import cv2
import numpy as np
from extra import utils

low = 50
maxval = 255


def set_threshold(value):
    global low
    threshold = value

def set_maxval(value):
    global maxval
    maxval = value


WIN_NAME = "a"
cv2.namedWindow(WIN_NAME)
cv2.createTrackbar("threshold", WIN_NAME, low, 255, set_threshold)
cv2.createTrackbar("maxval", WIN_NAME, maxval, 255, set_maxval)

img = cv2.imread(r"D:\Git Projects\ShogiBoardReader\temp\media\images\irl boards\board20.jpg")
img = img[1000:4000]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.resize(gray, (-1, -1), fx=0.2, fy=0.2)
while True:
    SIZE = 800

    ret, thresh = cv2.threshold(
        gray,
        low,
        maxval,
        cv2.THRESH_BINARY_INV,
    )
    thresh = cv2.resize(thresh, (SIZE, SIZE))

    cv2.imshow(WIN_NAME, thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
