# Класс Database_1C является специализированным подклассом Database, хпредставляющим базу данных на основе таблицы 1С
import openpyxl
from collections import OrderedDict
from Libs.Logic.class_SKU import SKU
from Libs.Logic.class_Database import *
from Libs.Logic.constants import TRUE_PG2_1C_NAMES, FIELD_NAMES_1C
from openpyxl.utils import column_index_from_string as colIndex

class Database_1C(Database):
    def __init__(self):
        super().__init__()

    def saveDatabase(self):
        super().saveDatabase('Database\\database_1c.db')

    @classmethod
    def loadDatabase(cls):
        # Метод загрузки возвращает готовую базу данных на основе файла database.db
        with open('Database\\database_1c.db', 'rb') as databaseFile:
            DB = pickle.load(databaseFile)
        return DB

    @classmethod
    def constructDatabase(cls):
        newDatabase = Database_1C()
        excelFile = openpyxl.load_workbook('Database/Excel/1CData.xlsx')
        SHEET = excelFile.active                                                # Активная вкладка
        firstRow = SHEET[1]                                                     # Первая строка вкладки
        HEADERS = {}                                                            # Словарь заголовков
        for cell in firstRow:   HEADERS[cell.value] = colIndex(cell.column) - 1 # Последовательно заполняем словарь
        for row in SHEET.iter_rows(min_row = 2):
            tg2name = row[HEADERS['Товарная группа 2(папка)']].value
            if tg2name not in TRUE_PG2_1C_NAMES.keys(): continue
            if tg2name in TRUE_PG2_1C_NAMES.keys():
                article = row[HEADERS['Артикул ']].value.strip()        # Артикул
                name    = row[HEADERS['Наименование']].value.strip()    # Название
                productGroups = OrderedDict()                           # Товарные группы
                pg_1_2 = TRUE_PG2_1C_NAMES[tg2name]
                productGroups[1] = pg_1_2[0]
                productGroups[2] = pg_1_2[1]
                productGroups[3] = row[HEADERS['Товарная Группа 3 ']].value
                productGroups[4] = row[HEADERS['Товарная Группа 4']].value
                productGroups[5] = row[HEADERS['Товарная Группа 5']].value
                newDatabase.append(SKU(name, article, productGroups))
        return newDatabase