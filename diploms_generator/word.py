import os

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from pattern_builder import TextData


def fillTemplate(pattern_obj: dict[str, TextData], template_path: str, output_dir: str) -> None:
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for placeholder, (replacement, font_size, font_color, bold, italic) in pattern_obj.items():
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, replacement)
                    if font_size:
                        run.font.size = font_size
                    if font_color:
                        run.font.color.rgb = font_color
                    run.bold = bold
                    run.italic = italic

    # Сохранение документа
    os.makedirs(output_dir, exist_ok=True)
    word_output_path = os.path.join(output_dir, f'{pattern_obj["{ФИО в дательном падеже}"].text}.docx')
    doc.save(word_output_path)

    print(f"Сертификат для {pattern_obj['{ФИО в дательном падеже}'].text} сохранён в {word_output_path}")
