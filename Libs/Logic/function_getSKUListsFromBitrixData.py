# Функция getSKUListsFromBitrixData.py возвращает списко гомогенных групп, получяенных на основе файла
# данных из системы Bitrix
from Libs.Logic.function_bitrixParser import parseBitrixData
from Libs.Logic.class_Database import Database
from Libs.Logic.class_Database_1C import Database_1C
from Libs.Logic.class_SKU import SKU
from Libs.Logic.class_SKUList import SKUList

DATABASE = Database().loadDatabase()
DATABASE_1C = Database_1C().loadDatabase()

def getSKUListsFromBitrixData(bitrixFile):
    incomeData = parseBitrixData(bitrixFile)# Парсим файл данных
    correctData = incomeData[0]             # Отделяем коррректные данные
    trashData   = incomeData[1]             # Отделяем некорректные данные
    # Создаем один общий список
    correctList = SKUList()
    for data in correctData:
        correctList.append(SKU(data['Product'],data['Article']))
    # Заполняем значения товарных групп и свойств, где это возможно
    for item in correctList:
        item.setupProductGroupsFromDatabase(DATABASE)
        item.setupProductGroupsFromDatabase(DATABASE_1C)
        item.setupProductGroupsFromInput()
        item.setupPropertiesFromDatabase(DATABASE)
    return correctList.splitToHomogenouses()