from __future__ import annotations

import os.path
import pickle
from collections import defaultdict

import cv2
import tensorflow as tf
import numpy as np
import pandas as pd
import tqdm
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from ShogiNeuralNetwork.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
from config import GLOBAL_CONFIG, Paths
from extra.image_modes import ImageMode
from extra.types import ImageNP, Figure, Direction
import imagehash
from PIL import Image
from . import preprocessing


def equalize_classes(data: pd.DataFrame) -> pd.DataFrame:
    shuffled_data = shuffle(data)
    classes_counts = shuffled_data["figure_type"].value_counts()
    min_count = classes_counts.min() * 3
    del_indices = []
    for i, row in shuffled_data.iterrows():
        if classes_counts[row["figure_type"]] > min_count:
            del_indices.append(i)
            classes_counts[row["figure_type"]] -= 1
    new_data = data.drop(index=del_indices)
    return new_data


def enums_to_labels(data: pd.DataFrame) -> pd.DataFrame:
    new_data = data.copy()
    new_data["figure_type"] = new_data["figure_type"].apply(lambda f: CATEGORIES_FIGURE_TYPE.index(f))
    new_data["direction"] = new_data["direction"].apply(lambda d: CATEGORIES_DIRECTION.index(d))
    return new_data


def reshape_imgs(data: pd.DataFrame) -> pd.DataFrame:
    """Converts all SIZE x SIZE images to SIZE x SIZE x 1"""
    new_data = data.copy()
    new_data["image"] = new_data["image"].apply(preprocessing.reshape_image)
    return new_data


class CellsDataset:
    __visited_images_hashes: set[imagehash.ImageHash]

    __data: pd.DataFrame
    """
    Dataframe columns:
        image: np.ndarray
        figure_type: Figure
        direction: Direction
    """

    def __init__(self, data: pd.DataFrame = None):
        self.__data = data

    def is_image_visited(self, path: str) -> bool:
        img = Image.open(path)
        img_hash = imagehash.average_hash(img)
        return img_hash in self.__visited_images_hashes

    def add_image_hash(self, path: str) -> None:
        img = Image.open(path)
        img_hash = imagehash.average_hash(img)
        self.__visited_images_hashes.add(img_hash)

    def load_pickle(self, path: str):
        if os.path.exists(path):
            with open(path, "rb") as f:
                pkl_data = pickle.load(f)
                self.__data = pkl_data[0]
                self.__visited_images_hashes = pkl_data[1]
        else:
            self.__data = pd.DataFrame(columns=["image", "figure_type", "direction"])
            self.__visited_images_hashes = set()

    def save_pickle(self, path: str):
        with open(path, "wb") as f:
            pkl_data = [self.__data, self.__visited_images_hashes]
            pickle.dump(pkl_data, f)

    def add_image(self, cell_img: ImageNP, figure: Figure, direction: Direction):
        self.__data.loc[len(self.__data)] = [cell_img, figure, direction]

    def convert(
            self,
            image_mode: ImageMode,
    ) -> CellsDataset:
        def func(img):
            return image_mode.convert_image(img)

        new_data = self.__data.copy()
        new_data["image"] = new_data["image"].apply(func)
        return CellsDataset(new_data)

    def resize(self, size: tuple[int, int]) -> CellsDataset:
        def func(img):
            return cv2.resize(img, size)

        new_data = self.__data.copy()
        new_data["image"] = new_data["image"].apply(func)
        return CellsDataset(new_data)

    def __prepare_1(self) -> pd.DataFrame:
        new_data = self.__data
        # new_data = equalize_classes(new_data)
        new_data = enums_to_labels(new_data)
        new_data = reshape_imgs(new_data)
        return new_data

    def __to_tf_dataset(self) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        data = self.__prepare_1()
        train, test = train_test_split(data, test_size=GLOBAL_CONFIG.NeuralNetwork.test_fraction)

        train_images = np.array(train["image"].tolist())
        train_figure_labels = train["figure_type"].to_numpy()
        train_direction_labels = train["direction"].to_numpy()

        test_images = np.array(test["image"].tolist())
        test_figure_labels = test["figure_type"].to_numpy()
        test_direction_labels = test["direction"].to_numpy()

        train_tf = tf.data.Dataset.from_tensor_slices(
            (
                train_images,
                train_figure_labels,
                train_direction_labels
            )
        )

        test_tf = tf.data.Dataset.from_tensor_slices(
            (
                test_images,
                test_figure_labels,
                test_direction_labels
            )
        )

        return train_tf, test_tf

    def __prepare_train(self, ds: tf.data.Dataset) -> tf.data.Dataset:
        train_ds = (
            ds
            .shuffle(ds.cardinality())
            .batch(GLOBAL_CONFIG.NeuralNetwork.batch_size)
            .map(lambda img, figure, direction:
                 (preprocessing.resize_and_rescale(img), figure, direction))
            .map(lambda img, figure, direction:
                 (preprocessing.augment(img), figure, direction))
        )
        return train_ds

    def __prepare_test(self, ds: tf.data.Dataset) -> tf.data.Dataset:
        test_ds = (
            ds
            .batch(GLOBAL_CONFIG.NeuralNetwork.batch_size)
            .map(lambda img, figure, direction:
                 (preprocessing.resize_and_rescale(img), figure, direction))
        )
        return test_ds

    def __chose_column(self, ds: tf.data.Dataset, column: str) -> tf.data.Dataset:
        match column:
            case "figure_type":
                return ds.map(lambda img, f, d: (img, f))
            case "direction":
                return ds.map(lambda img, f, d: (img, d))
            case _:
                raise Exception("WRONG COLUMN!!!")

    def get_figure_tf_dataset(self) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        train, test = self.__to_tf_dataset()

        train = self.__prepare_train(train)
        train = self.__chose_column(train, "figure_type")

        test = self.__prepare_test(test)
        test = self.__chose_column(test, "figure_type")

        return train, test

    def get_direction_tf_dataset(self) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        train, test = self.__to_tf_dataset()

        train = self.__prepare_train(train)
        train = self.__chose_column(train, "direction")

        test = self.__prepare_test(test)
        test = self.__chose_column(test, "direction")

        return train, test

    def save_images(self):
        count = defaultdict(int)
        for _, row in tqdm.tqdm(self.__data.iterrows()):
            img = row["image"]
            figure = row["figure_type"]
            count[figure] += 1
            img_name = f"{count[figure]}.jpg"
            os.makedirs(os.path.join(Paths.IMGS_EXAMPLE_DIR, figure.name), exist_ok=True)
            path = os.path.join(Paths.IMGS_EXAMPLE_DIR, figure.name, img_name)
            cv2.imwrite(path, img)
