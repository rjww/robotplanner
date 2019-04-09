#!/usr/bin/env python


import math
import os
import sys

from queue import PriorityQueue
from typing import List, Tuple


class ArgumentError(Exception):
    pass


Cell = Tuple[int, int]


class Grid:
    def __init__(self, width: int, height: int, walls: List[Cell]):
        self.width = width
        self.height = height
        self.walls = {cell for cell in walls if self.in_bounds(cell)}

    def in_bounds(self, cell: Cell):
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def unoccupied(self, cell: Cell):
        return cell not in self.walls

    def neighbours(self, cell: Cell):
        x, y = cell
        neighbours = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        neighbours = filter(self.in_bounds, neighbours)
        neighbours = filter(self.unoccupied, neighbours)
        return list(neighbours)

    def cost(self, a: Cell, b: Cell):
        return 1


class Fringe(PriorityQueue):
    def put(self, cell: Cell, priority: float):
        super().put((priority, cell))

    def get(self):
        _, cell = super().get()
        return cell


def find_path(grid: Grid, start: Cell, goal: Cell):
    fringe = Fringe()
    fringe.put(start, 0)
    path_to = {start: None}
    cost_to = {start: 0}
    nodes_explored = 0

    while not fringe.empty():
        current = fringe.get()

        if current == goal or not grid.unoccupied(current):
            break

        for neighbour in grid.neighbours(current):
            cost = cost_to[current] + grid.cost(current, neighbour)
            if neighbour not in cost_to or cost < cost_to[neighbour]:
                cost_to[neighbour] = cost
                priority = cost + euclidean_dist(neighbour, goal)
                fringe.put(neighbour, priority)
                path_to[neighbour] = current
                nodes_explored += 1

    return path_to, nodes_explored


def euclidean_dist(a: Cell, b: Cell):
    x0, y0 = a
    x1, y1 = b
    return math.hypot(x1 - x0, y1 - y0)


def unwind_path(path_to: dict, goal: Cell):
    current = goal
    path = ''
    path_length = 0

    while path_to[current] is not None:
        path = direction(path_to[current], current) + ' ' + path
        path_length += 1
        current = path_to[current]

    return path, path_length


def direction(orig: Cell, dest: Cell):
    dx = dest[0] - orig[0]
    dy = dest[1] - orig[1]
    if   dy < 0: return 'U'
    elif dy > 0: return 'D'
    elif dx < 0: return 'L'
    else:        return 'R'


def main():
    if len(sys.argv) != 6:
        usage = 'Usage: ./%s filename start_x start_y goal_x goal_y'
        raise ArgumentError(usage % os.path.basename(__file__))

    filename = sys.argv[1]
    start = (int(sys.argv[2]), int(sys.argv[3]))
    goal = (int(sys.argv[4]), int(sys.argv[5]))

    with open(filename, 'r') as file:
        width, height = (int(x) for x in file.readline().split())
        raw_grid = [line.split() for line in file.readlines()]
        walls = [(col, row) for row in range(height) for col in range(width)
                 if raw_grid[row][col] == '1']

    grid = Grid(width, height, walls)
    path_to, nodes_explored = find_path(grid, start, goal)

    if goal not in path_to:
        print(nodes_explored, 0)
        print('X')
    else:
        path, path_length = unwind_path(path_to, goal)
        print(nodes_explored, path_length)
        print(path)

if __name__ == '__main__':
    main()
