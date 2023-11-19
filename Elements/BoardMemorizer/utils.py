from extra.types import Figure, FigureBoard
from .Move import *
from ..Board import Board


def get_changed_cells(old_board: Board, new_board: Board) -> list[tuple[int, int]]:
    """Returns list of cells that changed from old_board to new_board"""
    changed = []
    for i in range(9):
        for j in range(9):
            figures_match = old_board.figures[i][j] == new_board.figures[i][j]
            directions_match = old_board.directions[i][j] == new_board.directions[i][j]
            cells_empty = old_board.figures[i][j] == new_board.figures[i][j] == Figure.EMPTY
            if cells_empty:
                continue
            elif not figures_match or not directions_match:
                changed.append((i, j))
    return changed


def get_move(old_board: Board, new_board: Board) -> Move | None:
    """
    Returns move taken between old_board and new_board
    or None if change from old_board to new_board is impossible in 1 move
    """
    changed_cells = get_changed_cells(old_board, new_board)
    changed_count = len(changed_cells)

    if changed_count == 1:
        """
        Valid options:
            piece dropped (EMPTY -> PIECE)
        """
        i, j = changed_cells[0]
        if old_board.figures[i][j] == Figure.EMPTY and new_board.figures[i][j] != Figure.EMPTY:
            dropped_fig = new_board.figures[i][j]
            x = j + 1
            y = i + 1
            return Move(
                move_type=MoveType.DROP,
                figure=dropped_fig,
                destination=(x, y)
            )
        else:
            return None
    elif changed_count == 2:
        """
        Valid options: 
            piece moved (PIECE-EMPTY -> EMPTY-PIECE or EMPTY-PIECE -> PIECE-EMPTY), 
            piece took piece (PIECE1-PIECE2 -> EMPTY-PIECE1 or PIECE1-PIECE2 -> PIECE2-EMPTY),
            piece moved and promoted (PIECE-EMPTY -> EMPTY-PIECE_PROM or EMPTY-PIECE -> PIECE_PROM-EMPTY)
            piece took and promoted (PIECE1-PIECE2 -> EMPTY-PIECE1_PROM or PIECE1-PIECE2 -> PIECE2_PROM-EMPTY)
        """
        i1, j1 = changed_cells[0]
        i2, j2 = changed_cells[1]

        cell_1_old = old_board.figures[i1][j1]
        cell_2_old = old_board.figures[i2][j2]
        cell_1_new = new_board.figures[i1][j1]
        cell_2_new = new_board.figures[i2][j2]

        # PIECE-EMPTY -> EMPTY-PIECE
        # PIECE1-PIECE2 -> EMPTY-PIECE1
        if cell_1_new == Figure.EMPTY and cell_2_new != Figure.EMPTY and cell_2_new == cell_1_old:
            moved_figure = cell_2_new
            x_origin = j1 + 1
            y_origin = i1 + 1
            x_destination = j2 + 1
            y_destination = i2 + 1
            move_type = MoveType.MOVE

        # EMPTY-PIECE -> PIECE-EMPTY
        # PIECE1-PIECE2 -> PIECE2-EMPTY
        elif cell_2_new == Figure.EMPTY and cell_1_new != Figure.EMPTY and cell_1_new == cell_2_old:
            moved_figure = cell_1_new
            x_origin = j2 + 1
            y_origin = i2 + 1
            x_destination = j1 + 1
            y_destination = i1 + 1
            move_type = MoveType.MOVE

        # PIECE-EMPTY -> EMPTY-PIECE_PROM (PIECE != Gold / King)
        # PIECE1-PIECE2 -> EMPTY-PIECE1_PROM (PIECE1 != Gold / King)
        elif (
                cell_1_new == Figure.EMPTY
                and cell_2_new != Figure.EMPTY
                and cell_1_old.is_promotable()
                and cell_2_new == cell_1_old.promoted()
        ):
            moved_figure = cell_1_old
            x_origin = j1 + 1
            y_origin = i1 + 1
            x_destination = j2 + 1
            y_destination = i2 + 1
            move_type = MoveType.MOVE_AND_PROMOTE

        # EMPTY - PIECE -> PIECE_PROM - EMPTY (PIECE != Gold / King)
        # PIECE1 - PIECE2 -> PIECE2_PROM - EMPTY (PIECE2 != Gold / King)
        elif (
                cell_2_new == Figure.EMPTY
                and cell_1_new != Figure.EMPTY
                and cell_2_old.is_promotable()
                and cell_1_new == cell_2_old.promoted()
        ):
            moved_figure = cell_2_old
            x_origin = j2 + 1
            y_origin = i2 + 1
            x_destination = j1 + 1
            y_destination = i1 + 1
            move_type = MoveType.MOVE_AND_PROMOTE

        else:
            return None

        return Move(
            move_type=move_type,
            figure=moved_figure,
            destination=(x_destination, y_destination),
            origin=(x_origin, y_origin)
        )

    else:
        return None
