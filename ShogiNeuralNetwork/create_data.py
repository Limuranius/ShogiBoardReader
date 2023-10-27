from data_info import *
from true_boards import TrueFigureTypes, TrueDirections
from extra import utils, figures
from extra.image_modes import ImageMode
from Elements import CornerGetters, ImageGetters, BoardSplitter
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm
from .Dataset import Dataset
from config.config import Config


def _create_training_data(
        random_translate_repeat: int,
        random_translate_max_margin: int,
        random_rotate_repeat: int,
        random_rotate_max_angle: int,
        img_mode: ImageMode
) -> pd.DataFrame:
    """
    Разбивает тренировочные фотографии досок на клетки
    и возвращает данные в виде таблицы с полями:
        image:              Изображение фигуры
        fig_type_label:     Индекс типа фигуры
        direction_label:    Индекс направления фигуры
    """

    total_data_count = (len(IMGS)
                        * 81
                        * (random_translate_repeat + 1)
                        * (random_rotate_repeat + 1)
                        )
    training_data = pd.DataFrame(columns=["image", "fig_type_label", "direction_label"],
                                 index=range(total_data_count))

    image_getter = ImageGetters.Photo()
    corner_getter = CornerGetters.HardcodedCornerDetector()
    board_splitter = BoardSplitter.BoardSplitter(
        image_getter,
        corner_getter
    )

    training_data_i = 0
    with tqdm(total=total_data_count, desc="creating data") as pbar:
        for img_path in IMGS:
            corners = IMGS_CORNERS[img_path]
            image_getter.set_image(img_path)
            corner_getter.set_corners(corners)

            true_figure_types = TrueFigureTypes.TRUE_BOARDS[img_path]
            true_directions = TrueDirections.TRUE_BOARDS[img_path]

            # Итерируемся по всем клеткам доски
            cells = board_splitter.get_board_cells(img_mode)
            for i in range(9):
                for j in range(9):
                    true_figure = Figure(true_figure_types[i][j])
                    true_direction = figures.Direction(true_directions[i][j])

                    cell_img = cells[i][j]
                    cell_variations = [cell_img]

                    # random translate
                    for _ in range(random_translate_repeat):
                        max_margin = random_translate_max_margin
                        trans_img = utils.random_translate_img(cell_img, max_margin, max_margin, fill=0)
                        cell_variations.append(trans_img)

                    # random rotate
                    for _ in range(random_rotate_repeat):
                        for img in cell_variations[: random_translate_repeat + 1]:
                            max_angle = random_rotate_max_angle
                            rot_img = utils.random_rotate_img(img, max_angle, fill=0)
                            cell_variations.append(rot_img)

                    figure_label = CATEGORIES_FIGURE_TYPE.index(true_figure)
                    direction_label = CATEGORIES_DIRECTION.index(true_direction)
                    for img in cell_variations:
                        training_data.loc[training_data_i] = [img, figure_label, direction_label]
                        training_data_i += 1
                        pbar.update(1)
    return training_data


def create_dataset(
        random_translate_repeat: int,
        random_translate_max_margin: int,
        random_rotate_repeat: int,
        random_rotate_max_angle: int,
        img_mode: ImageMode,
        test_fraction: float) -> Dataset:
    data = _create_training_data(random_translate_repeat, random_translate_max_margin,
                                 random_rotate_repeat, random_rotate_max_angle, img_mode)

    train, test = train_test_split(data, test_size=test_fraction)

    print("Train size:", len(train))
    print("Test size:", len(test))

    return Dataset(
        X_train=train["image"].to_numpy(),
        X_test=test["image"].to_numpy(),
        y_figure_train=train["fig_type_label"].to_numpy(),
        y_figure_test=test["fig_type_label"].to_numpy(),
        y_direction_train=train["direction_label"].to_numpy(),
        y_direction_test=test["direction_label"].to_numpy(),
    )
