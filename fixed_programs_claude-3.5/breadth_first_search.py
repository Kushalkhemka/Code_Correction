# Fixed Program: breadth_first_search (Claude 3.5 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: Variable shadowing in list comprehension where 'node' was used both as the outer loop variable and inner comprehension variable, causing incorrect successor node access
# Fixed on: 2025-05-27 13:41:50
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: Variable shadowing in list comprehension where 'node' was used both as the outer loop variable and inner comprehension variable, causing incorrect successor node access

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