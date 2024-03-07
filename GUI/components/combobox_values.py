import Elements
from extra import factories
from extra import utils


def corner_detector():
    return "Corner detector", [
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
    return "Inventory detector", [
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
    return "Memorizer", [
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
    return "Image source", [
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


def cameras():
    return "Camera", [
        (
            str(cam_id),
            f"Camera {cam_id}",
            lambda: Elements.ImageGetters.Camera(cam_id)
        )
        for cam_id in utils.get_available_cam_ids()
    ]

