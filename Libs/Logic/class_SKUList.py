# Класс SKUList представляет из себя набор SKU с методами выборки элементов, сравнения наборов, установки свойств
# для всех элементов набора и сохранения наборов в таблицы Excel
import openpyxl
from collections import OrderedDict
from Libs.Logic.constants import IGNORE_HEADERS, GROUPS_TREE, USED_HEADERS, PROPERTIES_DATA
from Libs.Logic.class_SKU import SKU

class SKUList:
    def __init__(self, someList = None):
        # Конструктор принимает в качестве аргумента список или кортеж. Если аргумент явно не передается, создается пустой
        # экземпляр, который в последствии может быть заполнен методом append
        if type(someList)   == tuple:   self.array = list(someList)
        elif type(someList) == list:    self.array = someList[:]
        elif not someList:              self.array = []
        else:                           raise TypeError ('Конструктору класса SKUList передан неверный тип аргумента "{}"'.format(type(someList)))
        self.counter = 0        # Счетчик позиции. Необходим для операций итерации
        self.setupArticleArray()# Список артикулов элементов. Необходим для более быстрого доступа
        self.setupListType()    # Установщик типа набора
# ========== Методы настройки объекта ==========
    def setupArticleArray(self):
        # Метод создает отдельный список артикулов списка SKU для более быстрого поиска элементов по артикулу
        self.articleArray = []
        for sku in self.array:  self.articleArray.append(sku.article)
    def setupListType(self):
        # Метод утановки типа списка. Для гомогенных списков тип равен наименованию ТГ2, для остальных - Смешанный
        if self.isHomogenous() and self.firstItem():
            type_1 = self.firstItem().productGroups[1]
            type_2 = self.firstItem().productGroups[2]
            if type_2.lower() in 'подогреватели, вакууматоры панели домино':
                type_2 = ' '.join(X.capitalize() for X in type_2.split(' '))
            if type_1.lower() == 'встраиваемая техника':
                type_2 += ' ВСТР'
            self.type = type_2
        else:
            self.type = 'Смешанный'
    def firstItem(self):
        # Внутренний метод, возвращающий первый элемент набора
        try:    return self.array[0]
        except: return None
    def isHomogenous(self):
        # Метод возвращает True, если все его SKU принадлежат одной ТГ2. В таком случае набор считается гомогенным
        if self.array:
            productGroup_1 = self.firstItem().productGroups[1]
            productGroup_2 = self.firstItem().productGroups[2]
            for item in self.array:
                if productGroup_1 != item.productGroups[1] or productGroup_2 != item.productGroups[2]: return False
        return True
# ========== Методы изменения набора ==========
    def append(self, someData):
        # Метод добавления элемента в набор. Элемент обязан быть либо экземпляром класса SKU, либо списком или кортежем
        # экземпляров этого класса. Так же item может быть другим объектом SKUList
        if type(someData) == SKU:
            self.array.append(someData)
            self.articleArray.append(someData.article)
            return
        elif type(someData) == SKUList:
            newData = someData.array[:]
        elif type(someData) == list:
            for item in someData:
                if type(item) != SKU: raise TypeError('Список, переданный в метод append() должен содержать только экземпляры SKU!')
            newData = someData[:]
        elif type(someData) == tuple:
            for item in someData:
                if type(item) != SKU: raise TypeError('Кортеж, переданный в метод append() должен содержать только экземпляры SKU!')
            newData = list(someData)
        else:
            raise TypeError('Аргумент, передаваемый методу append() должен быть типом SKU, SKUList или списокм или кортежем!')
        self.array += newData
        for item in newData:
            self.articleArray.append(item.article)
        self.setupListType()
# ========== Перегруженные методы ==========
    def __str__(self):
        # Метод строкового представления объекта списка товаров
        result = ''
        for item in self.array: result += str(item) + '\n'
        return result
    def __len__(self):
        # Перегружаем метод определения длины списка
        return len(self.array)
    def __iter__(self):
        # Метод для реализации итерации списка SKU в цикле for
        return self
    def __next__(self):
        # Метод, определяющий следующий элемент итерации
        if self.counter < len(self.array):
            self.counter += 1
            return self.array[self.counter - 1]
        else:
            self.counter = 0
            raise StopIteration
# ========== Методы класса (внешние конструкторы) ==========
    @classmethod
    def fromExcelTable(cls, givenFile):
        # Метод класса возвращает набор SKU, созданный на основе таблицы Excel, название котрой передается в excelFile
        try:    excelFile = openpyxl.load_workbook(givenFile)
        except: raise FileNotFoundError('Не найден файл "{}". Проверьте наличие файла или путь к нему!'.format(excelFile))
        SHEET = excelFile.worksheets[0] # Выбираем корректную вкладку
        RESULT = []                     # Список результатов
        # Формируем названия ТГ1 и ТГ2 на основе названия вкладки таблицы
        if ' ВСТР' in SHEET.title:
            productGroup_1 = 'Встраиваемая техника'
            productGroup_2 = SHEET.title.rstrip(' ВСТР')
        else:
            for key in GROUPS_TREE.keys():
                for value in GROUPS_TREE[key]:
                    if value == SHEET.title and key != 'Встраиваемая техника':
                        productGroup_1 = key
                        productGroup_2 = value
                        break
        # Формируем список параметров, характерный для данной ТГ2
        key = SHEET.title
        PARAMETERS = []
        for value in PROPERTIES_DATA[key].values():
            if type(value) == str:
                PARAMETERS.append(value)
            else:
                for subvalue in value:
                    PARAMETERS.append(subvalue)
        FIRST_ROW = SHEET[1]            # Получаем список наименований колонок
        # Получаем словарь вида {Наименование поля: индекс колонки}
        HEADERS = {}
        for fieldName in FIRST_ROW:
            if fieldName.value.upper() not in IGNORE_HEADERS:
                HEADERS[fieldName.value] = FIRST_ROW.index(fieldName)
        # Перебираем все строки во вкладке, начиная со второй
        for row in SHEET.iter_rows(min_row = 2):
            # Определяем переменные для данных о товаре
            article = row[HEADERS['Артикул']].value.strip()     # Артикул
            product = row[HEADERS['Название']].value.strip()    # Наименование
            productGroups   = OrderedDict()                     # Товарные группы
            properties      = OrderedDict()                     # Параметры
            productGroups[1] = productGroup_1
            productGroups[2] = productGroup_2
            productGroups[3] = row[HEADERS['Товарная Группа 3']].value
            productGroups[4] = row[HEADERS['Товарная Группа 4']].value
            productGroups[5] = row[HEADERS['Товарная Группа 5']].value
            try:
                for key in PARAMETERS:
                    properties[key] = row[HEADERS[key]].value
            except: print('Неверный ключ "{}" для файла {}|{}'.format(key, productGroup_1, productGroup_2))
            try:    RESULT.append(SKU(product, article, productGroups, properties))
            except: raise KeyError('Проблемы с продуктом "{}"'.format(product))
        return(cls(RESULT))



