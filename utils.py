""" Utils """
from icecream import ic

def read_input_file(folder: str = 'data', file_name: str = 'test.txt', remove_blank_lines=True) -> [str]:
    with open(f'{folder}/{file_name}') as file:
        data = file.readlines()
    response = [line.strip() for line in data if line.rstrip()] if remove_blank_lines else [line.strip() for line in data]
    return response


def number_of_input_lines(folder: str = 'data', file_name: str = 'test.txt') -> int:
    return len(read_input_file(folder, file_name))


def submatrix(in_matrix: list[[]], size: int, start_index: int, end_index: int, row: int) -> list[[]]:
    """ Creates a sub matrix of size extra items around the center (x, y) """
    start_column: int = start_index - size if start_index >= size else 0
    end_column: int = end_index + size if end_index + size < len(in_matrix[row]) else len(in_matrix[row])
    start_row: int = row - size if row >= size + 1 else 0
    end_row: int = row + size if row + size < len(in_matrix) else len(in_matrix)
    ic.disable()
    ic(start_column, end_column, start_row, end_row)
    ic.enable()
    sub_matrix = [a_row[start_column:end_column + 1] for a_row in in_matrix[start_row:end_row + 1]]
    return sub_matrix


def print_matrix(matrix):
    """ Prints the values of the matrix. """
    for row in matrix:
        for column in row:
            print(str(column), end='')
        print()
    print()
