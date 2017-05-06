# Класс Database является потомком класса SKUList, но поддерживает интерфейс записи/чтения в/из файл(а)
# и необходим для локализации всех известных SKU в одном месте
import os, pickle
from Libs.Logic.class_SKUList import SKUList

class Database(SKUList):
    def __init__(self):
        # Конструктор создает пустой класс
        super().__init__()
    def saveDatabase(self, databasepath = 'Database\\database.db'):
        # Метод записи сохраняет все данные класса в файл database.db
        with open(databasepath, 'wb') as databaseFile:
            pickle.dump(self, databaseFile)
    @classmethod
    def loadDatabase(cls, databasepath = 'Database\\database.db'):
        # Метод загрузки возвращает готовую базу данных на основе файла database.db
        with open(databasepath, 'rb') as databaseFile:
            DB = pickle.load(databaseFile)
        return DB
    @classmethod
    def constructDatabase(cls):
        # Метод формирует базу данных на основе всех имеющихся в папке Excel таблиц данных
        newDatabase = Database()
        for dirlist in os.walk('Database\\Excel\\Product groups'):
            for file in dirlist[-1]:
                folderPath = dirlist[0]
                newList = SKUList.fromExcelTable(os.path.join(folderPath,file))
                newDatabase.append(newList)
        return newDatabase