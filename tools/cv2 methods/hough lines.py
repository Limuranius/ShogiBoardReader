import matplotlib.pyplot as plt

from Elements import *
import cv2
import numpy as np
from extra import utils

RHO = 1
THETA = 180
THRESHOLD = 100


def fit_size(img, h, w):
    size = img.shape[:2]
    f = min(h / size[0], w / size[1])
    return cv2.resize(img, (int(size[1] * f), int(size[0] * f)), interpolation=cv2.INTER_AREA)


def set_low(value):
    global low
    low = value

def set_RHO(value):
    global RHO
    RHO = value

def set_THETA(value):
    global THETA
    THETA = value

def set_THRESHOLD(value):
    global THRESHOLD
    THRESHOLD = value


WIN_NAME = "a"
cv2.namedWindow(WIN_NAME)
cv2.createTrackbar("rho", WIN_NAME, RHO, 10, set_RHO)
cv2.createTrackbar("theta", WIN_NAME, THETA, 360, set_THETA)
cv2.createTrackbar("threshold", WIN_NAME, THRESHOLD, 1000, set_THRESHOLD)

img = cv2.imread(r"D:\Git Projects\ShogiBoardReader\temp\media\images\irl boards\board20.jpg")
# img = img[1000:4000]
img = fit_size(img, 500, 500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(gray, 50, 200)
edges = cv2.dilate(edges, np.ones((3, 3)))
edges = cv2.erode(edges, np.ones((5, 5)))
edges = cv2.dilate(edges, np.ones((3, 3)))

# plt.imshow(edges)
# plt.show()

while True:
    lines = cv2.HoughLines(edges, RHO, np.pi / THETA, THRESHOLD)
    if lines is None:
        lines = []

    img_copy = img.copy()

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow(WIN_NAME, img_copy)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
