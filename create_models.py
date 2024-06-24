import json
import os

import keras
import onnx
import tensorflow as tf

from ShogiNeuralNetwork.CellsDataset import CellsDataset
from ShogiNeuralNetwork.create_model import create_model
from ShogiNeuralNetwork.train_model import train_model
from config import Paths, GLOBAL_CONFIG
from extra.image_modes import ImageMode


def train_and_save_model():
    dataset = CellsDataset()
    dataset.load(Paths.DATASET_PATH)

    dataset = dataset.resize(
        (GLOBAL_CONFIG.NeuralNetworkTraining.cell_img_size, GLOBAL_CONFIG.NeuralNetworkTraining.cell_img_size))
    dataset = dataset.convert(ImageMode(GLOBAL_CONFIG.NeuralNetworkTraining.image_mode))
    train, test = dataset.get_tf_dataset()

    model = create_model(GLOBAL_CONFIG.NeuralNetworkTraining.cell_img_size)
    model = train_model(model, train, GLOBAL_CONFIG.NeuralNetworkTraining.epochs, 1)

    print(model.evaluate(test, return_dict=True, verbose=1))

    model.save(Paths.MODEL_TF_PATH)


def save_onnx_model():
    os.system("python -m tf2onnx.convert --saved-model {tf_model_path} --output {onnx_model_path}".format(
        tf_model_path=Paths.MODEL_TF_PATH,
        onnx_model_path=Paths.MODEL_ONNX_PATH,
    ))

    # Adding metadata to model
    model = onnx.load_model(Paths.MODEL_ONNX_PATH)

    def add_meta(key, value):
        m = model.metadata_props.add()
        m.key = key
        m.value = json.dumps(value)

    add_meta("cell_img_size", GLOBAL_CONFIG.NeuralNetworkTraining.cell_img_size)
    add_meta("image_mode", GLOBAL_CONFIG.NeuralNetworkTraining.image_mode)
    onnx.save(model, Paths.MODEL_ONNX_PATH)


def save_tflite_model():
    model = keras.models.load_model(Paths.MODEL_TF_PATH)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open(Paths.MODEL_TFLITE_PATH, 'wb') as f:
        f.write(tflite_model)


def main():
    train_and_save_model()
    save_onnx_model()
    save_tflite_model()


if __name__ == '__main__':
    main()
