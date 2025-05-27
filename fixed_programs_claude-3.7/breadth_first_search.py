# Fixed Program: breadth_first_search (Claude 3.7 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: Variable shadowing in list comprehension where the loop variable 'node' overwrote the parent 'node' variable from the outer scope, causing incorrect behavior in the breadth-first search algorithm.
# Fixed on: 2025-05-27 22:42:09
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: Variable shadowing in list comprehension where the loop variable 'node' overwrote the parent 'node' variable from the outer scope, causing incorrect behavior in the breadth-first search algorithm.

from collections import deque as Queue
 
def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while True:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            queue.extend(successor for successor in node.successors if successor not in nodesseen)
            nodesseen.update(node.successors)

    return False



"""
Breadth-First Search


Input:
    startnode: A digraph node
    goalnode: A digraph node

Output:
    Whether goalnode is reachable from startnode
"""