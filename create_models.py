import ShogiNeuralNetwork.train_model as train_model
from ShogiNeuralNetwork.CellsDataset import CellsDataset
from extra.image_modes import ImageMode
from config import Paths, GLOBAL_CONFIG
import os

dataset = CellsDataset()
dataset.load_pickle(Paths.ORIGINAL_CELLS_DATASET_PATH)
dataset = dataset.resize((GLOBAL_CONFIG.NeuralNetwork.cell_img_size, GLOBAL_CONFIG.NeuralNetwork.cell_img_size))
dataset.save_images()

dataset = dataset.convert(ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode))

train, test = dataset.get_tf_dataset()

model = train_model.train_model(train, GLOBAL_CONFIG.NeuralNetwork.figure_epochs, 0)

print(model.evaluate(test, return_dict=True, verbose=1))

model.save(Paths.MODEL_TF_PATH)
os.system("python -m tf2onnx.convert --saved-model {tf_model_path} --output {onnx_model_path}".format(
    tf_model_path=Paths.MODEL_TF_PATH,
    onnx_model_path=Paths.MODEL_ONNX_PATH,
))
