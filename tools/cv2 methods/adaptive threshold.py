from Elements import *
import cv2
import numpy as np
from extra import utils

low = 255
high = 3
C = 1


def set_threshold(value):
    global low
    threshold = value

def set_blockSize(value):
    global high
    blockSize = value

def set_C(value):
    global C
    C = value


WIN_NAME = "a"
cv2.namedWindow(WIN_NAME)
cv2.createTrackbar("threshold", WIN_NAME, low, 255, set_threshold)
cv2.createTrackbar("size", WIN_NAME, high, 50, set_blockSize)
cv2.createTrackbar("C", WIN_NAME, C, 255, set_C)

img = cv2.imread(r"D:\Git Projects\ShogiBoardReader\temp\media\images\irl boards\board20.jpg")
img = img[1000:4000]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.resize(gray, (-1, -1), fx=0.2, fy=0.2)
while True:
    SIZE = 800

    thresh = cv2.adaptiveThreshold(
        gray,
        low,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        high + ((high + 1) % 2),
        C
    )
    thresh = cv2.resize(thresh, (SIZE, SIZE))

    cv2.imshow(WIN_NAME, thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
