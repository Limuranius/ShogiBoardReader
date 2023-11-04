import ShogiNeuralNetwork.create_data as create_data
import ShogiNeuralNetwork.train_model as train_model
import ShogiNeuralNetwork.test_model as test_model
from extra.image_modes import ImageMode
from config import Paths

dataset = create_data.create_dataset(
    img_mode=ImageMode.GRAYSCALE_BLACK_THRESHOLD,
    cell_img_size=80
)

model_figure = train_model.train_figure_type_model(
    dataset=dataset,
    epochs=80,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    verbose=1,
)

model_direction = train_model.train_direction_model(
    dataset=dataset,
    epochs=80,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    verbose=1,
)

print(test_model.test_figure_type_model(model_figure, dataset))
print(test_model.test_direction_model(model_direction, dataset))

model_figure.save(Paths.MODEL_FIGURE_PATH)
model_direction.save(Paths.MODEL_DIRECTION_PATH)
