from .data_info import *
from .true_boards import TrueFigureTypes, TrueDirections
from extra import utils, figures
from extra.image_modes import ImageMode
from Elements import CornerGetters, ImageGetters, BoardSplitter
from sklearn.utils import shuffle
import pandas as pd
from tqdm import tqdm
from .Dataset import Dataset


def __create_training_data(
        random_translate_repeat: int,
        random_translate_max_margin: float,
        random_rotate_repeat: int,
        random_rotate_max_angle: int,
        img_mode: ImageMode,
        cell_img_size: int
) -> pd.DataFrame:
    """
    Разбивает тренировочные фотографии досок на клетки
    и возвращает данные в виде таблицы с полями:
        image:              Изображение фигуры (нормализованное)
        figure_type:        Индекс типа фигуры
        direction:          Индекс направления фигуры
    """

    total_data_count = (len(IMGS)
                        * 81
                        * (random_translate_repeat + 1)
                        * (random_rotate_repeat + 1)
                        )
    training_data = pd.DataFrame(columns=["image", "figure_type", "direction"],
                                 index=range(total_data_count))

    image_getter = ImageGetters.Photo()
    corner_getter = CornerGetters.HardcodedCornerDetector()
    board_splitter = BoardSplitter.BoardSplitter(
        image_getter,
        corner_getter,
        board_img_size=cell_img_size * 9,
        cell_img_size=cell_img_size
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
                    direction = CATEGORIES_DIRECTION.index(true_direction)
                    for img in cell_variations:
                        normalized_img = img.astype("float32") / 255
                        training_data.loc[training_data_i] = [
                            normalized_img,
                            figure_label,
                            direction
                        ]
                        training_data_i += 1
                        pbar.update(1)
    return training_data


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
        random_translate_repeat: int,
        random_translate_max_margin: float,
        random_rotate_repeat: int,
        random_rotate_max_angle: int,
        img_mode: ImageMode,
        test_fraction: float,
        cell_img_size: int) -> Dataset:
    data = __create_training_data(random_translate_repeat, random_translate_max_margin,
                                  random_rotate_repeat, random_rotate_max_angle, img_mode, cell_img_size)
    data = equalize_classes(data)

    dataset = Dataset(data)

    print("Train size:", len(dataset.y_figure_train))
    print("Test size:", len(dataset.y_figure_test))

    return dataset
