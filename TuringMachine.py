from TuringMachine.CodeObject import Worker
from TuringMachine.Tape import Tape

if __name__ == '__main__':
    file_path = "example.TMProgram"
    file_content = open(file_path).read().split('\n')
    out_file = open("tp_out.txt", "w")
    worker = Worker(file_content)
    tape = Tape("_____h")
    print(str(tape))
    worker.compile()
    worker.run(tape, out_file=out_file)
