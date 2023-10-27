from config.Paths import TRAIN_BOARDS_DIR
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
        "board1.jpg": START_BOARD,
        "board2.jpg": START_BOARD,
        "board3.jpg": START_BOARD,
        "board4.jpg": START_BOARD,
        "board5.jpg": START_BOARD,
        "board6.jpg": """
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
        "board7.jpg": """
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
        "board8.jpg": """
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
        "board9.jpg": """
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
        "board10.jpg": """
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
        "board11.jpg": """
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
        "board12.jpg": """
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
        "board13.jpg": """
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

        "board14.jpg": """
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

        "board15.jpg": START_BOARD,
        "board16.jpg": START_BOARD,
        "board17.jpg": """
            LN.....NL
            ..G.KSG..
            P.PPS..PP
            ....PPB..
            .P....P..
            ..P..P.P.
            PPSP..P.P
            ...GRKS..
            LN...G.NL
        """,
        "board18.jpg": """
            .....RNNL
            ....BSG..
            ......K.P
            ..PPRPBP.
            .P....P..
            ..PS.P.P.
            .P.P..P.P
            ...G.KS..
            .L...G.NL
        """,
        "board19.jpg": """
            .....RNNL
            ....BSG..
            ......K.P
            ..PPRPBP.
            .P....P..
            ..PS.P.P.
            .P.P..P.P
            ...G.KS..
            .L...G.NL
        """,
        "board20.jpg": """
            ......KNL
            L.G.RSG..
            N.PP..SPP
            P.P.BPP..
            .........
            ...B.....
            P.NPPPPPP
            ..G...S..
            L.S..GKNL
        """,
        "board21.jpg": """
            ........L
            .....S...
            .......RP
            ..PP.P...
            .P....P.K
            ..PS.P.PP
            .P.P..P..
            ...G.KS..
            .L...G.NL
        """,
        "board22.jpg": """
            LN..K..NL
            ...S.SG..
            P.PBPPPP.
            ..R.....P
            .P.......
            ..PR.....
            PPB.PPPP.
            ....GKS..
            ..S..G.NL
        """,
        "board23.jpg": """
            LN..K....
            ..GS.SG..
            P.P.PPNPB
            ...P..P..
            .R.L.....
            ..P......
            PPSPPPPPP
            ..G.RG...
            LB..K.SNL
        """,
        "board24.jpg": """
            LN..K..NL
            .....SG..
            P.PRPPPP.
            ..R.....P
            .P.......
            ..P......
            PPB.PPPP.
            ....GKS..
            ..S..G.NL
        """,
        "board25.jpg": """
            LN..K..NL
            .....SG..
            P.PRPPPP.
            ..R.....P
            .P.......
            ..P......
            PPB.PPPP.
            ....BKS..
            ..S..G.NL
        """,
        "board26.jpg": """
            LN.......
            ..GSKSG..
            P.PNPPNPB
            ...P..P..
            .B.......
            ..P.P....
            PP.L.PPPP
            .R...G...
            LB..K.SKL
        """,
        "board27.jpg": """
            LNG......
            ....KSG..
            P...PP.P.
            ..PP..P..
            .....N...
            ..PNP....
            PRG.KPPPP
            ..SB.....
            L....GSNL
        """
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
        "board1.jpg": START_BOARD,
        "board2.jpg": START_BOARD,
        "board3.jpg": START_BOARD,
        "board4.jpg": START_BOARD,
        "board5.jpg": START_BOARD,
        "board6.jpg": """
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
        "board7.jpg": """
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
        "board8.jpg": """
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
        "board9.jpg": """
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
        "board10.jpg": """
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
        "board11.jpg": """
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
        "board12.jpg": """
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
        "board13.jpg": """
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

        "board14.jpg": """
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

        "board15.jpg": START_BOARD,
        "board16.jpg": START_BOARD,
        "board17.jpg": """
            DD.....DD
            ..D.DDD..
            D.DDD..DD
            ....DDD..
            .D....D..
            ..U..U.U.
            UUUU..U.U
            ...UUUU..
            UU...U.UU
        """,
        "board18.jpg": """
            .....UDDD
            ....UDD..
            ......D.D
            ..DDUDDD.
            .D....D..
            ..UU.U.U.
            .U.U..U.U
            ...U.UU..
            .D...U.UU
        """,
        "board19.jpg": """
            .....UDDD
            ....UDD..
            ......D.D
            ..DDUDDD.
            .D....D..
            ..UU.U.U.
            .U.U..U.U
            ...U.UU..
            .D...U.UU
        """,
        "board20.jpg": """
            ......DDD
            D.D.UDD..
            D.DD..DDD
            D.U.UDD..
            .........
            ...U.....
            U.UUUUUUU
            ..U...U..
            U.U..UUUU
        """,
        "board21.jpg": """
            ........D
            .....U...
            .......UD
            ..DD.D...
            .D....D.D
            ..UU.U.UU
            .U.U..U..
            ...U.UU..
            .D...U.UU
        """,
        "board22.jpg": """
            DD..D..DD
            ...D.DD..
            D.DUDDDD.
            ..D.....U
            .D.......
            ..UU.....
            UUD.UUUU.
            ....UUU..
            ..U..U.UU
        """,
        "board23.jpg": """
            DD..D....
            ..DD.DD..
            D.D.DDDDU
            ...U..D..
            .D.D.....
            ..U......
            UUUDUUUUU
            ..U.UU...
            UD..U.UUU
        """,
        "board24.jpg": """
            DD..D..DD
            .....DD..
            D.DUDDDD.
            ..D.....U
            .D.......
            ..U......
            UUD.UUUU.
            ....UUU..
            ..U..U.UU
        """,
        "board25.jpg": """
            DD..D..DD
            .....DD..
            D.DUDDDD.
            ..D.....U
            .D.......
            ..U......
            UUD.UUUU.
            ....UUU..
            ..U..U.UU
        """,
        "board26.jpg": """
            DD.......
            ..DDDDD..
            D.DUDDDDU
            ...U..D..
            .D.......
            ..U.U....
            UU.D.UUUU
            .U...U...
            UD..U.UUU
        """,
        "board27.jpg": """
            DDD......
            ....DDD..
            D...DD.D.
            ..DU..D..
            .....D...
            ..UDU....
            UDU.UUUUU
            ..DU.....
            U....DUUU
        """
    }


for path in list(TrueFigureTypes.TRUE_BOARDS.keys()):
    board = TrueFigureTypes.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")
    TrueFigureTypes.TRUE_BOARDS[path] = board
    abs_path = os.path.join(TRAIN_BOARDS_DIR, path)
    TrueFigureTypes.TRUE_BOARDS[abs_path] = board
for path in list(TrueDirections.TRUE_BOARDS.keys()):
    board = TrueDirections.TRUE_BOARDS[path].strip().replace(" ", "").split("\n")
    TrueDirections.TRUE_BOARDS[path] = board
    abs_path = os.path.join(TRAIN_BOARDS_DIR, path)
    TrueDirections.TRUE_BOARDS[abs_path] = board
