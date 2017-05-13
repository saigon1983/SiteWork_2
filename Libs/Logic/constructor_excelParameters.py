# В этом модуле описана функция создания таблицы параметров для каждой ТГ и сохранения этой таблицы в excel-файл
from configobj import ConfigObj
import openpyxl

def constructParametersTable():
    sourceFile = ConfigObj('Database/Config/tree_parameters.ini')   # Подключаем файл конфигурации
    outputFile = openpyxl.Workbook()                                # Создаем файл Excel
    for tg in sourceFile:
        # Перебираем товарные группы 2 и создаем вкладки для каждой из них
        outputFile.create_sheet(tg, -1)
        currentSheet = outputFile.get_sheet_by_name(tg)
        # Счетчик строк
        line = 1
        for key in sourceFile[tg]:
            # Пишем заголовок подгруппы параметров
            currentSheet['A{}'.format(line)] = key
            currentSheet['A{}'.format(line)].font = currentSheet['A{}'.format(line)].font.copy(bold=True, italic=True)
            line += 1
            if sourceFile[tg][key] == 0 or sourceFile[tg][key] == '0': continue # Пропускаем пустые категории
            # Пишем названия параметров
            if type(sourceFile[tg][key]) == str:
                # Для строк - пишем строку
                result = ''
                for value in sourceFile[tg][key]:
                    result += value
                currentSheet['A{}'.format(line)] = sourceFile[tg][key]
                line += 1
            else:
                # Для списка строк - проходим по списк уи пишем по строке для каждого элемента
                for value in sourceFile[tg][key]:
                    currentSheet['A{}'.format(line)] = value
                    line += 1
    # Удаляем пустую вкладку
    sheet = outputFile.get_sheet_by_name('Sheet')
    outputFile.remove(sheet)
    # Сохраняем таблицу в файл
    outputFile.save('Output\\groups.xlsx')