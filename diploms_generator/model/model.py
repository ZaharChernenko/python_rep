import os
import time

from docx2pdf import convert

from .excel_reader import ExcelReader
from .pattern_builder import PatternBuilder
from .word_filler import WordFiller, WordFillerOutput


class DiplomsGeneratorModel:
    def __init__(self, *, template_file_path: str, excel_file_path: str, pattern_file_path: str):
        self.pattern_builder: PatternBuilder = PatternBuilder(pattern_file_path)
        self.excel_reader: ExcelReader = ExcelReader(excel_file_path)
        self.word_filler: WordFiller = WordFiller(template_file_path)

    def __call__(self):
        output_dir: str = f"output_{int(time.time())}"
        os.makedirs(output_dir, exist_ok=True)
        for row in self.excel_reader:
            result: WordFillerOutput = self.word_filler((self.pattern_builder(row)))
            result.document.save(os.path.join(output_dir, result.file_name))
            print(f"Сертификат {result.file_name} сохранён в {output_dir}")
        convert(output_dir)
