import functions
from extra.image_modes import ImageMode

cases = functions.create_cases(
    random_translate_repeat=0,
    random_translate_max_margin=0.2,
    random_rotate_repeat=0,
    random_rotate_max_angle=10,
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=80,
    epochs=list(range(1, 6)),
)
functions.draw_relation(cases=cases, field="epochs", redo_data=False)
