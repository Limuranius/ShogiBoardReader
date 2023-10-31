import functions
from extra.image_modes import ImageMode

cases = functions.create_cases(
    random_translate_repeat=list(range(0, 7)),
    random_translate_max_margin=0.2,
    random_rotate_repeat=2,
    random_rotate_max_angle=10,
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=100,
    epochs=4,
)
functions.draw_relation(cases=cases, field="random_translate_repeat", redo_data=True)
