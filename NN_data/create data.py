import cv2

from reader import ShogiBoardReader
import figures
import os
from collections import defaultdict
import random
import pickle
from data_info import *
from true_boards import TrueFigureTypes, TrueDirections
import numpy as np
import utils
import image_getter
import corner_getter
from config import config
import paths


def save_data_to_pickle(data: dict[str, np.ndarray]):
    for path in data:
        with open(path, "wb") as f:
            pickle.dump(data[path], f)


def save_data_to_imgs(X, y):
    size = y.shape[0]
    count = defaultdict(int)
    for i in range(size):
        img = X[i]
        label = y[i]
        figure = CATEGORIES_FIGURE_TYPE[label]
        count[figure] += 1
        img_name = f"{count[figure]}.jpg"
        path = os.path.join(paths.IMGS_EXAMPLE_DIR, figures.FIGURE_FOLDERS[figure], img_name)
        cv2.imwrite(path, img)


def create_training_data() -> list[tuple[np.ndarray, tuple[int, int]]]:
    """Возвращает данные в виде [(изображение, (индекс типа фигуры, индекс направления))]"""

    training_data = []

    im_getter = image_getter.Photo(None)
    corn_getter = corner_getter.HardcodedCornerDetector(None)
    reader = ShogiBoardReader(
        im_getter,
        corn_getter,
        config
    )

    for img_path in IMGS:
        corners = IMGS_CORNERS[img_path]
        im_getter.set_image(img_path)
        corn_getter.set_corners(corners)

        true_figure_types = TrueFigureTypes.TRUE_BOARDS[img_path]
        true_directions = TrueDirections.TRUE_BOARDS[img_path]

        # Итерируемся по всем клеткам доски
        cells = reader.get_board_cells()
        for i in range(9):
            for j in range(9):
                true_figure = Figure(true_figure_types[i][j])
                true_direction = figures.Direction(true_directions[i][j])

                cell_img = cells[i][j]

                cell_variations = [cell_img]
                for _ in range(config.NN_data.random_translate_repeat):  # random translate
                    max_margin = config.NN_data.random_translate_max_margin
                    trans_img = utils.random_translate_img(cell_img, max_margin, max_margin, fill=0)
                    cell_variations.append(trans_img)

                for _ in range(config.NN_data.random_rotate_repeat):  # random rotate
                    for img in cell_variations[: config.NN_data.random_translate_repeat + 1]:
                        max_angle = config.NN_data.random_rotate_max_angle
                        rot_img = utils.random_rotate_img(img, max_angle, fill=0)
                        cell_variations.append(rot_img)

                figure_label = CATEGORIES_FIGURE_TYPE.index(true_figure)
                direction_label = CATEGORIES_DIRECTION.index(true_direction)
                for img in cell_variations:
                    training_data.append((img, (figure_label, direction_label)))

    random.shuffle(training_data)
    return training_data


def main():
    data = create_training_data()
    size = len(data)
    size_test = int(config.NN_data.test_fraction * size)
    size_train = size - size_test
    X_train = []
    X_test = []
    y_figure_train = []
    y_figure_test = []
    y_direction_train = []
    y_direction_test = []
    for feature, labels in data[:size_test]:
        figure_label, direction_label = labels
        X_test.append(feature)
        y_figure_test.append(figure_label)
        y_direction_test.append(direction_label)
    for feature, labels in data[size_test:]:
        figure_label, direction_label = labels
        X_train.append(feature)
        y_figure_train.append(figure_label)
        y_direction_train.append(direction_label)
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_figure_train = np.array(y_figure_train)
    y_figure_test = np.array(y_figure_test)
    y_direction_train = np.array(y_direction_train)
    y_direction_test = np.array(y_direction_test)

    print("Test size:", size_test)
    print("Train size:", size_train)

    save_data_to_pickle({
        paths.X_TRAIN_PATH: X_train,
        paths.X_TEST_PATH: X_test,
        paths.Y_FIGURE_TRAIN_PATH: y_figure_train,
        paths.Y_FIGURE_TEST_PATH: y_figure_test,
        paths.Y_DIRECTION_TRAIN_PATH: y_direction_train,
        paths.Y_DIRECTION_TEST_PATH: y_direction_test,
    })
    save_data_to_imgs(X_test, y_figure_test)


if __name__ == '__main__':
    main()
