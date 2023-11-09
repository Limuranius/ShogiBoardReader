from extra import factories
import cv2
from extra import utils
from extra.image_modes import ImageMode
from config import GLOBAL_CONFIG


def camera():
    reader = factories.get_camera_reader(
        ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode),
        cam_id=0
    )
    size = 700

    while True:
        board_img = reader.get_full_img(show_borders=True)
        predicted_board_img = reader.get_digital_board()
        no_persp = reader.get_board_image_no_perspective()

        board_img = cv2.resize(board_img, (size, size))
        predicted_board_img = cv2.resize(predicted_board_img, (size, size))
        no_persp = cv2.resize(no_persp, (size, size))

        img = cv2.hconcat((
            board_img,
            # no_persp,
            predicted_board_img,
        ))

        cv2.imshow("", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def photo():
    reader = factories.get_hardcoded_reader(
        ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode),
        "board20.jpg"
    )
    board_img = reader.get_board_image_no_perspective()
    predicted_board_img = reader.get_digital_board()
    board_img = cv2.resize(board_img, (600, 600))
    predicted_board_img = cv2.resize(predicted_board_img, (600, 600))
    img = cv2.hconcat((board_img, predicted_board_img))

    cv2.imshow("", img)
    cv2.waitKey(0)


def video():
    reader = factories.get_video_reader(
        ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode),
        "temp/VID_20231103_163606.mp4",
        use_memorizer=True
    )

    while True:
        board_img = reader.get_full_img(show_borders=True)

        board = reader.get_board()
        predicted_board_img = board.to_image()

        no_persp = reader.get_board_image_no_perspective(img_mode=ImageMode.GRAYSCALE_BLACK_THRESHOLD)
        no_persp = utils.gray_to_3d(no_persp)

        no_persp = reader.get_board_image_no_perspective()
        # no_persp = reader.get_board_image_no_perspective()

        board_img = cv2.resize(board_img, (600, 600))
        predicted_board_img = cv2.resize(predicted_board_img, (600, 600))
        no_persp = cv2.resize(no_persp, (600, 600))
        img = cv2.hconcat((
            # board_img,
            no_persp,
            predicted_board_img,
        ))

        cv2.imshow("", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            reader.memorizer.save_to_kifu("/home/gleb/ShogiBoardReader/temp/kifu.kif")
            break
    cv2.destroyAllWindows()


# camera()
# photo()
video()
