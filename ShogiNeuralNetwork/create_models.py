import ShogiNeuralNetwork.create_data as create_data
import ShogiNeuralNetwork.train_model as train_model
import ShogiNeuralNetwork.test_model as test_model
from extra.image_modes import ImageMode
from config import Paths, GLOBAL_CONFIG

dataset = create_data.create_dataset(
    img_mode=ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode),
    cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
)

model_figure = train_model.train_figure_type_model(
    dataset=dataset,
    epochs=GLOBAL_CONFIG.NeuralNetwork.figure_epochs,
    rotation_range=GLOBAL_CONFIG.NeuralNetwork.rotation_range,
    width_shift_range=GLOBAL_CONFIG.NeuralNetwork.width_shift_range,
    height_shift_range=GLOBAL_CONFIG.NeuralNetwork.height_shift_range,
    verbose=1,
)

model_direction = train_model.train_direction_model(
    dataset=dataset,
    epochs=GLOBAL_CONFIG.NeuralNetwork.direction_epochs,
    rotation_range=GLOBAL_CONFIG.NeuralNetwork.rotation_range,
    width_shift_range=GLOBAL_CONFIG.NeuralNetwork.width_shift_range,
    height_shift_range=GLOBAL_CONFIG.NeuralNetwork.height_shift_range,
    verbose=1,
)

print(test_model.test_figure_type_model(model_figure, dataset))
print(test_model.test_direction_model(model_direction, dataset))

model_figure.save(Paths.MODEL_FIGURE_PATH)
model_direction.save(Paths.MODEL_DIRECTION_PATH)
