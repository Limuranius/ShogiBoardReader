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
from . import augmentation


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

    def __init__(self, data: pd.DataFrame = None, visited_hashes=None):
        self.__data = data
        self.__visited_images_hashes = visited_hashes

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

    def save(self, path: str):
        count = defaultdict(int)
        for _, row in tqdm.tqdm(self.__data.iterrows()):
            img = row["image"]
            figure = row["figure_type"]
            direction = row["direction"]
            count[(figure, direction)] += 1
            img_name = f"{count[(figure, direction)]}.jpg"
            dir_path = os.path.join(path, figure.name, direction.name)
            img_path = os.path.join(dir_path, img_name)
            os.makedirs(dir_path, exist_ok=True)
            cv2.imwrite(img_path, img)
        img_hash_path = os.path.join(path, "images_hash.pickle")
        with open(img_hash_path, "wb") as f:
            pickle.dump(self.__visited_images_hashes, f)

    def load(self, path: str):
        data = []
        for figure in Figure:
            for direction in Direction:
                folder_path = os.path.join(path, figure.name, direction.name)
                if os.path.exists(folder_path):
                    for img_name in os.listdir(folder_path):
                        img_path = os.path.join(folder_path, img_name)
                        img = cv2.imread(img_path)
                        data.append((img, figure, direction))
        self.__data = pd.DataFrame(data, columns=["image", "figure_type", "direction"])
        img_hash_path = os.path.join(path, "images_hash.pickle")
        with open(img_hash_path, "rb") as f:
            self.__visited_images_hashes = pickle.load(f)

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
        return CellsDataset(new_data, self.__visited_images_hashes)

    def resize(self, size: tuple[int, int]) -> CellsDataset:
        def func(img):
            return cv2.resize(img, size)

        new_data = self.__data.copy()
        new_data["image"] = new_data["image"].apply(func)
        return CellsDataset(new_data, self.__visited_images_hashes)

    def __prepare_1(self) -> pd.DataFrame:
        new_data = self.__data
        # new_data = equalize_classes(new_data)
        new_data = enums_to_labels(new_data)
        new_data = reshape_imgs(new_data)
        return new_data

    def __to_tf_dataset(self) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        data = self.__prepare_1()
        train, test = train_test_split(data, test_size=GLOBAL_CONFIG.NeuralNetworkTraining.test_fraction)

        train_images = np.array(train["image"].tolist())
        train_figure_labels = train["figure_type"].to_numpy()
        train_direction_labels = train["direction"].to_numpy()

        test_images = np.array(test["image"].tolist())
        test_figure_labels = test["figure_type"].to_numpy()
        test_direction_labels = test["direction"].to_numpy()

        train_tf = tf.data.Dataset.from_tensor_slices(
            (
                train_images,
                {"figure": train_figure_labels, "direction": train_direction_labels}
            )
        )

        test_tf = tf.data.Dataset.from_tensor_slices(
            (
                test_images,
                {"figure": test_figure_labels, "direction": test_direction_labels}
            )
        )

        return train_tf, test_tf

    def __prepare_train(self, ds: tf.data.Dataset) -> tf.data.Dataset:
        train_ds = (
            ds
            .shuffle(ds.cardinality())
            .batch(GLOBAL_CONFIG.NeuralNetworkTraining.batch_size)
            .map(lambda img, outputs:
                 (augmentation.resize_and_rescale(img), outputs))
            .map(lambda img, outputs:
                 (augmentation.augment(img), outputs))
        )
        return train_ds

    def __prepare_test(self, ds: tf.data.Dataset) -> tf.data.Dataset:
        test_ds = (
            ds
            .batch(GLOBAL_CONFIG.NeuralNetworkTraining.batch_size)
            .map(lambda img, outputs:
                 (augmentation.resize_and_rescale(img), outputs))
        )
        return test_ds

    def get_tf_dataset(self) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        train, test = self.__to_tf_dataset()
        train = self.__prepare_train(train)
        test = self.__prepare_test(test)
        return train, test
