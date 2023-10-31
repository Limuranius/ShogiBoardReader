import numpy as np
from dataclasses import dataclass
from config import Paths
import pickle
from collections import defaultdict
import os
from .data_info import CATEGORIES_FIGURE_TYPE
from extra import figures
import cv2


@dataclass(frozen=True)
class Dataset:
    X_train: np.ndarray
    X_test: np.ndarray
    y_figure_train: np.ndarray
    y_figure_test: np.ndarray
    y_direction_train: np.ndarray
    y_direction_test: np.ndarray

    def save_to_pickle(self):
        paths = {
            Paths.X_TRAIN_PATH: self.X_train,
            Paths.X_TEST_PATH: self.X_test,
            Paths.Y_FIGURE_TRAIN_PATH: self.y_figure_train,
            Paths.Y_FIGURE_TEST_PATH: self.y_figure_test,
            Paths.Y_DIRECTION_TRAIN_PATH: self.y_direction_train,
            Paths.Y_DIRECTION_TEST_PATH: self.y_direction_test,
        }
        for path in paths:
            with open(path, "wb") as f:
                pickle.dump(paths[path], f)

    def save_to_img(self):
        save_data_to_imgs(self.X_test, self.y_figure_test)


def save_data_to_imgs(X, y):
    size = y.shape[0]
    count = defaultdict(int)
    for i in range(size):
        img = X[i]
        label = y[i]
        figure = CATEGORIES_FIGURE_TYPE[label]
        count[figure] += 1
        img_name = f"{count[figure]}.jpg"
        path = os.path.join(Paths.IMGS_EXAMPLE_DIR, figures.FIGURE_FOLDERS[figure], img_name)
        cv2.imwrite(path, img)
