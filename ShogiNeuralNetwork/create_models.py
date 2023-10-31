import ShogiNeuralNetwork.create_data as create_data
import ShogiNeuralNetwork.train_model as train_model
import ShogiNeuralNetwork.test_model as test_model
from extra.image_modes import ImageMode
from config import Paths

data = create_data.create_dataset(
    random_translate_repeat=2,
    random_translate_max_margin=0.1,
    random_rotate_repeat=2,
    random_rotate_max_angle=5,
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=80
)

model_figure = train_model.train_figure_type_model(
    dataset=data,
    cell_img_size=80,
    epochs=5,
    verbose=1,
)

model_direction = train_model.train_direction_model(
    dataset=data,
    cell_img_size=80,
    epochs=5,
    verbose=1,
)

print(test_model.test_figure_type_model(model_figure, data))
print(test_model.test_direction_model(model_direction, data))

model_figure.save(Paths.MODEL_FIGURE_PATH)
model_direction.save(Paths.MODEL_DIRECTION_PATH)
