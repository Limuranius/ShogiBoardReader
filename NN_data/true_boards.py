from paths import TRAIN_BOARDS_DIR
import os


class TrueFigureTypes:
    START_BOARD = """
    LNSGKGSNL
    .R.....B.
    PPPPPPPPP
    .........
    .........
    .........
    PPPPPPPPP
    .B.....R.
    LNSGKGSNL
    """

    TRUE_BOARDS = {
        os.path.join(TRAIN_BOARDS_DIR, "board.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board2.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board3.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board4.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board5.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board6.jpg"): """
            LNKG.GSNL
            .RS....B.
            PPPPPP.PP
            ......P..
            .......P.
            ..P.P..R.
            PP.P.PP.P
            .B...K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board7.jpg"): """
            LNKG.GSNL
            .RS....B.
            PPPPPP.PP
            ......P..
            .......P.
            ..P....R.
            PP.PPPP.P
            .B...K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board8.jpg"): """
            LNKG.GSNL
            .RS....B.
            .PPPPP.PP
            P.....P..
            ....B..P.
            ..P.P..R.
            PP.P.PP.P
            .....K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board9.jpg"): """
            LNKG.GSNL
            .RS....B.
            .PPPPP.PP
            P.....P..
            ....B..P.
            ..P.P..R.
            PP.P.PP.P
            .....K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board10.jpg"): """
            LNKG.GSNL
            .RS....B.
            PPPPPP.PP
            ......P..
            .......P.
            ..P....R.
            PP.PPPP.P
            .B...K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board11.jpg"): """
            LNKG.GSNL
            .RS....B.
            PPPPPP.PP
            ......P..
            .......P.
            ..P.P..R.
            PP.P.PP.P
            .B...K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board12.jpg"): """
            LNKG.GSNL
            .RS....B.
            PPPPPP.PP
            ......P..
            ....B..P.
            ..P.P..R.
            PP.P.PP.P
            .....K...
            LNSG.GSNL
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board13.jpg"): """
            ....L....
            ..S...R..
            ....N...L
            .P..N..G.
            .........
            ..B.P..S.
            .........
            ..K....G.
            .....P...
        """,

        os.path.join(TRAIN_BOARDS_DIR, "board14.jpg"): """
            ......L..
            .........
            ....NL...
            ...SN.R..
            ...P.....
            .........
            ...PG....
            .B..KSG..
            .....P...
        """,

        os.path.join(TRAIN_BOARDS_DIR, "board15.jpg"): START_BOARD,
    }


class TrueDirections:
    """Направление фигур. U - смотрят вверх, D - смотрят вниз"""

    START_BOARD = """
    DDDDDDDDD
    .D.....D.
    DDDDDDDDD
    .........
    .........
    .........
    UUUUUUUUU
    .U.....U.
    UUUUUUUUU
    """

    TRUE_BOARDS = {
        os.path.join(TRAIN_BOARDS_DIR, "board.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board2.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board3.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board4.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board5.jpg"): START_BOARD,
        os.path.join(TRAIN_BOARDS_DIR, "board6.jpg"): """
            DDDD.DDDD
            .DD....D.
            DDDDDD.DD
            ......D..
            .......U.
            ..U.U..U.
            UU.U.UU.U
            .U...U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board7.jpg"): """
            DDDD.DDDD
            .DD....D.
            DDDDDD.DD
            ......D..
            .......U.
            ..U....U.
            UU.UUUU.U
            .U...U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board8.jpg"): """
            DDDD.DDDD
            .DD....D.
            .DDDDD.DD
            D.....D..
            ....U..U.
            ..U.U..U.
            UU.U.UU.U
            .....U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board9.jpg"): """
            DDDD.DDDD
            .DD....D.
            .DDDDD.DD
            D.....D..
            ....U..U.
            ..U.U..U.
            UU.U.UU.U
            .....U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board10.jpg"): """
            DDDD.DDDD
            .DD....D.
            DDDDDD.DD
            ......D..
            .......U.
            ..U....U.
            UU.UUUU.U
            .U...U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board11.jpg"): """
            DDDD.DDDD
            .DD....D.
            DDDDDD.DD
            ......D..
            .......U.
            ..U.U..U.
            UU.U.UU.U
            .U...U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board12.jpg"): """
            DDDD.DDDD
            .DD....D.
            DDDDDD.DD
            ......D..
            ....U..U.
            ..U.U..U.
            UU.U.UU.U
            .....U...
            UUUU.UUUU
        """,
        os.path.join(TRAIN_BOARDS_DIR, "board13.jpg"): """
            ....D....
            ..U...D..
            ....U...U
            .U..D..U.
            .........
            ..U.U..D.
            .........
            ..U....U.
            .....U...
        """,

        os.path.join(TRAIN_BOARDS_DIR, "board14.jpg"): """
            ......D..
            .........
            ....UD...
            ...UD.D..
            ...U.....
            .........
            ...UU....
            .U..UDU..
            .....U...
        """,

        os.path.join(TRAIN_BOARDS_DIR, "board15.jpg"): START_BOARD,
    }


for path in TrueFigureTypes.TRUE_BOARDS:
    TrueFigureTypes.TRUE_BOARDS[path] = TrueFigureTypes.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")
for path in TrueDirections.TRUE_BOARDS:
    TrueDirections.TRUE_BOARDS[path] = TrueDirections.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")
