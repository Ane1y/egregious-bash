from src.Parser import *
from src.Lexer import *
from src.Extender import *
from src.Executable import *


class App:
    def __init__(self):
        pass

    def run(self):
        text = input(" > ")
        lexer = Lexer(text)
        extender = Extender(lexer.get())
        parser = Parser(extender.get())

        self.execute(parser.get())

    def execute(self, prog: Program):

        for cmd in prog.commands:
            raise NotImplemented



if __name__ == '__main__':
    app = App()
    app.run()