""" Pipes! """

import logging

from utils import read_input_file, submatrix
from dataclasses import dataclass
from enum import Enum


filename = 'test.txt'
# filename = 'test2.txt'
# filename = 'day10.txt'


@dataclass
class Coordinate:
    """ Describes a coordinate with x and y value."""
    x: int
    y: int


class TileType(Enum):
    """ Describes the different tile types."""
    HORIZONTAL = '-'
    VERTICAL = '|'
    L = 'L'
    J = 'J'
    SEVEN = '7'
    F = 'F'
    START = 'S'
    GROUND = '.'


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('day10')


@dataclass
class RelativePosition:
    """ Relative positions. """
    is_above: bool = False
    is_below: bool = False
    is_to_left: bool = False
    is_to_right: bool = False


class Tile:
    """ Describes a tile by its position and its type. """
    def __init__(self, position: Coordinate, tile_type: TileType):
        self.position = position
        self.type = tile_type

    def __str__(self):
        return self.type.value

    def as_pipe(self):
        """ Returns the tile as a pipe """
        if type(self) is Pipe:
            pipe: Pipe = Pipe(self.position, self.type)
            pipe.connected_to = self.connected_to
            return pipe
        else:
            raise Exception(f'Tile of type {self.type.value} is not a pipe.')


class Ground(Tile):
    """ Describes a tile that is ground. """
    def __init__(self, position: Coordinate):
        super().__init__(position, TileType.GROUND)

    def __str__(self):
        return self.type.value


class Pipe(Tile):
    """ Describes a tile that is a pipe. """
    def __init__(self, position: Coordinate, pipe_type: TileType):
        super().__init__(position, pipe_type)
        self.connected_to = []

    @staticmethod
    def is_pipe(tile: str) -> bool:
        """ Checks if the tile is a pipe or not. """
        try:
            TileType(tile)
            return True
        except ValueError:
            logger.debug('%s is not a pipe.', tile)
            return False

    def add_if_connected(self, tile: Tile):
        """ Checks if this pipe is connected to another tile and adds it to this pipe connections if it is."""
        relative_position = self.position_of(tile)
        if type(tile) is Pipe and self.is_connected_to(tile, relative_position):
            self.connected_to.append(tile)
        if len(self.connected_to) > 2:
            logger.warning('To manny connections for tile: (%d, %d)', self.position.x, self.position.y)

    def is_connected_to(self, pipe, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe is connected to the provided pipe. """
        if pipe.type == TileType.HORIZONTAL:
            return self.can_connect_to_horizontal(relative_position)
        if pipe.type == TileType.VERTICAL:
            return self.can_connect_to_vertical(relative_position)
        if pipe.type == TileType.L:
            return self.can_connect_to_l(relative_position)
        if pipe.type == TileType.J:
            return self.can_connect_to_j(relative_position)
        if pipe.type == TileType.SEVEN:
            return self.can_connect_to_7(relative_position)
        if pipe.type == TileType.F:
            return self.can_connect_to_f(relative_position)

    def can_connect_to_horizontal(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can connect to a horizontal pipe at the relative position. """
        if self.type is TileType.VERTICAL:
            return False
        if self.type is TileType.HORIZONTAL and (relative_position.is_to_left or relative_position.is_to_right):
            return True
        if self.type in [TileType.L, TileType.F] and relative_position.is_to_right:
            return True
        if self.type in [TileType.J, TileType.SEVEN] and relative_position.is_to_left:
            return True
        return False

    def can_connect_to_vertical(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can be connected to a vertical pipe at the relative position. """
        if self.type is TileType.HORIZONTAL:
            return False
        if self.type is TileType.VERTICAL and (relative_position.is_above or relative_position.is_below):
            return True
        if self.type in [TileType.L, TileType.J] and relative_position.is_above:
            return True
        if self.type in [TileType.F, TileType.SEVEN] and relative_position.is_below:
            return True
        return False

    def can_connect_to_l(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can connect to an L pipe at the relative position. """
        if self.type is TileType.L:
            return False
        if self.type in [TileType.HORIZONTAL, TileType.J, TileType.SEVEN] and relative_position.is_to_left:
            return True
        if self.type in [TileType.VERTICAL, TileType.SEVEN, TileType.F] and relative_position.is_below:
            return True
        return False

    def can_connect_to_j(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can connect to an J pipe at the relative position. """
        if self.type is TileType.J:
            return False
        if self.type in [TileType.HORIZONTAL, TileType.L, TileType.F] and relative_position.is_to_right:
            return True
        if self.type in [TileType.VERTICAL, TileType.SEVEN, TileType.F] and relative_position.is_below:
            return True
        return False

    def can_connect_to_7(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can connect to an 7 pipe at the relative position. """
        if self.type is TileType.SEVEN:
            return False
        if self.type in [TileType.HORIZONTAL, TileType.L, TileType.F] and relative_position.is_to_right:
            return True
        if self.type in [TileType.VERTICAL, TileType.L, TileType.J] and relative_position.is_above:
            return True
        return False

    def can_connect_to_f(self, relative_position: RelativePosition) -> bool:
        """ Checks if this pipe can connect to an F pipe at the relative position. """
        if self.type is TileType.F:
            return False
        if self.type in [TileType.HORIZONTAL, TileType.J, TileType.SEVEN] and relative_position.is_to_left:
            return True
        if self.type in [TileType.VERTICAL, TileType.L, TileType.J] and relative_position.is_above:
            return True
        return False

    def position_of(self, pipe) -> RelativePosition:
        """ Calculates the relative position of the pipe to self. """
        above = self.position.x == pipe.position.x and self.position.y == pipe.position.y + 1
        bellow = self.position.x == pipe.position.x and self.position.y == pipe.position.y - 1
        to_the_left = self.position.x == pipe.position.x + 1 and self.position.y == pipe.position.y
        to_the_right = self.position.x == pipe.position.x - 1 and self.position.y == pipe.position.y
        return RelativePosition(above, bellow, to_the_left, to_the_right)

    def __str__(self):
        return f'({self.position.x}, {self.position.y})'
        # return self.type.value


class Engine:
    """ An engine that moves along the pipes. """
    def __init__(self, matrix: list[list[Tile]], start_position: Coordinate):
        self.matrix = matrix
        self.start_pipe: Pipe = self.matrix[start_position.y][start_position.x].as_pipe()
        self.is_at_pipe: Pipe = self.start_pipe
        self.came_from = None
        self.path: list[Pipe] = []

    def traverse_loop(self) -> list[Pipe]:
        """ Traverses the loop until reaching the start again. """
        path = []
        done = False
        while not done:
            done, is_at_position = self.move()
            path.append(is_at_position)
        return path

    def move(self) -> (bool, Coordinate):
        """ Makes a step to the next pipe in the current direction.
         If the current pipe is the start pipe it picks the first connected pipe it finds."""
        if not self.came_from:
            self.is_at_pipe = self.start_pipe.connected_to[0]
            self.came_from = self.start_pipe
        else:
            temp = self.is_at_pipe
            self.is_at_pipe = self.find_next()
            self.came_from = temp
        self.path.append(self.is_at_pipe)
        return self.is_at_pipe.position == self.start_pipe.position, self.is_at_pipe

    def find_next(self):
        """ Finds the next pipe to move to. """
        for pipe in self.is_at_pipe.connected_to:
            if pipe.position != self.came_from.position:
                return pipe
        raise Exception("Nothing found!")


def part1():
    """ Solves part 1. """
    logger.info('Starting part 1')
    matrix, start_position = parse_input()
    start_pipe_type = find_start_pipe_type(matrix, start_position)
    logger.info('Starting at %s', start_pipe_type)
    matrix[start_position.y][start_position.x].type = start_pipe_type
    add_connections(matrix)
    engine = Engine(matrix, start_position)
    path = engine.traverse_loop()
    logger.info('Total length of loop: %d, halfway at: %d', len(path), len(path) / 2)


def part2():
    """ Solves part 2. """
    logger.info('Starting part 2')
    matrix, start_position = parse_input()
    start_pipe_type = find_start_pipe_type(matrix, start_position)
    matrix[start_position.y][start_position.x].type = start_pipe_type
    add_connections(matrix)
    engine = Engine(matrix, start_position)
    path = engine.traverse_loop()



def find_start_pipe_type(matrix: list[list[Tile]], start_position: Coordinate) -> TileType:
    """ Finds the pipe type of the start pipe. """
    sub_matrix = submatrix(matrix, 1, start_position.x, start_position.x, start_position.y)
    center = find_start(sub_matrix)
    up = get_at_pos_or_none(sub_matrix, center.x, center.y, 'up')
    left = get_at_pos_or_none(sub_matrix, center.x, center.y, 'left')
    down = get_at_pos_or_none(sub_matrix, center.x, center.y, 'down')
    right = get_at_pos_or_none(sub_matrix, center.x, center.y, 'right')
    if up in [TileType.VERTICAL, TileType.SEVEN, TileType.F] and down in [TileType.VERTICAL, TileType.L, TileType.J]:
        return TileType.VERTICAL
    if left in [TileType.HORIZONTAL, TileType.L, TileType.F] and right in [TileType.HORIZONTAL, TileType.J, TileType.SEVEN]:
        return TileType.HORIZONTAL
    if up in [TileType.VERTICAL, TileType.SEVEN, TileType.F] and right in [TileType.HORIZONTAL, TileType.SEVEN, TileType.J]:
        return TileType.L
    if up in [TileType.VERTICAL, TileType.SEVEN, TileType.F] and left in [TileType.HORIZONTAL, TileType.F, TileType.L]:
        return TileType.J
    if left in [TileType.HORIZONTAL, TileType.L, TileType.F] and down in [TileType.VERTICAL, TileType.L, TileType.J]:
        return TileType.SEVEN
    if right in [TileType.HORIZONTAL, TileType.SEVEN, TileType.J] and down in [TileType.VERTICAL, TileType.L, TileType.J]:
        return TileType.F
    raise Exception('Could not find center pipe type')


def get_at_pos_or_none(sub_matrix: list[[Tile]], x, y, direction: str):
    """ Gets the tile at the x and y position in the matrix or None if it is out of bounds. """
    if direction == 'up':
        if y - 1 < 0:
            return None
        else:
            return sub_matrix[y - 1][x].type
    if direction == 'left':
        if x - 1 < 0:
            return None
        else:
            return sub_matrix[y][x - 1].type
    if direction == 'down':
        if y + 1 > len(sub_matrix):
            return None
        else:
            return sub_matrix[y + 1][x].type
    if direction == 'right':
        if x + 1 > len(sub_matrix[y]):
            return None
        else:
            return sub_matrix[y][x + 1].type
    raise Exception(f'Could not move {direction} in {sub_matrix}')


def find_start(matrix) -> Coordinate:
    """ Finds the start pipe in the matrix. """
    for row_index, row in enumerate(matrix):
        for column_index, column in enumerate(row):
            if type(column) is Pipe and column.type is TileType.START:
                return Coordinate(column_index, row_index)
    raise Exception('Could not find start node.')


def parse_input() -> (list[list[Tile]], Coordinate):
    """ Parses the input data and returns the matrix and the start position. """
    matrix = []
    start_position = None
    lines = read_input_file(file_name=filename)
    for row_index, line in enumerate(lines):
        row = []
        for column_index, char in enumerate(line):
            position = Coordinate(column_index, row_index)
            if Pipe.is_pipe(char):
                pipe = Pipe(position, TileType(char))
                row.append(pipe)
                if pipe.type is TileType.START:
                    start_position = position
            else:
                row.append(Ground(position))
        matrix.append(row)
    return matrix, start_position


def add_connections(matrix: list[list[Tile]]):
    """ Goes through the matrix and adds the connections to all pipes. """
    for row in matrix:
        for tile in row:
            if type(tile) is Pipe:
                sub_matrix = submatrix(matrix, 1, tile.position.x, tile.position.x, tile.position.y)
                for sub_matrix_row in sub_matrix:
                    for sub_matrix_column in sub_matrix_row:
                        tile.add_if_connected(sub_matrix_column)



if __name__ == '__main__':
    part1()
    part2()
