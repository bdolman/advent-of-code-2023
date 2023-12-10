from parse import parse
from dataclasses import dataclass
from typing import Optional
import itertools

@dataclass
class Node:
    name: str
    left_name: str
    right_name: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None

def parse_node(line):
    result = parse("{} = ({}, {})", line.strip())
    name, left_name, right_name = result
    return Node(name, left_name, right_name)

def resolve_edges(node, node_dict):
    if not node.left:
        node.left = node_dict[node.left_name]
        resolve_edges(node.left, node_dict)
    if not node.right:
        node.right = node_dict[node.right_name]
        resolve_edges(node.right, node_dict)

def steps(from_node, to_node, instructions):
    current_node = from_node
    steps = 0
    print(f"*{from_node.name}")
    while current_node != to_node:
        steps += 1
        dir = next(instructions)
        if dir == "L":
            print(f"*L to {current_node.left.name}")
            current_node = current_node.left
        if dir == "R":
            print(f"*R to {current_node.right.name}")
            current_node = current_node.right
    return steps

with open("08/day8-input.txt", "r", encoding="utf-8") as file:
    instruction_list = list(file.readline().strip())
    instructions = itertools.cycle(instruction_list)
    file.readline()

    node_list = list(map(parse_node, file))
    node_dict = dict(map(lambda n: (n.name, n), node_list))
    
    start = node_dict["AAA"]
    end = node_dict["ZZZ"]
    resolve_edges(start, node_dict)
    steps = steps(start, end, instructions)

    print(f"Steps to end: {steps}")