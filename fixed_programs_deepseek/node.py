# Fixed Program: node (DeepSeek)
# Bug Classification: Incorrect method called
# Bug Description: The method 'successor' was defined with the same name as the attribute 'successor', causing a naming conflict. The method was renamed to 'get_successor' to avoid this conflict.
# Fixed on: 2025-05-27 12:52:31
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect method called
# This indicates: The method 'successor' was defined with the same name as the attribute 'successor', causing a naming conflict. The method was renamed to 'get_successor' to avoid this conflict.

class Node:
    def __init__(self, value=None, successor=None, successors=[], predecessors=[], incoming_nodes=[], outgoing_nodes=[]):
        self.value = value
        self.successor = successor
        self.successors = successors
        self.predecessors = predecessors
        self.incoming_nodes = incoming_nodes
        self.outgoing_nodes = outgoing_nodes

    def get_successor(self):
        return self.successor

    def get_successors(self):
        return self.successors

    def get_predecessors(self):
        return self.predecessors