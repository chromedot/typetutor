from collections import defaultdict
from typing import List, Dict, Set, Optional
import itertools

class GraphNode:
    def __init__(self, value: int):
        self.value = value
        self.neighbors: List['GraphNode'] = []
        self.visited = False

    def add_neighbor(self, node: 'GraphNode') -> None:
        if node not in self.neighbors:
            self.neighbors.append(node)
            node.neighbors.append(self)

def find_path(start: GraphNode, end: GraphNode) -> Optional[List[int]]:
    queue = [(start, [start.value])]
    visited: Set[int] = {start.value}

    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path

        for neighbor in current.neighbors:
            if neighbor.value not in visited:
                visited.add(neighbor.value)
                queue.append((neighbor, path + [neighbor.value]))

    return None
