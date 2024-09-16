from base_parser import Parser
class ParserPDF(Parser):
    def parse(self):
        for i in range(0, 100):
            print(f"ParserPDF: Parsing from {self.url}")