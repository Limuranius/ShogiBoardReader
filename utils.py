import numpy as np
import cv2
import random
import figures


def get_black_mask(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    min_value = 100
    ret, thresh = cv2.threshold(gray, min_value, 255, cv2.THRESH_BINARY)
    return thresh


def tweak_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.resize(gray, (800, 800))
    canny = cv2.Canny(gray, 150, 200)
    r = [0, 255]

    def low(value):
        r[0] = value
        cv2.imshow("edges", cv2.Canny(gray, *r))

    def high(value):
        r[1] = value
        cv2.imshow("edges", cv2.Canny(gray, *r))

    cv2.imshow("edges", canny)
    cv2.createTrackbar("lower", "edges", 0, 255, low)
    cv2.createTrackbar("higher", "edges", 255, 255, high)
    cv2.waitKey(0)


def show_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    cv2.waitKey(0)


def translate_img(img, dx, dy, fill=255):
    """Сдвигает изображение img на (dx, dy) пикселей и заполняет освободившиеся пиксели значением fill"""
    height, width = img.shape[:2]
    T = np.float32([[1, 0, dx], [0, 1, dy]])
    img_translation = cv2.warpAffine(img, T, (width, height))
    if dx >= 0:
        img_translation[:, :dx] = fill
    else:
        img_translation[:, dx:] = fill
    if dy >= 0:
        img_translation[:dy, :] = fill
    else:
        img_translation[dy:, :] = fill
    return img_translation


def rotate_img(img, angle, fill):
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_img = cv2.warpAffine(img, M, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=fill)
    return rotated_img


def random_translate_img(img, sx: float, sy: float, fill=255):
    """Сдвигает изображение в случайном направлении максимум на sx по оси OX и на sy по оси OY
    sx, sy: [0, 1] и заполняет освободившиеся пиксели значением fill"""
    height, width = img.shape[:2]
    max_dx = int(width * sx)
    max_dy = int(height * sy)
    dx = random.randint(-max_dx, max_dx)
    dy = random.randint(-max_dy, max_dy)
    return translate_img(img, dx, dy, fill)


def random_rotate_img(img, max_angle, fill):
    angle = random.randint(-max_angle, max_angle)
    return rotate_img(img, angle, fill)


def order_points(pts: np.ndarray):
    rect = np.zeros((4, 2), dtype=pts.dtype)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def remove_perspective(img: np.ndarray, corners: np.ndarray):
    (tl, tr, br, bl) = order_points(corners)
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    corners = corners.astype("float32")
    M = cv2.getPerspectiveTransform(corners, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    return warped


def find_clusters_centers(mask: np.ndarray, k_clusters: int) -> np.ndarray:
    """Применяет кластеризацию k-means к маске mask, чтобы найти центры k_clusters кластеров"""
    nz = cv2.findNonZero(mask)
    if nz is None or len(nz) < k_clusters:
        return np.array([(0, 0)] * k_clusters)
    nz = nz.reshape(-1, 2).astype("float32")
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, centers = cv2.kmeans(nz, k_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = centers.astype("int32")
    return centers


def overlay_image_on_image(img: np.ndarray, img_overlay: np.ndarray, x: int, y: int):
    """Накладывает изображение img_overlay на изображение img в координате (x, y)"""
    x1 = x + img_overlay.shape[1]
    y1 = y + img_overlay.shape[0]
    img[y: y1, x: x1] = img_overlay
    return img
