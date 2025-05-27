# Fixed Program: node (Claude 3.7 Sonnet)
# Bug Classification: Incorrect method called
# Bug Description: Method names 'successor', 'successors', and 'predecessors' conflicted with instance variables of the same names, causing infinite recursion when these methods were called. The methods needed to be renamed to avoid this naming conflict.
# Fixed on: 2025-05-27 22:54:12
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect method called
# This indicates: Method names 'successor', 'successors', and 'predecessors' conflicted with instance variables of the same names, causing infinite recursion when these methods were called. The methods needed to be renamed to avoid this naming conflict.

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