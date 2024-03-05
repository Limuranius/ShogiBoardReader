import Elements
from extra import factories


def corner_detector():
    return [
        (
            "Cool",
            "Universal corner detector.\nUse it if you're unsure what to choose",
            Elements.CoolCornerDetector
        ),
        (
            "Book",
            "Works really good in e-books",
            Elements.BookCornerDetector
        ),
        (
            "HSV Markers",
            "Detects colored markers using HSV thresholding",
            factories.hsv_corner_detector
        ),
        (
            "Hardcoded",
            "Set corners manually. If nothing else is working...",
            Elements.HardcodedCornerDetector
        ),
    ]


def inventory_detector():
    return [
        (
            "None",
            "Don't use inventory detector",
            lambda: None
        ),
        (
            "Book",
            "Detects inventories of e-books' boards",
            Elements.InventoryDetectors.BookInventoryDetector
        ),
    ]


def memorizer():
    return [
        (
            "None",
            "Don't use memorizer",
            lambda: None
        ),
        (
            "Memorizer",
            "Use memorizer",
            Elements.BoardMemorizer
        ),
    ]


def image_getter():
    return [
        (
            "Photo",
            "Photo of board",
            Elements.ImageGetters.Photo
        ),
        (
            "Video",
            "Recorded video of board",
            Elements.ImageGetters.Video
        ),
        (
            "Camera",
            "Use camera connected to computer",
            Elements.ImageGetters.Camera
        ),
    ]
