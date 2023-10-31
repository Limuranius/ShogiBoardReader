import numpy as np
from dataclasses import dataclass
from config import Paths
import pickle
from collections import defaultdict
import os
from .data_info import CATEGORIES_FIGURE_TYPE
from extra import figures
import cv2
import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass
class Dataset:
    _full_data: pd.DataFrame
    _train: pd.DataFrame = None
    _test: pd.DataFrame = None

    def __post_init__(self):
        self.reshuffle(0.2)

    def reshuffle(self, test_size: float):
        self._train, self._test = train_test_split(self._full_data, test_size=test_size)

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

    @property
    def X_train(self):
        return np.array(self._train["image"].to_list())

    @property
    def X_test(self):
        return np.array(self._test["image"].to_list())

    @property
    def y_figure_train(self):
        return np.array(self._train["figure_type"].to_list())

    @property
    def y_figure_test(self):
        return np.array(self._test["figure_type"].to_list())

    @property
    def y_direction_train(self):
        return np.array(self._train["direction"].to_list())

    @property
    def y_direction_test(self):
        return np.array(self._test["direction"].to_list())

    @property
    def train_data(self):
        return self._train

    @property
    def test_data(self):
        return self._test

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
