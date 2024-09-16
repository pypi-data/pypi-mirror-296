from base_parser import Parser


class ParserCustom(Parser):
    def parse(self):
        self.validate()
        for i in range(0, 100):
            print(f"ParserCustom: Parsing from {self.url}")
