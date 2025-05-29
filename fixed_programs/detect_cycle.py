def detect_cycle(node):
    hare = tortoise = node

    while hare and hare.successor and hare.successor.successor:
        tortoise = tortoise.successor
        hare = hare.successor.successor
        if hare is tortoise:
            return True
    return False


"""
Linked List Cycle Detection
Tortoise-Hare Algorithm

Detects whether a linked list has a cycle using two pointers (tortoise and hare).

Input:
    node: The head node of a linked list

Output:
    Boolean indicating whether the linked list is cyclic
"""
