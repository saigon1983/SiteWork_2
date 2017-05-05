# В этом модуле описана функция для парсинга таблицы данных из 1С
import openpyxl
from Libs.Logic.class_SKUList import *
from Libs.Logic.constants import TRUE_PG2_1C_NAMES, FIELD_NAMES_1C

def parse1CData(excelFile):
    try:    excelFile = openpyxl.load_workbook(excelFile)
    except: raise FileNotFoundError('Файл {} базы данных 1С не найден!'.format(excelFile))
    SHEET = excelFile.active
    firstRow = SHEET[1]
    HEADERS = {}
    for cell in firstRow:
        HEADERS[cell.value] = cell.column
    newList = SKUList()
    for row in SHEET.iter_rows(min_row = 2):
        article = row[openpyxl.utils.column_index_from_string(HEADERS['Артикул ']) - 1].value.strip()
        name = row[openpyxl.utils.column_index_from_string(HEADERS['Наименование']) - 1].value.strip()
        productGroups = OrderedDict()
        pg_1_2 = TRUE_PG2_1C_NAMES[row[openpyxl.utils.column_index_from_string(HEADERS['Товарная группа 2(папка)']) - 1].value.strip()]
        productGroups[1] = pg_1_2[0]
        productGroups[2] = pg_1_2[1]
        productGroups[3] = row[openpyxl.utils.column_index_from_string(HEADERS['Товарная Группа 3 ']) - 1].value
        productGroups[4] = row[openpyxl.utils.column_index_from_string(HEADERS['Товарная Группа 4']) - 1].value
        productGroups[5] = row[openpyxl.utils.column_index_from_string(HEADERS['Товарная Группа 5']) - 1].value
        try:
            newList.append(SKU(name, article, productGroups))
        except: print(name)
    #print(newList)