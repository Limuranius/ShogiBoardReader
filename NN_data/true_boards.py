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
        "imgs/board.jpg": START_BOARD,
        "imgs/board2.jpg": START_BOARD,
        "imgs/board3.jpg": START_BOARD,
        "imgs/board4.jpg": START_BOARD,
        "imgs/board5.jpg": START_BOARD,
        "imgs/board6.png": """
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
        "imgs/board7.png": """
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
        "imgs/board8.png": """
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
        "imgs/board9.png": """
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
        "imgs/board10.png": """
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
        "imgs/board11.png": """
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
        "imgs/board12.png": """
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
        "imgs/board13.jpg": """
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

        "imgs/board14.jpg": """
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
        "imgs/board.jpg": START_BOARD,
        "imgs/board2.jpg": START_BOARD,
        "imgs/board3.jpg": START_BOARD,
        "imgs/board4.jpg": START_BOARD,
        "imgs/board5.jpg": START_BOARD,
        "imgs/board6.png": """
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
        "imgs/board7.png": """
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
        "imgs/board8.png": """
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
        "imgs/board9.png": """
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
        "imgs/board10.png": """
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
        "imgs/board11.png": """
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
        "imgs/board12.png": """
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
        "imgs/board13.jpg": """
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

        "imgs/board14.jpg": """
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
    }


for path in TrueFigureTypes.TRUE_BOARDS:
    TrueFigureTypes.TRUE_BOARDS[path] = TrueFigureTypes.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")
for path in TrueDirections.TRUE_BOARDS:
    TrueDirections.TRUE_BOARDS[path] = TrueDirections.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")