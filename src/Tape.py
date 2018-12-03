import random
import time


class Node(object):

    def __init__(self, left: "Node"=None, right: "Node"=None, symbol: str='a'):
        self.left = left
        self.right = right
        if len(symbol) == 1:
            self.symbol = symbol
        else:
            raise AttributeError(f"symbol must have length 1, not {len(symbol)}")

    def add_left(self):
        self.left = Node(right=self)

    def add_right(self):
        self.right = Node(left=self)

    def __str__(self):
        return self.symbol


class Tape(object):

    def __init__(self):
        self.__active_node_pos: int = 0
        self.active_node: Node = Node()
        self.left: Node = self.active_node
        self.right: Node = self.active_node
        self.size = 1

    def move_left(self):
        if not self.active_node.left:
            self.active_node.add_left()
            self.left = self.active_node
            self.size += 1
            self.__active_node_pos += 1
        self.active_node = self.active_node.left
        self.__active_node_pos -= 1

    def move_right(self):
        if not self.active_node.right:
            self.active_node.add_right()
            self.right = self.active_node
            self.size += 1
            self.right = self.active_node
        self.active_node = self.active_node.right
        self.__active_node_pos += 1

    def __iter__(self):
        current_node: Node = self.left
        while current_node.right is not None:
            yield current_node
            current_node = current_node.right

    def __str__(self):
        upper: str = ''.join(str(node) for node in self)
        lower: str = ' '*(self.__active_node_pos - 1) + '^' + ' '*(self.size - self.__active_node_pos - 1)
        return f"{upper}\n{lower}"

if __name__ == '__main__':
    t = Tape()

    print()
    print()
    for i in range(10):
        print("\x1b[3F")
        time.sleep(0.1)
        print(str(t))
        if random.randint(0, 1):
            t.move_left()
        else:
            t.move_right()
