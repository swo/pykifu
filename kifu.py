#!/usr/bin/env python3

import math
import xml.etree.ElementTree as ET

class Board:
    def __init__(self):
        self.board_n = 9
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

# line_xs = [board_margin + i * lane_height for i in range(board_n)]

# svg = ET.Element('svg', {'height': str(canvas_size), 'width': str(canvas_size), 'xmlsn': 'http://www.w3.org/2000/svg'})
# for x in line_xs:
#     ET.SubElement(svg, 'line', {'x1': str(board_margin), 'x2': str(canvas_size - board_margin), 'y1': str(x), 'y2': str(x), 'stroke': 'black'})
#     ET.SubElement(svg, 'line', {'y1': str(board_margin), 'y2': str(canvas_size - board_margin), 'x1': str(x), 'x2': str(x), 'stroke': 'black'})

# ET.SubElement(svg, 'circle', {'cx': str(line_xs[3]), 'cy': str(line_xs[4]), 'r': str(stone_radius), 'stroke': 'black', 'fill': 'black'})
# ET.SubElement(svg, 'text', {'x': str(line_xs[3]), 'y': str(line_xs[4]), 'fill': 'white', 'text-anchor': 'middle', 'font-size': str(text_height), 'alignment-baseline': 'middle'}).text = '10'

# ET.SubElement(svg, 'circle', {'cx': str(line_xs[4]), 'cy': str(line_xs[4]), 'r': str(stone_radius), 'stroke': 'black', 'fill': 'white'})
# ET.SubElement(svg, 'text', {'x': str(line_xs[4]), 'y': str(line_xs[4]), 'fill': 'black', 'text-anchor': 'middle', 'font-size': str(text_height), 'alignment-baseline': 'middle'}).text = '11'

# with open('a.html', 'w') as f:
#     print(ET.tostring(svg, encoding='unicode'), file=f)

b = Board()
b.add_stone(3, 4, 'black', 10)
b.add_stone(4, 4, 'white', 11)
b.write_to('a.html')
