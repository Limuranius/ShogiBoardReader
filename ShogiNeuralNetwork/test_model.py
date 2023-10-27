from tensorflow import keras
from .Dataset import Dataset
from dataclasses import dataclass
from extra.figures import Figure, Direction


@dataclass
class FigureTypeTestResult:
    total_accuracy: float
    each_figure_acc: dict[Figure, float]


@dataclass
class DirectionTestResult:
    total_accuracy: float
    each_figure_acc: dict[Direction, float]


def test_figure_type_model(
        model: keras.Model,
        dataset: Dataset
) -> FigureTypeTestResult:
    X_test = dataset.X_test
    y_test = dataset.y_figure_test
    model.evaluate(X_test, y_test, batch_size=32)


def test_direction_model(
        model: keras.Model,
        dataset: Dataset
) -> DirectionTestResult:
    X_test = dataset.X_test
    y_test = dataset.y_figure_test
    model.evaluate(X_test, y_test, batch_size=32)
