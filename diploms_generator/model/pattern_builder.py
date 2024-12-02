import json
import re
from typing import NamedTuple, Optional

from docx.shared import Pt, RGBColor


class TextData(NamedTuple):
    text: str
    font_size: Pt
    font_color: RGBColor
    is_bold: bool
    is_italic: bool
    line_spacing: Optional[float] = None


class PatternBuilderException(Exception):
    def __init__(self, message: Optional[str] = None):
        self._message: Optional[str] = message


class PatternBuilder:
    def __init__(self, file_path: str):
        with open(file_path, encoding="utf-8") as fin:
            try:
                pattern: list[dict] = json.load(fin)
            except json.JSONDecodeError:
                raise PatternBuilderException(f"Файл {file_path} поврежден")
        for el in pattern:
            if el.get("текст", None) is None and el.get("зависит от", None) is None:
                raise PatternBuilderException(f'В объекте паттерна нет ни поля "текст", ни поля "зависит от"\n {el}')
            if el.get("тип", None) is None:
                raise PatternBuilderException(f'В объекте паттерна нет поля "тип"')
        self._pattern: list[dict] = pattern
        self._excel_isolator: re.Pattern = re.compile(r"\[\[((?:\w+\s*)+)\]\]")

    def __call__(self, source_row) -> dict[str, TextData]:
        result: dict[str, TextData] = {}
        for el in self._pattern:
            text: Optional[str] = el.get("текст", None)
            if text is None:
                depends_on: str = el["зависит от"]
                try:
                    value = source_row[depends_on]
                except KeyError:
                    raise PatternBuilderException(f"В excel таблице нет поля {depends_on}")
                try:
                    text = el[value]
                except KeyError:
                    raise PatternBuilderException(f"В объекте паттерна нет поля {value}")
            text = self._excel_isolator.sub(lambda match_el: f"{{{match_el.group(1)}}}", text, count=0)
            try:
                text = text.format(**source_row)
            except KeyError as e:
                raise PatternBuilderException(f"В excel таблице нет поля {e}")

            type_of_text: str = el["тип"]

            result[type_of_text] = TextData(
                text=text,
                font_size=Pt(el.get("размер шрифта", 12)),
                font_color=RGBColor(*el.get("цвет шрифта", (0, 0, 0))),
                is_bold=el.get("жирный", False),
                is_italic=el.get("курсивный", False),
                line_spacing=el.get("межстрочный интервал", None),
            )

        return result


if __name__ == "__main__":
    test_builder = PatternBuilder("../tests/pattern.json")
    test_result: dict[str, TextData] = test_builder(
        {
            "Пол": "м",
            "Курс": 1,
            "Группа": "2-МД-21",
            "Номинация": "Лучший доклад",
            "Дата": "26 ноября 2024",
            "Фамилия": "Иванову",
            "Имя": "Сергею",
            "ТемаДоклада": "Инновации в налогообложении",
            "НаучныйРуководитель": "к.э.н., доцент кафедры бухгалтерского учёта и аудита Павлова Т.А.",
        }
    )
    print(*test_result.items(), sep="\n")
    print("%({НаучныйРуководитель})s" % {key: value.text for key, value in test_result.items()})
