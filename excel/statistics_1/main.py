import statistics

import openpyxl

name = "Расчетное задание №1.xlsx"
try:
    wb = openpyxl.load_workbook(name)
except FileNotFoundError:
    print(f"Файла с именем {name} не существует")
    exit(1)

input_ws = wb["Лист1"]
stats = statistics.DiscreteRandomVars(input_ws, name=name)

output_ws = wb.create_sheet(title="output")
stats.writeBaseValues(output_ws)
graph, row = stats.writeRowExpValSubject2ColVal(output_ws)

for column in output_ws.columns:
    column_letter = column[0].column_letter
    length = 0
    for cell in column:
        length = max(length, len(cell.value) + 2 if isinstance(cell.value, str) else 0)
    output_ws.column_dimensions[column_letter].width = length

stats.writeGraphic(sheet=output_ws, graphic=graph, row=row)

wb.save(name)
print("Расчеты сохранены в лист output")
