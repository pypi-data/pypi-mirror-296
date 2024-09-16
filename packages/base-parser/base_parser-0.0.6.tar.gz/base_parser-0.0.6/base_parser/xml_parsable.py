from base_parser import Parser

class ParserXML(Parser):
    def parse(self):
        for i in range(0, 100):
            print(f"ParserXML: Parsing from {self.url}")