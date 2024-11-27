from excel_reader import ExcelReader
from pattern_builder import PatternBuilder

excel_reader: ExcelReader = ExcelReader("tests/table.xlsx")
pattern_builder: PatternBuilder = PatternBuilder("tests/pattern.json")

for el in excel_reader:
    print(pattern_builder(el))
