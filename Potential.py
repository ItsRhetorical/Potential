import os
import sys
import time
from msvcrt import getch
from msvcrt import kbhit
from colorama import init
from colorama import Fore, Back, Style
init()

Grid = {}
cursor = [0, 0]
lastKey = ""
gridSizeX = 20
gridSizeY = 20
StepsPerIteration = 5
TimePerStep = .3
simulate = True


class Tile:
    def __init__(self, location, item, field):
        self.location = location
        self.item = item
        self.field = field

def buildGrid():
    for x in range(gridSizeX):
        for y in range(gridSizeY):
            tile = Tile((x, y), "", 0)
            Grid[x, y] = tile


def averageOfNeighbors(grid, _x, _y):
    if _x == 0:
        left = 0
    else:
        left = grid[_x - 1, _y].field

    if _y == 0:
        down = 0
    else:
        down = grid[_x, _y - 1].field

    if _x == gridSizeX - 1:
        right = 0
    else:
        right = grid[_x + 1, _y].field

    if _y == gridSizeY - 1:
        up = 0
    else:
        up = grid[_x, _y + 1].field
    return (left + right + up + down)/4.0


def simulationIterations(numberOfIterations):
    for i in range(numberOfIterations):
        for x in range(gridSizeX):
            for y in range(gridSizeY):
                if Grid[x, y].item == "source":
                    Grid[x, y].field = 9
                Grid[x, y].field = averageOfNeighbors(Grid, x, y)
                if Grid[x, y].item == "source":
                    Grid[x, y].field = 9


def drawScreen(_grid):
    os.system("cls")
    sys.stdout.write("\033[0;0H")
    for y in range(gridSizeY):
        for x in range(gridSizeX):
            field = _grid[(x, y)].field
            if field > 0:
                sys.stdout.write(Back.RED)
            if cursor[0] == x and cursor[1] == y:
                sys.stdout.write(Back.WHITE)
            sys.stdout.write(str("{:10.4f}".format(field)))
            sys.stdout.write(Style.RESET_ALL+" ")
        sys.stdout.write("\n")
        sys.stdout.flush()


buildGrid()
while True:
    time.sleep(TimePerStep)
    if kbhit():
        key = ord(getch())
        if key == 120:  # x
            print("Exit")
            break
        elif key == 32:  # space
            print("Pause")
            simulate = not simulate
        elif key == 113:  # q
            print("spawn")
            Grid[cursor[0], cursor[1]].item = "source"
            Grid[cursor[0], cursor[1]].field = 9
            simulate = True
        elif key == 97:  # a
            print("left")
            cursor[0] -= 1
            simulate = False
            drawScreen(Grid)
        elif key == 100:  # d
            print("right")
            cursor[0] += 1
            print(cursor)
            simulate = False
            drawScreen(Grid)
        elif key == 119:  # w
            print("up")
            cursor[1] -= 1
            simulate = False
            drawScreen(Grid)
        elif key == 115:  # s
            print("down")
            cursor[1] += 1
            simulate = False
            drawScreen(Grid)
        new_cursor = [0 if i < 0 else i for i in cursor]  # change all negatives to 0
        cursor = new_cursor
    if simulate:
        simulationIterations(StepsPerIteration)
        drawScreen(Grid)










































