#!/usr/bin/env python2

import gomill.sgf
import render_board

with open('jguy.sgf') as f:
    g = gomill.sgf.Sgf_game.from_string(f.read())

br = render_board.BoardRenderer(g.get_size())
nodes = g.get_main_sequence()
root_node = nodes.pop(0)

comment_node_idx = [-1] + [node_i for node_i, node in enumerate(nodes) if node.has_property('C')]

if root_node.has_property('C'):
    print '<p>' + root_node.get('C') + '</p>'

for start_i, end_i in zip(comment_node_idx[:-1], comment_node_idx[1:]):
    unlabeled_nodes = nodes[0: start_i + 1]
    labeled_nodes = nodes[start_i + 1: end_i + 1]
    labels = [i + 1 for i in range(start_i + 1, end_i + 1)]

    svg = br.render(unlabeled_nodes, zip(labeled_nodes, labels))
    print svg
    print '<p>' + labeled_nodes[-1].get('C') + '</p>'
    print
