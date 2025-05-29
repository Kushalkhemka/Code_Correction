def detect_cycle(node):
    hare = tortoise = node
    while hare and hare.successor:
        tortoise = tortoise.successor
        hare = hare.successor.successor
        if hare is tortoise:
            return True
    return False