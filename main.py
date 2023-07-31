import factories
import cv2
import utils


def camera():
    reader = factories.get_camera_reader()

    while True:
        board_img = reader.get_full_img_with_borders()
        predicted_board_img = reader.get_digital_board()

        no_persp = reader.get_board_image()

        board_img = cv2.resize(board_img, (800, 800))
        predicted_board_img = cv2.resize(predicted_board_img, (800, 800))
        no_persp = cv2.resize(no_persp, (800, 800))
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
    reader = factories.get_hardcoded_reader()
    board_img = reader.get_board_image()
    predicted_board_img = reader.get_digital_board()
    board_img = cv2.resize(board_img, (800, 800))
    predicted_board_img = cv2.resize(predicted_board_img, (800, 800))
    img = cv2.hconcat((board_img, predicted_board_img))

    cv2.imshow("", img)
    cv2.waitKey(0)


def video():
    reader = factories.get_video_reader(
        "temp/img/VID_20230731_160231.mp4"
    )

    while True:
        board_img = reader.get_full_img_with_borders()
        predicted_board_img = reader.get_digital_board()

        no_persp = reader.get_board_image()

        board_img = cv2.resize(board_img, (800, 800))
        predicted_board_img = cv2.resize(predicted_board_img, (800, 800))
        no_persp = cv2.resize(no_persp, (800, 800))
        img = cv2.hconcat((
            board_img,
            # no_persp,
            predicted_board_img,
        ))

        cv2.imshow("", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


# camera()
photo()
# video()
