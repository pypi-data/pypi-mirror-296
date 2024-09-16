import pandas as pd
from base_parser import Parser

class ParserExcel(Parser):
    def parse(self):
        for i in range(0, 100):
            print(f"ParserExcel: Parsing from {self.url}")

# def parse_excel(file_path):
#     df = pd.read_excel(file_path, engine='openpyxl')
#     print("Информация о таблице:")
#     print(df.info())
#     if 'Column1' in df.columns:
#         print("\nУникальные значения в столбце 'Column1':")
#         print(df['Column1'].unique())
#
#
# file_path = 'files/bdu.xlsx'
# parse_excel(file_path)
#