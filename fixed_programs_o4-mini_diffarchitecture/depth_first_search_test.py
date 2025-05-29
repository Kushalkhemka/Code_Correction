from node import Node
from depth_first_search import depth_first_search

"""
Driver to test depth first search
"""
def main():
    station1 = Node("Westminster")
    station2 = Node("Waterloo", None, [station1])
    station3 = Node("Trafalgar Square", None, [station1, station2])
    station4 = Node("Canary Wharf",  None, [station2, station3])
    station5 = Node("London Bridge",  None, [station4, station3])
    station6 = Node("Tottenham Court Road",  None, [station5, station4])

    if depth_first_search(station6, station1):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    nodef =  Node("F")
    nodee =  Node("E")
    noded =  Node("D")
    nodec =  Node("C", None, [nodef])
    nodeb =  Node("B", None, [nodee])
    nodea =  Node("A", None, [nodeb, nodec, noded])

    if depth_first_search(nodea, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    if depth_first_search(nodef, nodee):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    if depth_first_search(nodef, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

    nodee.successors = [nodea]

    if depth_first_search(nodea, nodef):
        print("Path found!", end=" ")
    else:
        print("Path not found!", end=" ")
    print()

if __name__ == "__main__":
    main()