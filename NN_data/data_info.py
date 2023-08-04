from figures import Figure, Direction
import os
import paths

IMGS_CORNERS = {
    os.path.join(paths.TRAIN_BOARDS_DIR, "board.jpg"): ((425, 759), (2871, 725), (2981, 3508), (381, 3522)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board2.jpg"): ((570, 1036), (2759, 992), (2962, 3526), (442, 3561)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board3.jpg"): ((809, 793), (2829, 1214), (2700, 3340), (821, 3859)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board4.jpg"): ((826, 499), (2602, 1104), (2590, 3132), (755, 3366)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board5.jpg"): ((920, 2002), (2620, 1930), (3289, 3676), (319, 3733)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board6.png"): ((49, 109), (491, 105), (510, 593), (52, 603)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board7.png"): ((68, 53), (547, 55), (558, 592), (52, 589)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board8.png"): ((61, 61), (475, 50), (504, 508), (66, 517)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board9.png"): ((51, 48), (499, 43), (520, 534), (61, 551)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board10.png"): ((68, 69), (456, 65), (494, 484), (79, 506)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board11.png"): ((50, 48), (491, 45), (507, 531), (52, 540)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board12.png"): ((35, 47), (493, 44), (512, 544), (45, 558)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board13.jpg"): ((1583, 980), (3421, 956), (3462, 2806), (1608, 2827)),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board14.jpg"): ((1594, 976), (3429, 967), (3454, 2814), (1602, 2822)),
}

IMGS = [
    os.path.join(paths.TRAIN_BOARDS_DIR, "board.jpg"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board2.jpg"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board3.jpg"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board4.jpg"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board5.jpg"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board6.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board7.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board8.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board9.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board10.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board11.png"),
    # os.path.join(paths.TRAIN_BOARDS_DIR, "board12.png"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board13.jpg"),
    os.path.join(paths.TRAIN_BOARDS_DIR, "board14.jpg"),
]

CATEGORIES_FIGURE_TYPE = [Figure.PAWN, Figure.BISHOP, Figure.ROOK, Figure.LANCE,
                          Figure.KNIGHT, Figure.SILVER, Figure.GOLD, Figure.KING, Figure.EMPTY]

CATEGORIES_DIRECTION = [Direction.UP, Direction.DOWN, Direction.NONE]
