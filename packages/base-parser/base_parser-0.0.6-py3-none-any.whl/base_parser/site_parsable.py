from base_parser import Parser

class ParserHTML(Parser):
    def parse(self):
        for i in range(0, 100):
            print(f"ParserHTML: Parsing from {self.url}")