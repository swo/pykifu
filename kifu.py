#!/usr/bin/env python3

'''
Use https://github.com/jtauber/sgf for parsing the file
https://en.wikipedia.org/wiki/Smart_Game_Format
https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.SubElement
https://developer.mozilla.org/en-US/docs/Web/SVG/Element
'''

import math
import xml.etree.ElementTree as ET
import sgf

class Board:
    def __init__(self, board_n):
        self.board_n = board_n
        self.canvas_size = 200
        self.board_size = self.canvas_size * 0.9
        self.board_margin = (self.canvas_size - self.board_size) / 2
        self.lane_height = self.board_size / (self.board_n - 1)
        self.stone_radius = self.lane_height / 2 * 0.95
        self.text_height = self.stone_radius * math.sqrt(2)

        self.line_xs = [self.board_margin + i * self.lane_height for i in range(self.board_n)]

        self.svg = ET.Element('svg', {'height': str(self.canvas_size), 'width': str(self.canvas_size), 'xmlsn': 'http://www.w3.org/2000/svg'})

        self.add_board_lines()

    def add_line(self, x1, x2, y1, y2):
        ET.SubElement(self.svg, 'line', {'x1': str(x1), 'x2': str(x2), 'y1': str(y1), 'y2': str(y2), 'stroke': 'black'})

    def add_circle(self, cx, cy, r, fill):
        ET.SubElement(self.svg, 'circle', {'cx': str(cx), 'cy': str(cy), 'r': str(r), 'stroke': 'black', 'fill': fill})

    def add_text(self, x, y, text, fill='black'):
        ET.SubElement(self.svg, 'text', {'x': str(x), 'y': str(y), 'fill': fill, 'text-anchor': 'middle', 'font-size': str(self.text_height), 'alignment-baseline': 'middle'}).text = text

    def add_board_lines(self):
        for x in self.line_xs:
            self.add_line(self.board_margin, self.canvas_size - self.board_margin, x, x)
            self.add_line(x, x, self.board_margin, self.canvas_size - self.board_margin)

    def add_stone(self, x, y, stone_color, number):
        assert stone_color in ['white', 'black']
        if stone_color == 'white':
            text_color = 'black'
        else:
            text_color = 'white'

        self.add_circle(self.line_xs[x], self.line_xs[y], self.stone_radius, stone_color)
        self.add_text(self.line_xs[x], self.line_xs[y], str(number), text_color)

    def write_to(self, fn):
        with open(fn, 'w') as f:
            print(ET.tostring(self.svg, encoding='unicode'), file=f)

class Game:
    def __init__(self, board_n, moves=[]):
        self.board_n = board_n
        self.moves = moves

    def board_between(self, start, end):
        board = Board(self.board_n)
        for move in self.moves:
            if move.number is None or move.number < start:
                board.add_stone(move.x, move.y, move.color, '')
            elif start <= move.number <= end:
                board.add_stone(move.x, move.y, move.color, move.number)
            else:
                pass

        return board

class Move:
    def __init__(self, x, y, color, number=None):
        self.x = x
        self.y = y
        self.color = color
        self.number = number

def parse_coords(xy):
    assert len(xy) == 2
    xc = xy[0]
    yc = xy[1]
    letters = 'abcdefghijklmnopqrs'
    x = letters.index(xc)
    y = letters.index(yc)
    return x, y

def parse_game(sgf_string):
    tree = sgf.parse(sgf_string)
    moves = []

    first_alternate = tree.children[0]
    setup_node = first_alternate.nodes[0]
    if 'AB' in setup_node.properties:
        for xy in setup_node.properties['AB']:
            x, y = parse_coords(xy)
            moves.append(Move(x, y, 'black', number=None))

    assert 'SZ' in setup_node.properties
    board_n = int(setup_node.properties['SZ'][0])

    for node_i, node in enumerate(first_alternate.nodes[1:]):
        move_n = node_i + 1
        assert len(node.properties) == 1
        raw_color = list(node.properties.keys())[0]

        if raw_color in ['RW', 'RB']:
            break

        assert raw_color in ['W', 'B']
        x, y = parse_coords(node.properties[raw_color][0])

        if raw_color == 'W':
            moves.append(Move(x, y, 'white', move_n))
        elif raw_color == 'B':
            moves.append(Move(x, y, 'black', move_n))

    return Game(board_n, moves)

with open('game.sgf') as f:
    g = parse_game(f.read())

b = g.board_between(6, 10)
b.write_to('a.html')
