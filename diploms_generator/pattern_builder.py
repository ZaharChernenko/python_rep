import json
import re
from typing import NamedTuple, Optional


class TextData(NamedTuple):
    text: str
    font_size: float
    font_color: tuple[int, int, int]
    is_bold: bool
    is_italic: bool


class PatternBuilderException(Exception):
    def __init__(self, message: Optional[str] = None):
        self._message: Optional[str] = message


class PatternBuilder:
    def __init__(self, pattern: list[dict]):
        self._pattern: list[dict] = pattern
        self._excel_isolator: re.Pattern = re.compile(r"\[\[((?:\w+\s*)+)\]\]")

    def __call__(self, source_row) -> dict[str, TextData]:
        result: dict[str, TextData] = {}
        for el in self._pattern:
            text: Optional[str] = el.get("текст", None)
            if text is None:
                try:
                    depends_on: str = el["зависит от"]
                except KeyError:
                    raise PatternBuilderException(
                        f'В объекте паттерна нет ни поля "текст", ни поля "зависит от"\n {el}'
                    )
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

            try:
                type_of_text: str = el["тип"]
            except KeyError:
                raise PatternBuilderException(f'В объекте паттерна нет поля "тип"')

            result[type_of_text] = TextData(
                text=text,
                font_size=el.get("размер шрифта", 12),
                font_color=el.get("цвет шрифта", (0, 0, 0)),
                is_bold=el.get("жирный", False),
                is_italic=el.get("курсивный", False),
            )

        return result


if __name__ == "__main__":
    with open("pattern.json") as fin:
        test_pattern = json.load(fin)
    test_builder = PatternBuilder(test_pattern)
    result: dict[str, TextData] = test_builder(
        {
            "Пол": "м",
            "Курс": 1,
            "Группа": "2-МД-21",
            "Номинация": "Лучший доклад",
            "Дата": "26 ноября 2024",
            "ФИО в дательном падеже": "Иванову Сергею Викторовичу",
            "Тема доклада": "Инновации в налогообложении",
            "Научный руководитель": "к.э.н., доцент кафедры бухгалтерского учёта и аудита Павлова Т.А.",
        }
    )
    print(*result.items(), sep="\n")
    print("{Научный руководитель.text}".format(**result))
