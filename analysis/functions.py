import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from ShogiNeuralNetwork import create_data
from ShogiNeuralNetwork import train_model
from ShogiNeuralNetwork import test_model
from extra.image_modes import ImageMode
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import multiprocessing
from tqdm import tqdm

REPEAT_FOR_AVERAGE_COUNT = 5


def create_cases(
        random_translate_repeat: int | list[int],
        random_translate_max_margin: float | list[float],
        random_rotate_repeat: int | list[int],
        random_rotate_max_angle: int | list[int],
        img_mode: ImageMode,
        test_fraction: float | list[float],
        cell_img_size: int | list[int],
        epochs: int | list[int],
) -> pd.DataFrame:
    df = pd.DataFrame(columns=["random_translate_repeat", "random_translate_max_margin", "random_rotate_repeat",
                               "random_rotate_max_angle", "img_mode", "test_fraction", "cell_img_size", "epochs"])
    if not isinstance(random_translate_repeat, list):
        random_translate_repeat = [random_translate_repeat]
    if not isinstance(random_translate_max_margin, list):
        random_translate_max_margin = [random_translate_max_margin]
    if not isinstance(random_rotate_repeat, list):
        random_rotate_repeat = [random_rotate_repeat]
    if not isinstance(random_rotate_max_angle, list):
        random_rotate_max_angle = [random_rotate_max_angle]
    if not isinstance(img_mode, list):
        img_mode = [img_mode]
    if not isinstance(test_fraction, list):
        test_fraction = [test_fraction]
    if not isinstance(cell_img_size, list):
        cell_img_size = [cell_img_size]
    if not isinstance(epochs, list):
        epochs = [epochs]
    combinations = itertools.product(random_translate_repeat, random_translate_max_margin, random_rotate_repeat,
                                     random_rotate_max_angle, img_mode, test_fraction, cell_img_size, epochs)
    for row in combinations:
        df.loc[len(df)] = row
    return df


def draw_relation(cases: pd.DataFrame, field: str, redo_data: bool):
    results = pd.DataFrame(columns=[field, "sample_type", "class", "accuracy"])
    data = None
    pbar = tqdm(total=len(cases) * REPEAT_FOR_AVERAGE_COUNT)
    for _, case in cases.iterrows():
        if redo_data or data is None:
            data = create_data.create_dataset(
                random_translate_repeat=case["random_translate_repeat"],
                random_translate_max_margin=case["random_translate_max_margin"],
                random_rotate_repeat=case["random_rotate_repeat"],
                random_rotate_max_angle=case["random_rotate_max_angle"],
                img_mode=case["img_mode"],
                test_fraction=case["test_fraction"],
                cell_img_size=case["cell_img_size"]
            )

        def gpu_process(accs_train, accs_test):
            model = train_model.train_figure_type_model(
                dataset=data,
                cell_img_size=case["cell_img_size"],
                epochs=case["epochs"]
            )
            test_results = test_model.test_figure_type_model(model, data)
            accs_train.append(test_results.train_total_accuracy)
            accs_test.append(test_results.test_total_accuracy)
            data.reshuffle(0.2)

        train_avg: int
        test_avg: int
        with multiprocessing.Manager() as manager:
            accs_train = manager.list()
            accs_test = manager.list()
            for _ in range(REPEAT_FOR_AVERAGE_COUNT):
                proc = multiprocessing.Process(target=gpu_process, args=(accs_train, accs_test))
                proc.start()
                proc.join()
                proc.close()
                data.reshuffle(0.2)
                pbar.update(1)
            print(accs_train)
            print(accs_test)
            train_avg = sum(accs_train) / len(accs_train)
            test_avg = sum(accs_test) / len(accs_test)

        results.loc[len(results)] = [case[field], "train", "total", train_avg]
        results.loc[len(results)] = [case[field], "test", "total", test_avg]
        # for figure_type in test_results.test_each_figure_acc.keys():
        #     results.loc[len(results)] = [case[field], "test", figure_type.name,
        #                                  test_results.test_each_figure_acc[figure_type]]
        #     results.loc[len(results)] = [case[field], "train", figure_type.name,
        #                                  test_results.train_each_figure_acc[figure_type]]

    total_results = results[results["class"] == "total"]
    sns.relplot(data=total_results, x=field, y="accuracy", hue="sample_type", kind="line")
    plt.grid()
    plt.savefig(field, dpi=300)


def float_range(start: float, end: float, step: float) -> list[float]:
    result = []
    curr = start
    while curr <= end:
        result.append(curr)
        curr += step
    return result
