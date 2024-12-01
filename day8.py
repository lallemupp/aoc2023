""" Haunted Desert Navigation. """
import datetime
import logging
import math

from icecream import ic
from utils import read_input_file
from re import findall
from itertools import cycle
from multiprocessing import Pool


pattern = r'[A-Z1-9]{3}'

# filename = 'test.txt'
# filename = 'test2.txt'
filename = 'day8.txt'


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("day8")


class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def get(self, move):
        if move == 'L':
            return self.left
        if move == 'R':
            return self.right

    def is_end(self, partial: bool = False):
        return self.name == 'ZZZ' if not partial else self.name.endswith('Z')

class Engine:
    """ An engine that traverses the nodes according to the movement. """
    def __init__(self, movement, nodes):
        self.movement = movement
        self.nodes = nodes

    def move(self):
        """ Traverses the dessert according to the movement and the nodes. """
        count = 0
        current: Node = self.nodes['AAA']
        for move in cycle(self.movement):
            next_name = current.get(move)
            ic(move, next_name)
            next_node = self.nodes[next_name]
            count += 1
            if next_node.is_end():
                return count
            current = next_node

    def multi_move(self, start_name: str) -> list[(int, str)]:
        """ Moves from start node until a node with Z as last letter. """
        count = 0
        found = []
        current = self.nodes[start_name]
        for move in cycle(self.movement):
            count += 1
            next_name = current.get(move)
            next_node = self.nodes[next_name]
            if next_node.name.endswith('Z'):
                found.append((count, next_node.name))
                count = 0
            if len(found) > 1000:
                return found
            current = next_node

    def multiple_move(self):
        count = 0
        current = self.find_start_nodes()
        move_iter = iter(cycle(self.movement))
        while not Engine.done(current):
            move = next(move_iter)
            next_nodes = []
            for node in [self.nodes[name] for name in current]:
                next_nodes.append(node.get(move))
            current = [node for node in next_nodes]
            if count % 1_000_000 == 0:
                logger.info("%s after %d steps", next_nodes, count)
        ic(current)
        return count

    def find_period(self, start_node: Node):
        count = 0
        current = start_node
        move_iter = iter(cycle(self.movement))
        while not current.is_end(partial=True):
            count += 1
            move = next(move_iter)
            next_name = current.get(move)
            current = self.nodes[next_name]
        return count

    @staticmethod
    def done(nodes: list[str]) -> bool:
        """ Checks if the node only contains end nodes or not. """
        for node in nodes:
            if not node.endswith('Z'):
                return False
        return True

    def find_start_nodes(self) -> list[str]:
        """ Finds all nodes that ends with A. """
        return [node for node in self.nodes if node.endswith('A')]


def part1():
    """ Executes the stuff! """
    engine = create_engine()
    steps = engine.move()
    ic(steps)


def done(numbers: list[int], max_number) -> bool:
    for number in numbers:
        if not max_number % number == 0:
            return False
    return True


def find_lowest_common_period(periods) -> int:
    max_period = max(periods)
    max_number = max_period
    count = 0
    while not done(periods, max_number):
        count += 1
        max_number += max_period
        if count % 1_000_000 == 0:
            logger.debug(max_number)
    return max_number


def part2():
    """ Part 2. """
    start = datetime.datetime.now()
    engine = create_engine()
    start_nodes = map(engine.nodes.get, engine.find_start_nodes())
    with Pool(10) as p:
        periods = p.map(engine.find_period, start_nodes)
    ic(periods)
    max_number = find_lowest_common_period(periods)
    ic(max_number)


def create_engine() -> Engine:
    """ Parses input data and convert it to an engine. """
    lines = read_input_file(file_name=filename)
    line_iter = iter(lines)
    movement = next(line_iter)
    nodes = {}
    line = next(line_iter)
    try:
        while line:
            letters = findall(pattern, line)
            nodes[letters[0]] = Node(letters[0], letters[1], letters[2])
            line = next(line_iter)
    except StopIteration:
        ic(len(nodes))
    return Engine(movement, nodes)


if __name__ == '__main__':
    # part1()
    part2()

# 16722109789192057789770047 Too high
# 13_289_612_809_129 Correct!
