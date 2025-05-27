def detect_cycle(node):
    hare = tortoise = node
 
    while True:
        # Fix: Check if hare is None or its successor is None to avoid AttributeError
        if hare is None or hare.successor is None:
            return False
 
        tortoise = tortoise.successor
        hare = hare.successor.successor
 
        if hare is tortoise:
            return True


"""
Linked List Cycle Detection
Uses the tortoise-hare cycle detection algorithm

Input:
    node: The head of a linked list

Output:
    True if a cycle is detected, False otherwise
"""
