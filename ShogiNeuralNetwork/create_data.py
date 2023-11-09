from extra import figures
from extra.image_modes import ImageMode
from Elements import *
from sklearn.utils import shuffle
import pandas as pd
from tqdm import tqdm
from ShogiNeuralNetwork.data_info import *
from ShogiNeuralNetwork.Dataset import Dataset
from ShogiNeuralNetwork import true_boards
import os
from config import Paths


def load_boards(
        cell_img_size: int,
        img_mode: ImageMode) -> pd.DataFrame:
    total_data_count = len(IMGS) * 81
    data = pd.DataFrame(columns=["image", "figure_type", "direction"],
                        index=range(total_data_count))

    image_getter = ImageGetters.Photo()
    corner_getter = CornerDetectors.HardcodedCornerDetector()
    board_splitter = BoardSplitter(
        image_getter,
        corner_getter,
        cell_img_size=cell_img_size
    )

    data_i = 0
    with tqdm(total=total_data_count, desc="Loading data") as pbar:
        for img_name in IMGS:
            img_path = os.path.join(Paths.TRAIN_BOARDS_DIR, img_name)
            corners = true_boards.get_corners(img_name)
            image_getter.set_image(img_path)
            corner_getter.set_corners(corners)

            true_figure_types = true_boards.get_true_figures(img_name)
            true_directions = true_boards.get_true_directions(img_name)

            cells = board_splitter.get_board_cells(img_mode)
            for i in range(9):
                for j in range(9):
                    true_figure = Figure(true_figure_types[i][j])
                    true_direction = figures.Direction(true_directions[i][j])
                    cell_img = cells[i][j]
                    figure_label = CATEGORIES_FIGURE_TYPE.index(true_figure)
                    direction = CATEGORIES_DIRECTION.index(true_direction)
                    normalized_img = cell_img.astype("float32") / 255
                    data.loc[data_i] = [
                        normalized_img,
                        figure_label,
                        direction
                    ]
                    data_i += 1
                    pbar.update(1)
    return data


def equalize_classes(data: pd.DataFrame) -> pd.DataFrame:
    shuffled_data = shuffle(data)
    classes_counts = shuffled_data["figure_type"].value_counts()
    min_count = classes_counts.min()
    del_indices = []
    for i, row in shuffled_data.iterrows():
        if classes_counts[row["figure_type"]] > min_count:
            del_indices.append(i)
            classes_counts[row["figure_type"]] -= 1
    new_data = data.drop(index=del_indices)
    return new_data


def create_dataset(
        img_mode: ImageMode,
        cell_img_size: int
) -> Dataset:
    data = load_boards(cell_img_size, img_mode)
    data = equalize_classes(data)

    dataset = Dataset(data, img_mode)

    print("Train size:", len(dataset.y_figure_train))
    print("Test size:", len(dataset.y_figure_test))

    return dataset
