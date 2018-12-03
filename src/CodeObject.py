import re
from typing import List


class CodeStructure(object):
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
            raise SyntaxError(f'string "{code_str}" doesnt match pattern')

    def __match_pattern(self):
        code_re = re.compile(r"\w+ \w \w [lhrLHR] \w+")
        result = re.findall(code_re, self.__original)
        return bool(result)

    def __str__(self):
        return self.__original


class Code(object):

    def __init__(self, code_strings: List[str]):
        self.__codes = [CodeStructure(_str) for _str in code_strings]

    def compile(self):
        pass
