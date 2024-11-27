from excel_reader import ExcelReader
from pattern_builder import PatternBuilder
from word import fillTemplate

excel_reader: ExcelReader = ExcelReader("tests/table.xlsx")
pattern_builder: PatternBuilder = PatternBuilder("tests/pattern.json")

for el in excel_reader:
    fillTemplate(pattern_builder(el), "tests/Сертификат.docx", "output")
