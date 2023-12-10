
from parse import parse
from dataclasses import dataclass
from typing import Optional
import itertools
import math

@dataclass
class Node:
    name: str
    left_name: str
    right_name: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def is_start(self):
        return self.name[2] == "A"
    def is_end(self):
        return self.name[2] == "Z"
    
    def __repr__(self):
        return f'Node({self.name} ({self.left_name} {self.right_name}))'
    
    

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

def steps_to_closest_end_node(from_node, instructions):
    current_node = from_node
    steps = 0
    # print(f"*{from_node.name}")
    while steps == 0 or not current_node.is_end():
        steps += 1
        dir = next(instructions)
        prev_node = current_node
        if dir == "L":
            # print(f"*L to {current_node.left.name}")
            current_node = current_node.left
        if dir == "R":
            # print(f"*R to {current_node.right.name}")
            current_node = current_node.right
    return (steps, current_node)

def steps_to_closest_end_nodes(from_nodes, instructions):
    current_nodes = from_nodes
    steps = 0
    # print(f"*{list(map(lambda n: n.name, current_nodes))}")
    while not all(map(Node.is_end, current_nodes)):
        steps += 1
        dir = next(instructions)
        if dir == "L":
            current_nodes = list(map(lambda n: n.left, current_nodes))
            # print(f"*L to {list(map(lambda n: n.name, current_nodes))}")
        if dir == "R":
            current_nodes = list(map(lambda n: n.right, current_nodes))
            # print(f"*R to {list(map(lambda n: n.name, current_nodes))}")
        if steps % 100000 == 0:
            print(f"Steps: {steps}")
    print(f"Last instruction: {dir}")
    return (steps, current_nodes)

def lcm(a, b):
    return a*b // math.gcd(a, b)

with open("08/day8-input.txt", "r", encoding="utf-8") as file:
    instruction_list = list(file.readline().strip())
    instructions = itertools.cycle(instruction_list)
    file.readline()

    node_list = list(map(parse_node, file))
    node_dict = dict(map(lambda n: (n.name, n), node_list))

    start_nodes = list(filter(Node.is_start, node_list))
    end_nodes = list(filter(Node.is_end, node_list))

    for node in start_nodes:
        resolve_edges(node, node_dict)

    iterations = []
    for start in start_nodes:
        instructions = itertools.cycle(instruction_list)
        steps, end = steps_to_closest_end_node(start, instructions)
        print(f"{start} steps: {steps} end: {end} iterations: {steps / len(instruction_list)}")

        # Validate that we are at the end of the instruction set
        if steps % len(instruction_list) != 0:
            print(f"Assumption that we are at end of instruction list is not correct")
            exit()

        # Validate that there there is a loopback from the end to the end in the same number of instructions
        # If these hold (as an analysis of the test data shows they do) then we can proceed with our approach
        loop_back_steps, loop_back_end = steps_to_closest_end_node(end, instructions)
        if loop_back_end != end or loop_back_steps != steps:
            print(f"Assumption that end loops back to end in same number of steps is not correct")
            exit()

        instruction_iterations = int(steps / len(instruction_list))
        iterations.append(instruction_iterations)

    print(iterations)

    lcm_all_numbers = iterations[0]
    for n in iterations[1::]:
        lcm_all_numbers = lcm(lcm_all_numbers, n)
    
    iterations_needed = lcm_all_numbers
    steps_needed = iterations_needed * len(instruction_list)

    print(f"Steps needed: {steps_needed}")
    