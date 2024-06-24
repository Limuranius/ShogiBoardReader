from Elements import *
import cv2
import numpy as np
from extra import utils

low = 50
high = 50


def set_low(value):
    global low
    low = value

def set_high(value):
    global high
    high = value

WIN_NAME = "a"
cv2.namedWindow(WIN_NAME)
cv2.createTrackbar("low", WIN_NAME, low, 255, set_low)
cv2.createTrackbar("high", WIN_NAME, high, 255, set_high)

img = cv2.imread(r"D:\Git Projects\ShogiBoardReader\temp\media\images\irl boards\board20.jpg")
img = img[1000:4000]
img = cv2.resize(img, (500, 500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
# gray = cv2.resize(gray, (-1, -1), fx=0.2, fy=0.2)
while True:
    SIZE = 500

    # gray = cv2.resize(gray, (SIZE, SIZE))
    canny = cv2.Canny(gray, low, high)
    # canny = cv2.resize(canny, (SIZE, SIZE))

    cv2.imshow(WIN_NAME, canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
