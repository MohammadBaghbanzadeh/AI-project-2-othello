class Node:
    def __init__(self, value, depth, parent: 'Node' = None, children: '[Node]' = []) -> None:
        self.value = value
        self.depth = depth
        self.children = children
        self.parent = parent

    def Print(self):
        print(f"value: {self.value}, depth: {self.depth}, parent: {self.parent}, children: {self.children}")

    def __repr__(self):
        return f"(value: {self.value}, depth: {self.depth}, parent: {self.parent})"


root = Node(None, 3, None)
n1 = Node(1, 2, root)
n2 = Node(2, 2, root)
root.children = [n1, n2]

n3 = Node(3, 1, n1)
n4 = Node(4, 1, n1)
n1.children = [n3, n4]

n5 = Node(5, 1, n2)
n6 = Node(6, 1, n2)
n2.children = [n5, n6]

n7 = Node(7, 0, n3)
n8 = Node(8, 0, n3)
n3.children = [n7, n8]

height_of_tree = 3
root = Node(None, height_of_tree, None)
par = root
ind = height_of_tree
for i in range(height_of_tree):
    ind -= 1
    first_child = Node(None, ind, par)
    second_child = Node(None, ind, par)
    par.children = [first_child, second_child]


# root.children[0].children[0].Print()
