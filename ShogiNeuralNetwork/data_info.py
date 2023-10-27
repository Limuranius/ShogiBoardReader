from extra.figures import Figure, Direction
from config import Paths
import os

IMGS_CORNERS = {
    "board1.jpg": ((425, 759), (2871, 725), (2981, 3508), (381, 3522)),
    "board2.jpg": ((570, 1036), (2759, 992), (2962, 3526), (442, 3561)),
    "board3.jpg": ((809, 793), (2829, 1214), (2700, 3340), (821, 3859)),
    "board4.jpg": ((826, 499), (2602, 1104), (2590, 3132), (755, 3366)),
    "board5.jpg": ((920, 2002), (2620, 1930), (3289, 3676), (319, 3733)),
    "board6.jpg": ((49, 109), (491, 105), (510, 593), (52, 603)),
    "board7.jpg": ((68, 53), (547, 55), (558, 592), (52, 589)),
    "board8.jpg": ((61, 61), (475, 50), (504, 508), (66, 517)),
    "board9.jpg": ((51, 48), (499, 43), (520, 534), (61, 551)),
    "board10.jpg": ((68, 69), (456, 65), (494, 484), (79, 506)),
    "board11.jpg": ((50, 48), (491, 45), (507, 531), (52, 540)),
    "board12.jpg": ((35, 47), (493, 44), (512, 544), (45, 558)),
    "board13.jpg": ((1583, 980), (3421, 956), (3462, 2806), (1608, 2827)),
    "board14.jpg": ((1594, 976), (3429, 967), (3454, 2814), (1602, 2822)),
    "board15.jpg": ((510, 1031), (2723, 981), (2824, 3759), (445, 3756)),
    "board16.jpg": ((633, 1282), (2585, 1218), (2684, 3598), (676, 3653)),
    "board17.jpg": ((463, 1370), (2610, 1341), (2668, 3966), (461, 3988)),
    "board18.jpg": ((642, 1128), (2692, 1086), (2761, 3624), (620, 3620)),
    "board19.jpg": ((647, 1491), (2571, 1499), (2629, 3863), (602, 3888)),
    "board20.jpg": ((670, 1295), (2553, 1383), (2467, 3659), (558, 3581)),
    "board21.jpg": ((431, 1281), (2606, 1232), (2653, 3880), (463, 3881)),
    "board22.jpg": ((412, 872), (2825, 884), (2841, 3814), (370, 3810)),
    "board23.jpg": ((602, 1087), (2906, 1064), (2932, 4017), (458, 3901)),
    "board24.jpg": ((372, 842), (2847, 783), (2934, 3863), (331, 3856)),
    "board25.jpg": ((574, 1166), (2858, 1155), (2932, 3999), (503, 3987)),
    "board26.jpg": ((721, 1182), (2680, 1219), (2675, 3674), (572, 3588)),
    "board27.jpg": ((635, 1438), (2631, 1526), (2605, 4029), (449, 3948)),
}

IMGS = [
    "board1.jpg",
    "board2.jpg",
    "board3.jpg",
    "board4.jpg",
    "board5.jpg",
    # "board6.jpg",
    # "board7.jpg",
    # "board8.jpg",
    # "board9.jpg",
    # "board10.jpg",
    # "board11.jpg",
    # "board12.jpg",
    "board13.jpg",
    "board14.jpg",
    "board15.jpg",
    "board16.jpg",
    "board17.jpg",
    "board18.jpg",
    "board19.jpg",
    "board20.jpg",
    "board21.jpg",
    "board22.jpg",
    "board23.jpg",
    "board24.jpg",
    "board25.jpg",
    "board26.jpg",
    "board27.jpg",
]

for path in list(IMGS_CORNERS.keys()):
    abs_path = os.path.join(Paths.TRAIN_BOARDS_DIR, path)
    IMGS_CORNERS[abs_path] = IMGS_CORNERS[path]
for i, path in enumerate(IMGS):
    IMGS[i] = os.path.join(Paths.TRAIN_BOARDS_DIR, path)

CATEGORIES_FIGURE_TYPE = [Figure.PAWN, Figure.BISHOP, Figure.ROOK, Figure.LANCE,
                          Figure.KNIGHT, Figure.SILVER, Figure.GOLD, Figure.KING, Figure.EMPTY]

CATEGORIES_DIRECTION = [Direction.UP, Direction.DOWN, Direction.NONE]
