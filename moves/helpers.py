from typing import List


# Helper functions
def check_horizontal_winner(
    number_of_sides: int, board: List[List[str | None]]
) -> str | None:
    for row in board:
        if len(row) >= number_of_sides and all(
            len(row) >= 0 and item == row[0] for item in row
        ):
            return row[0]

    return None


def check_vertical_winner(
    number_of_sides: int, board: List[List[str | None]]
) -> str | None:
    if len(board) < number_of_sides:
        return None

    for column_index in range(number_of_sides):
        if column_index >= len(board[0]):
            continue

        start_item = board[0][column_index]
        start_item_count = 0

        for row_index in range(number_of_sides):
            if column_index >= len(board[row_index]):
                break

            if board[row_index][column_index] == start_item:
                start_item_count += 1

        if start_item_count >= number_of_sides:
            return start_item

    return None


def check_diagonal_winner(
    number_of_sides: int, board: List[List[str | None]]
) -> str | None:
    if len(board) < number_of_sides:
        return None

    if any(len(row) <= 0 for row in board):
        return None

    major_axis_start_item = board[0][0]
    minor_axis_start_item = (
        board[0][number_of_sides - 1] if len(board[0]) >= number_of_sides else None
    )
    major_axis_start_item_count = 0
    minor_axis_start_item_count = 0

    for index, row in enumerate(board):
        if row[index] == major_axis_start_item:
            major_axis_start_item_count += 1

        minor_axis_index = number_of_sides - index - 1
        if (
            minor_axis_index < len(row)
            and row[minor_axis_index] == minor_axis_start_item
        ):
            minor_axis_start_item_count += 1

    if major_axis_start_item_count >= number_of_sides:
        return major_axis_start_item

    if minor_axis_start_item_count >= number_of_sides:
        return minor_axis_start_item

    return None
