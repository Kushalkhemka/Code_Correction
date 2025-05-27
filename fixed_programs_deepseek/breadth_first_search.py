# Fixed Program: breadth_first_search (DeepSeek)
# Bug Classification: Incorrect variable
# Bug Description: The line 'nodesseen.update(node.successors)' unconditionally adds all successors of the current node to the 'nodesseen' set, even if they were already filtered out for the queue. This can lead to inefficiency and incorrect behavior by revisiting nodes unnecessarily.
# Fixed on: 2025-05-27 12:52:43
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect variable
# This indicates: The line 'nodesseen.update(node.successors)' unconditionally adds all successors of the current node to the 'nodesseen' set, even if they were already filtered out for the queue. This can lead to inefficiency and incorrect behavior by revisiting nodes unnecessarily.

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
            queue.extend(node for node in node.successors if node not in nodesseen)
            nodesseen.update(node for node in node.successors if node not in nodesseen)

    return False


"""
Breadth-First Search


Input:
    startnode: A digraph node
    goalnode: A digraph node

Output:
    Whether goalnode is reachable from startnode
"""