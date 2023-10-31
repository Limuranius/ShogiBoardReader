import functions
from extra.image_modes import ImageMode



cases = functions.create_cases(
    random_translate_repeat=2,
    random_translate_max_margin=0.2,
    random_rotate_repeat=2,
    random_rotate_max_angle=10,
    img_mode=ImageMode.CANNY,
    test_fraction=0.2,
    cell_img_size=list(range(20, 101, 10)),
    epochs=4,
)
functions.draw_relation(cases=cases, field="cell_img_size", redo_data=True)
