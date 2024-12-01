from dataclasses import dataclass
from enum import Enum

@dataclass
class Coordinate:
    """ Describes a coordinate with x and y value."""
    x: int
    y: int


if __name__ == '__main__':
    apa = [Coordinate(1, 2), Coordinate(2, 2)]
    bapa = Coordinate(3, 2)
    print(bapa in apa)

# class PipeType(Enum):
#     HORIZONTAL = '-'
#     VERTICAL = '|'
#     DRB = 'L'
#     DLB = 'J'
#     ULB = '7'
#     URB = 'F'
#     START = 'S'
