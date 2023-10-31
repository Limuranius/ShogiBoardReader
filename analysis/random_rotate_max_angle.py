import functions
from extra.image_modes import ImageMode

cases = functions.create_cases(
    random_translate_repeat=2,
    random_translate_max_margin=0.2,
    random_rotate_repeat=2,
    random_rotate_max_angle=list(range(0, 20, 2)),
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=80,
    epochs=4,
)
functions.draw_relation(cases=cases, field="random_rotate_max_angle", redo_data=True)
