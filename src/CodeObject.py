import re
from functools import partial
from typing import List, Dict, Set

from src.Tape import Tape


class CodeString(object):
    __slots__ = ("block_name", "change_from", "change_to", "move_to", "go_to", "__original")

    def __init__(self, code_str: str):
        self.__original = code_str
        if self.__match_pattern():
            tokens = code_str.split()
            self.block_name = tokens[0]
            self.change_from = tokens[1]
            self.change_to = tokens[2]
            self.move_to = tokens[3]
            self.go_to = tokens[4]
        else:
            raise SyntaxError(f"""string "{code_str}" doesn't match pattern""")

    def __match_pattern(self):
        block_name = r"\w+"
        available_chars = r"""[0-9 _a-zA-Z*:;'"\|/,.?()]"""
        directions = r"[lhrLHR]"
        pattern = f"{block_name} {available_chars} {available_chars} {directions} {block_name}"
        code_re = re.compile(pattern)
        result = re.findall(code_re, self.__original)
        return result

    def __str__(self):
        return self.__original


def code_func(*, t: Tape, s: CodeString):
    if s.change_to != '*':
        t.active_node.symbol = s.change_to

    if s.move_to in 'Rr':
        t.move_right()
    else:
        t.move_left()
    return s.go_to


class Worker(object):

    def __init__(self, code_strings: List[str]):
        self.__blocks: List[CodeString] = [CodeString(_str) for _str in code_strings]
        self.__in_names: Set[str] = set()
        self.__out_names: Set[str] = set()
        self.__compiled: Dict[str, Dict[str, type(lambda: ())]] = dict()

    def __find_names(self):
        for code_obj in self.__blocks:
            self.__in_names.add(code_obj.block_name)
            self.__out_names.add(code_obj.go_to)

        if "start" not in self.__in_names or "end" not in self.__out_names:
            raise SyntaxError("'start' and 'end' must be in code")

    def compile(self):
        self.__find_names()

        for in_name in self.__in_names:
            self.__compiled[in_name] = dict()

        for code_obj in self.__blocks:
            self.__compiled[code_obj.block_name][code_obj.change_from] = partial(code_func, s=code_obj)

    def run(self, tape: Tape, out_file=None):
        current_block = "start"
        while current_block != "end":
            block = self.__compiled[current_block]
            current_symbol = tape.active_node.symbol
            line_in_block_by_code = block[current_symbol]
            current_block = line_in_block_by_code(t=tape)

        if out_file:
            out_file.write(str(tape))
        else:
            print(str(tape))
