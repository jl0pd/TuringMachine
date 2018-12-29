import random
import time

default_node_char = ' '


class Node(object):

    def __init__(self, *, left: "Node" = None, right: "Node" = None, symbol: str = default_node_char):
        self.__symbol: str
        self.left = left
        self.right = right
        self.symbol = symbol

    def add_left(self):
        self.left = Node(right=self)

    def add_right(self):
        self.right = Node(left=self)

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, sym: str):
        if len(sym) == 1:
            if sym == '*':
                raise ValueError("cannot set symbol '*' for node")
            else:
                self.__symbol = sym
        else:
            raise ValueError(f"symbol must have length 1, not {len(sym)}")

    def __str__(self):
        return self.__symbol


class Tape(object):

    def __init__(self, default_str: str=None, position=0):
        self.active_node: Node = Node()
        self.left: Node = self.active_node
        self.right: Node = self.active_node
        self.size = 1
        self.__active_node_pos: int = 0
        if default_str:
            self.active_node.symbol = default_str[0]
            for c in default_str[1:]:
                self.move_right()
                self.active_node.symbol = c
                self.size += 1
        while self.__active_node_pos != position:
            if self.__active_node_pos > position:
                self.move_left()
            elif self.__active_node_pos < position:
                self.move_right()

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
        while current_node is not None:
            yield current_node
            current_node = current_node.right

    def __str__(self):
        upper: str = ''.join(str(node) for node in self)
        lower: str = ' ' * (self.__active_node_pos - 1) + '^' + ' ' * (self.size - self.__active_node_pos - 1)
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
