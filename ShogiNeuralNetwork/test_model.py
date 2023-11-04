from tensorflow import keras
from .Dataset import Dataset
from dataclasses import dataclass, field
from extra.figures import Figure, Direction
from .data_info import CATEGORIES_DIRECTION, CATEGORIES_FIGURE_TYPE


@dataclass
class FigureTypeTestResult:
    test_total_accuracy: float = None
    test_each_figure_acc: dict[Figure, float] = field(default_factory=dict)
    train_total_accuracy: float = None
    train_each_figure_acc: dict[Figure, float] = field(default_factory=dict)

    def __str__(self):
        s = f"TEST:\nTotal accuracy: {self.test_total_accuracy}"
        for fig_type in Figure:
            s += f"\n{fig_type.name}: {self.test_each_figure_acc[fig_type]}"
        s += f"\n\nTRAIN:\nTotal accuracy: {self.train_total_accuracy}"
        for fig_type in Figure:
            s += f"\n{fig_type.name}: {self.train_each_figure_acc[fig_type]}"
        s += "\n\n"
        return s


@dataclass
class DirectionTestResult:
    test_total_accuracy: float = None
    test_each_direction_acc: dict[Direction, float] = field(default_factory=dict)
    train_total_accuracy: float = None
    train_each_direction_acc: dict[Direction, float] = field(default_factory=dict)

    def __str__(self):
        s = f"TEST:\nTotal accuracy: {self.test_total_accuracy}"
        for direction in Direction:
            s += f"\n{direction.name}: {self.test_each_direction_acc[direction]}"
        s += f"\n\nTRAIN:\nTotal accuracy: {self.train_total_accuracy}"
        for direction in Direction:
            s += f"\n{direction.name}: {self.train_each_direction_acc[direction]}"
        s += "\n\n"
        return s


def test_figure_type_model(
        model: keras.Model,
        dataset: Dataset
) -> FigureTypeTestResult:
    result = FigureTypeTestResult()

    # Test data
    X_test = dataset.x_test
    y_test = dataset.y_figure_test
    result.test_total_accuracy = model.evaluate(X_test, y_test, batch_size=32, return_dict=True,
                                                verbose=0)["accuracy"]
    for i in range(len(CATEGORIES_FIGURE_TYPE)):
        fig_X_test = X_test[y_test == i]
        fig_y_test = y_test[y_test == i]
        fig_type = CATEGORIES_FIGURE_TYPE[i]
        fig_res = model.evaluate(fig_X_test, fig_y_test, batch_size=32, return_dict=True, verbose=0)
        result.test_each_figure_acc[fig_type] = fig_res["accuracy"]

    # Train data
    X_train = dataset.x_train
    y_train = dataset.y_figure_train
    result.train_total_accuracy = model.evaluate(X_train, y_train, batch_size=32, return_dict=True,
                                                 verbose=0)["accuracy"]
    for i in range(len(CATEGORIES_FIGURE_TYPE)):
        fig_X_train = X_train[y_train == i]
        fig_y_train = y_train[y_train == i]
        fig_type = CATEGORIES_FIGURE_TYPE[i]
        fig_res = model.evaluate(fig_X_train, fig_y_train, batch_size=32, return_dict=True, verbose=0)
        result.train_each_figure_acc[fig_type] = fig_res["accuracy"]

    return result


def test_direction_model(
        model: keras.Model,
        dataset: Dataset
) -> DirectionTestResult:
    result = DirectionTestResult()

    # Test data
    X_test = dataset.x_test
    y_test = dataset.y_direction_test
    result.test_total_accuracy = model.evaluate(X_test, y_test, batch_size=32, return_dict=True,
                                                verbose=0)["accuracy"]
    for i in range(len(CATEGORIES_DIRECTION)):
        direction_X_test = X_test[y_test == i]
        direction_y_test = y_test[y_test == i]
        direction_type = CATEGORIES_DIRECTION[i]
        direction_res = model.evaluate(direction_X_test, direction_y_test, batch_size=32, return_dict=True, verbose=0)
        result.test_each_direction_acc[direction_type] = direction_res["accuracy"]

    # Train data
    X_train = dataset.x_train
    y_train = dataset.y_direction_train
    result.train_total_accuracy = model.evaluate(X_train, y_train, batch_size=32, return_dict=True,
                                                 verbose=0)["accuracy"]
    for i in range(len(CATEGORIES_DIRECTION)):
        direction_X_test = X_test[y_test == i]
        direction_y_test = y_test[y_test == i]
        direction_type = CATEGORIES_DIRECTION[i]
        direction_res = model.evaluate(direction_X_test, direction_y_test, batch_size=32, return_dict=True, verbose=0)
        result.train_each_direction_acc[direction_type] = direction_res["accuracy"]

    return result
