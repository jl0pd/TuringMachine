from src.CodeObject import Worker
from src.Tape import Tape
import src
src.Tape.default_node_char = '_'
if __name__ == '__main__':
    file_path = "../t_p"
    file_content = open(file_path).read().split('\n')
    out_file = open("../tp_out.txt", "w")
    worker = Worker(file_content)
    tape = Tape("hi there!")
    worker.compile()
    worker.run(tape, out_file=out_file)
