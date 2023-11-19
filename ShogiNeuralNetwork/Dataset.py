import numpy as np
from dataclasses import dataclass, field
from config import Paths
import pickle
from collections import defaultdict
import os
from extra.image_modes import ImageMode
from .data_info import CATEGORIES_FIGURE_TYPE
from extra import figures
import cv2
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.src.preprocessing.image import ImageDataGenerator


@dataclass
class Dataset:
    _full_data: pd.DataFrame
    """
    Dataframe columns:
        image: np.ndarray
        figure_type: int
        direction: int
    """
    img_mode: ImageMode

    _train: pd.DataFrame = field(init=False)
    _test: pd.DataFrame = field(init=False)
    cell_img_size: int = field(init=False)

    def __post_init__(self):
        self.cell_img_size = self._full_data.iloc[0]["image"].shape[0]
        self.reshuffle(0.2)

    def reshuffle(self, test_size: float):
        self._train, self._test = train_test_split(self._full_data, test_size=test_size)

    def save_to_pickle(self):
        paths = {
            Paths.X_TRAIN_PATH: self.x_train,
            Paths.X_TEST_PATH: self.x_test,
            Paths.Y_FIGURE_TRAIN_PATH: self.y_figure_train,
            Paths.Y_FIGURE_TEST_PATH: self.y_figure_test,
            Paths.Y_DIRECTION_TRAIN_PATH: self.y_direction_train,
            Paths.Y_DIRECTION_TEST_PATH: self.y_direction_test,
        }
        for path in paths:
            with open(path, "wb") as f:
                pickle.dump(paths[path], f)

    @property
    def x_train(self):
        return (np.array(self._train["image"].to_list())
                .reshape((-1, self.cell_img_size, self.cell_img_size, 1)))

    @property
    def x_test(self):
        return (np.array(self._test["image"].to_list())
                .reshape((-1, self.cell_img_size, self.cell_img_size, 1)))

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
        save_data_to_imgs(self.x_test, self.y_figure_test)

    def show_examples(self):
        import cv2
        for fig_type in self._full_data["figure_type"].unique():
            img = self._full_data[self._full_data["figure_type"] == fig_type].iloc[0]["image"]
            cv2.imshow(str(fig_type), img)
        cv2.waitKey(0)

    def get_augmented_data_generator(
            self,
            y_type: str,
            **data_augmentation_params
    ):
        datagen = ImageDataGenerator(
            rescale=1/255,
            **data_augmentation_params
        )
        datagen.fit(self.x_train)
        match y_type:
            case "figure":
                return datagen.flow(self.x_train, self.y_figure_train)
            case "direction":
                return datagen.flow(self.x_train, self.y_direction_train)
            case _:
                raise Exception("Unknown y_type")


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
