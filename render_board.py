import math
import xml.etree.ElementTree as ET

class BoardRenderer:
    def __init__(self, board_n):
        self.board_n = board_n
        self.canvas_size = 500
        self.board_size = self.canvas_size * 0.9
        self.board_margin = (self.canvas_size - self.board_size) / 2
        self.lane_height = self.board_size / (self.board_n - 1)
        self.stone_radius = self.lane_height / 2 * 0.95
        self.text_height = self.stone_radius * math.sqrt(2)

        self.line_xs = [self.board_margin + i * self.lane_height for i in range(self.board_n)]

        self.svg = ET.Element('svg', {'height': str(self.canvas_size), 'width': str(self.canvas_size), 'xmlsn': 'http://www.w3.org/2000/svg'})
        self.color_dict = {'b': 'black', 'w': 'white'}
        self.other_color = {'b': 'white', 'w': 'black'}

    def render(self, unlabeled_nodes, labeled_nodes):
        svg = ET.Element('svg', {'height': str(self.canvas_size), 'width': str(self.canvas_size), 'xmlsn': 'http://www.w3.org/2000/svg'})
        self._add_board_lines(svg)

        for node in unlabeled_nodes:
            color, (x, y) = node.get_move()
            self._add_stone(svg, x, y, color)

        for node, label in labeled_nodes:
            color, (x, y) = node.get_move()
            self._add_stone(svg, x, y, color, label)

        last_node = labeled_nodes[-1][0]
        if last_node.has_property('LB'):
            for (x, y), text in last_node.get('LB'):
                self._add_text(svg, x, y, text)

        return ET.tostring(svg)

    @staticmethod
    def _add_line(svg, x1, x2, y1, y2):
        ET.SubElement(svg, 'line', {'x1': str(x1), 'x2': str(x2), 'y1': str(y1), 'y2': str(y2), 'stroke': 'black'})

    def _add_board_lines(self, svg):
        for x in self.line_xs:
            self._add_line(svg, self.board_margin, self.canvas_size - self.board_margin, x, x)
            self._add_line(svg, x, x, self.board_margin, self.canvas_size - self.board_margin)

    @staticmethod
    def _add_circle(svg, cx, cy, r, fill):
        ET.SubElement(svg, 'circle', {'cx': str(cx), 'cy': str(cy), 'r': str(r), 'stroke': 'black', 'fill': fill})

    def _add_text(self, svg, x, y, text, fill='black'):
        ET.SubElement(svg, 'text', {'x': str(self.line_xs[x]), 'y': str(self.line_xs[y]), 'fill': fill, 'text-anchor': 'middle', 'font-size': str(self.text_height), 'alignment-baseline': 'middle'}).text = text

    def _add_stone(self, svg, x, y, stone_color, number=None):
        assert stone_color in self.color_dict
        self._add_circle(svg, self.line_xs[x], self.line_xs[y], self.stone_radius, self.color_dict[stone_color])

        if number is not None:
            self._add_text(svg, x, y, str(number), self.other_color[stone_color])
