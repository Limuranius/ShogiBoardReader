import ShogiNeuralNetwork.train_model as train_model
from ShogiNeuralNetwork.CellsDataset import CellsDataset
from extra.image_modes import ImageMode
from config import Paths, GLOBAL_CONFIG

dataset = CellsDataset()
dataset.load_pickle(Paths.ORIGINAL_CELLS_DATASET_PATH)
dataset.save_images()
dataset = dataset.convert(ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode))

figure_train, figure_test = dataset.get_figure_tf_dataset()
direction_train, direction_test = dataset.get_direction_tf_dataset()

model_figure = train_model.train_figure_type_model(
    train_ds=figure_train,
    epochs=GLOBAL_CONFIG.NeuralNetwork.figure_epochs,
    verbose=1,
)

model_direction = train_model.train_direction_model(
    train_ds=direction_train,
    epochs=GLOBAL_CONFIG.NeuralNetwork.figure_epochs,
    verbose=1,
)

model_figure.save(Paths.MODEL_FIGURE_PATH)
model_direction.save(Paths.MODEL_DIRECTION_PATH)
