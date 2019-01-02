import re
from typing import List, Dict, Set

from .Tape import Tape


class CodeObject(object):
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
        available_chars = r"""[0-9_a-zA-Z*:;'"\|/,.?()]"""
        directions = r"[lhrLHR]"
        pattern = f"{block_name} {available_chars} {available_chars} {directions} {block_name}"
        code_re = re.compile(pattern)
        result = re.match(code_re, self.__original)
        return result

    def __str__(self):
        return self.__original

    def __call__(self, t: Tape):
        if self.change_to != '*':
            t.active_node.symbol = self.change_to

        if self.move_to in 'Rr':
            t.move_right()
        elif self.move_to in 'Ll':
            t.move_left()

        return self.go_to


class Worker(object):
    class CodeDict(dict):

        def __init__(self):
            def error_func(t: Tape):
                raise KeyError(f"No matching action for '{t.active_node.symbol}' symbol")

            self.__func = error_func
            super().__init__()

        def __setitem__(self, key, value: CodeObject):
            if key == '*':
                self.__func_any = CodeObject
            else:
                super().__setitem__(key, value)

        def __missing__(self, key):
            return self.__func

    def __init__(self, code_strings: List[str]):
        self.__blocks: List[CodeObject] = [CodeObject(s) for s in code_strings if s.strip()]
        self.__in_names: Set[str] = set()
        self.__out_names: Set[str] = set()
        self.__compiled: Dict[str, Dict[str, type(lambda: ())]] = dict()

    def compile(self):
        for code_obj in self.__blocks:
            block_name = code_obj.block_name
            self.__in_names.add(block_name)
            if block_name not in self.__compiled.keys():
                self.__compiled[block_name] = Worker.CodeDict()
                self.__compiled[block_name].setdefault('*')
            self.__out_names.add(code_obj.go_to)

        if "start" not in self.__in_names or "end" not in self.__out_names:
            raise SyntaxError("'start' and 'end' must be in code")

        for code_obj in self.__blocks:
            self.__compiled[code_obj.block_name][code_obj.change_from] = code_obj

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
