import functions
from extra.image_modes import ImageMode

cases = functions.create_cases(
    random_translate_repeat=4,
    random_translate_max_margin=functions.float_range(0, 0.5, 0.1),
    random_rotate_repeat=0,
    random_rotate_max_angle=10,
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=100,
    epochs=4,
)
functions.draw_relation(cases=cases, field="random_translate_max_margin", redo_data=True)
