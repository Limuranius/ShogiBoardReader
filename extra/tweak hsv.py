from config import GLOBAL_CONFIG
from Elements import *
import cv2
import numpy as np
from extra import utils

TWEAKS_WIN_NAME = "tweaks"
HSV_WIN_NAME = "hsv threshold"
CANNY_WIN_NAME = "canny"
ORIGINAL_WIN_NAME = "original"
NO_PERSP_WIN_NAME = "no perspective"


def is_win_open(win_name: str):
    return cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) >= 1


def h_low(value):
    GLOBAL_CONFIG.HSVThreshold.h_low = value


def h_high(value):
    GLOBAL_CONFIG.HSVThreshold.h_high = value


def s_low(value):
    GLOBAL_CONFIG.HSVThreshold.s_low = value


def s_high(value):
    GLOBAL_CONFIG.HSVThreshold.s_high = value


def v_low(value):
    GLOBAL_CONFIG.HSVThreshold.v_low = value


def v_high(value):
    GLOBAL_CONFIG.HSVThreshold.v_high = value


def show_orig_img(value):
    GLOBAL_CONFIG.Tweaks.show_orig_img = value


def show_hsv_mask(value):
    GLOBAL_CONFIG.Tweaks.show_hsv_mask = value


def show_canny(value):
    GLOBAL_CONFIG.Tweaks.show_canny = value


def canny_low(value):
    GLOBAL_CONFIG.Tweaks.canny_low = value


def canny_high(value):
    GLOBAL_CONFIG.Tweaks.canny_high = value


def img_scale(value):
    GLOBAL_CONFIG.Tweaks.img_scale = value


def get_hsv_mask(orig_img):
    img_hsv = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)

    low = np.array([
        GLOBAL_CONFIG.HSVThreshold.h_low,
        GLOBAL_CONFIG.HSVThreshold.s_low,
        GLOBAL_CONFIG.HSVThreshold.v_low,
    ])

    high = np.array([
        GLOBAL_CONFIG.HSVThreshold.h_high,
        GLOBAL_CONFIG.HSVThreshold.s_high,
        GLOBAL_CONFIG.HSVThreshold.v_high,
    ])
    mask = cv2.inRange(img_hsv, low, high)
    return mask


def get_canny(img):
    low = GLOBAL_CONFIG.Tweaks.canny_low
    high = GLOBAL_CONFIG.Tweaks.canny_high
    return cv2.Canny(img, low, high)


def setup_windows():
    cv2.namedWindow(TWEAKS_WIN_NAME)
    cv2.namedWindow(HSV_WIN_NAME)
    cv2.namedWindow(CANNY_WIN_NAME)
    cv2.namedWindow(ORIGINAL_WIN_NAME)
    cv2.namedWindow(NO_PERSP_WIN_NAME)

    cv2.createTrackbar("show original image", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.show_orig_img, 1, show_orig_img)
    cv2.createTrackbar("show hsv mask", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.show_hsv_mask, 1, show_hsv_mask)
    cv2.createTrackbar("show canny", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.show_canny, 1, show_canny)
    cv2.createTrackbar("img_scale", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.img_scale, 100, img_scale)

    # cv2.createTrackbar("h_low", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.h_low, 180, h_low)
    # cv2.createTrackbar("h_high", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.h_high, 180, h_high)
    # cv2.createTrackbar("s_low", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.s_low, 255, s_low)
    # cv2.createTrackbar("s_high", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.s_high, 255, s_high)
    # cv2.createTrackbar("v_low", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.v_low, 255, v_low)
    # cv2.createTrackbar("v_high", HSV_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.v_high, 255, v_high)
    #
    # cv2.createTrackbar("low", CANNY_WIN_NAME, GLOBAL_CONFIG.Tweaks.canny_low, 255, canny_low)
    # cv2.createTrackbar("high", CANNY_WIN_NAME, GLOBAL_CONFIG.Tweaks.canny_high, 255, canny_high)

    cv2.createTrackbar("h_low", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.h_low, 180, h_low)
    cv2.createTrackbar("h_high", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.h_high, 180, h_high)
    cv2.createTrackbar("s_low", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.s_low, 255, s_low)
    cv2.createTrackbar("s_high", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.s_high, 255, s_high)
    cv2.createTrackbar("v_low", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.v_low, 255, v_low)
    cv2.createTrackbar("v_high", TWEAKS_WIN_NAME, GLOBAL_CONFIG.HSVThreshold.v_high, 255, v_high)
    cv2.createTrackbar("low", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.canny_low, 255, canny_low)
    cv2.createTrackbar("high", TWEAKS_WIN_NAME, GLOBAL_CONFIG.Tweaks.canny_high, 255, canny_high)


def main():
    setup_windows()

    img_get = ImageGetters.Camera()
    corn_get = CornerGetters.HSVThresholdCornerDetector(None, None)

    while True:
        hsv_low = np.array([
            GLOBAL_CONFIG.HSVThreshold.h_low,
            GLOBAL_CONFIG.HSVThreshold.s_low,
            GLOBAL_CONFIG.HSVThreshold.v_low,
        ])
        hsv_high = np.array([
            GLOBAL_CONFIG.HSVThreshold.h_high,
            GLOBAL_CONFIG.HSVThreshold.s_high,
            GLOBAL_CONFIG.HSVThreshold.v_high,
        ])
        corn_get.hsv_low = hsv_low
        corn_get.hsv_high = hsv_high

        orig_img = img_get.get_image()
        orig_img = cv2.resize(orig_img, (-1, -1), fx=GLOBAL_CONFIG.Tweaks.img_scale / 100, fy=GLOBAL_CONFIG.Tweaks.img_scale / 100)
        hsv_mask = get_hsv_mask(orig_img)
        hsv_masked_img = cv2.bitwise_and(orig_img, orig_img, mask=hsv_mask)
        corners = np.array(corn_get.get_corners(orig_img))
        for x, y in corners:
            cv2.circle(hsv_masked_img, (x, y), 3, [0, 0, 255], thickness=-1)
        cv2.polylines(hsv_masked_img, [corners], True, [255, 255, 255], thickness=1)

        no_persp = utils.remove_perspective(orig_img, corners)

        canny = get_canny(orig_img)
        if GLOBAL_CONFIG.Tweaks.show_orig_img:
            cv2.imshow(ORIGINAL_WIN_NAME, orig_img)
        elif is_win_open(ORIGINAL_WIN_NAME):
            cv2.destroyWindow(ORIGINAL_WIN_NAME)
        if GLOBAL_CONFIG.Tweaks.show_hsv_mask:
            cv2.imshow(HSV_WIN_NAME, hsv_masked_img)
        elif is_win_open(HSV_WIN_NAME):
            cv2.destroyWindow(HSV_WIN_NAME)
        if GLOBAL_CONFIG.Tweaks.show_canny:
            cv2.imshow(CANNY_WIN_NAME, canny)
        elif is_win_open(CANNY_WIN_NAME):
            cv2.destroyWindow(CANNY_WIN_NAME)
        cv2.imshow(TWEAKS_WIN_NAME, np.zeros((100, 500)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
