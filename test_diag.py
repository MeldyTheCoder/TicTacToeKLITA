import math

diagonal = 5
total_cells = diagonal**2

points_to_win = 3

board = [{"selected": None, "id": cell} for cell in range(total_cells)]

def get_bord_diag(board: list[dict]):
    return int(math.sqrt(len(board)))

def get_cell_diag(cell_id: int, board: list[dict]):
    cell = board[cell_id]
    diagonal = get_bord_diag(board)
    diags = []

    if diagonal - cell_id % diagonal >= points_to_win - 1 and cell_id // diagonal >= points_to_win - 1:
        print("Up left")
        diags.append([cell_id - (diagonal + 1) * 2, cell_id - (diagonal + 1) * 1, cell_id])

    if cell_id % diagonal >= points_to_win - 1 and cell_id // diagonal >= points_to_win - 1:
        print("Up right")
        diags.append([cell_id - (diagonal - 1) * 2, cell_id - (diagonal - 1) * 1, cell_id])

    if cell_id % diagonal <= points_to_win:
        print("Down right")
        diags.append([cell_id, cell_id + (diagonal + 1) * 1, cell_id + (diagonal + 1) * 2])

    if not cell_id % diagonal < points_to_win:
        print("Down left")
        diags.append([cell_id, cell_id + (diagonal - 1) * 1, cell_id + (diagonal - 1) * 2])

    return diags

print(get_cell_diag(12, board))