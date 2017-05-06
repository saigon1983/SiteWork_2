# Класс SKU является виртуальным представлением единицы товара
from collections import OrderedDict
from Libs.Logic.constants import AVAILABLE_BRANDS, CAPS_BRANDS, VALID_ARTICLE_SYMBOLS, RUS_TO_LAT, PROPERTIES_DATA
from Libs.Logic.function_fixBrands import fixBrandNames
from Libs.Logic.function_detectPGs import detectPG

class SKU:

    def __init__(self, name, article = '', productGroups = {}, properties = {}):
        '''
        Конструктор класса принимает следующий параметры:
        :param name:            название товара вида <Тип прибора Бренд Модель>
        :param article:         артикул товара. При отсутствии, артикулом становится модель за вычетом всех лишних символов
        :param productGroups:   словарь товарных групп вида {номер товарной группы: название товарной группы}
        :param properties:      словарь параметров вида {имя поля параметра: значение параметра}
        :return:                экземпляр класса SKU
        '''
        self.parseName(name)
        self.setupArticle(article)
        self.setupProductGroups(productGroups)
        self.setupProperties(properties)
# ========== Методы настройки объекта ==========
    def parseName(self, name):
        # Метод разбирает переданное имя продукта name и формирует на его основе тип прибора, его ренд и модель
        if type(name) != str: raise TypeError('Конструктору имени передан неверный аргумент name! Ожидалось: "str", получено: {}'.format(type(name)))
        currentName = name.upper()      # Переводим имя в верхний регистр
        # Задаем значения полей по умолчанию
        productBrand    = ''    # Бренд
        productGenus    = ''    # Тип прибора
        productModel    = ''    # Модель
        for brandName in AVAILABLE_BRANDS:
            if brandName in currentName:
                productBrand = fixBrandNames(brandName)         # Правим и фиксируем бренд
                splitted = currentName.split(brandName + ' ')   # Получаем кортеж из типа прибора и модели
                productGenus = splitted[0]                      # Тип прибора
                productModel = " ".join(splitted[1:])           # Модель прибора
        # Производим проверку написания бренда
        if productBrand not in CAPS_BRANDS: productBrand = productBrand.title()
        # Производим установку атрибутов экземпляр
        self.brand = productBrand.strip()
        self.model = productModel.strip()
        self.genus = productGenus.strip().capitalize()
        if 'свч' in self.genus: self.genus = self.genus.replace('свч', 'СВЧ')
    def setupArticle(self, article):
        # Метод установки артикула. Если артикула нет, артикулом становится модель прибора
        if not article:
            self.article = ''
            for letter in self.model:
                if letter in VALID_ARTICLE_SYMBOLS: self.article += letter
        else:
            self.article = article.upper()
        # Редактируем получившийся артикул на предмет замены русских букв на латинские и удаления ненужных символов
        if ' ' in self.article: self.article = self.article.replace(' ','') # Удаляем пробелы
        for letter in self.article:                                         # Заменяем русские буквы на латинские
            if letter in RUS_TO_LAT.keys(): self.article = self.article.replace(letter, RUS_TO_LAT[letter])
        # Выполняем финальную проверку на отсутствие лишних символов в артикуле
        for letter   in self.article:
            if letter not in VALID_ARTICLE_SYMBOLS: raise ValueError('Некорректный символ "{}" в артикуле "{}"'.format(letter, self.article))
    def setupProductGroups(self, productGroups):
        # Метод установки товарных групп. Принимает на вход словарь вида {Номер ТГ: Название ТГ}
        self.productGroups = OrderedDict()
        try:    self.productGroups[1] = productGroups[1].capitalize()
        except: self.productGroups[1] = ''
        try:    self.productGroups[2] = productGroups[2]
        except: self.productGroups[2] = ''
        try:    self.productGroups[3] = productGroups[3].lower()
        except: self.productGroups[3] = ''
        try:    self.productGroups[4] = productGroups[4].lower()
        except: self.productGroups[4] = ''
        try:    self.productGroups[5] = productGroups[5].lower()
        except: self.productGroups[5] = ''
        # TODO: Продолжить автозаполнение товарных групп методами выбора из базы данных и ручного ввода
        self.initProperties()
    def initProperties(self):
        # Метод инициализации типов свойств. Задает ключи с пустыми значениями, соответствующими товарной группе
        self.properties = OrderedDict()
        if self.productGroups[1] and self.productGroups[2]:
            key = self.productGroups[2]
            if self.productGroups[1] == 'Встраиваемая техника': key += ' ВСТР'
            for value in PROPERTIES_DATA[key].values():
                if value != '0':
                    if type(value) == str:
                        self.properties[value] = ''
                    else:
                        for subvalue in value:
                            self.properties[subvalue] = ''
    def setupProperties(self, properties):
        # Метод установки свойств (характеристик) продуктов
        if self.properties and properties:
            for key in self.properties.keys(): self.properties[key] = properties[key]
    def setupProductGroupsFromDatabase(self, database):
        # Метод установки корректных товарных групп на основе какой-либо базы данных database
        changed = False
        if not self.productGroups[1] or not self.productGroups[2]:
            for someSKU in database:
                if someSKU.article == self.article:
                    changed = True
                    for key, value in someSKU.productGroups.items():
                        self.productGroups[key] = value
        if changed: self.initProperties()
    def setupProductGroupsFromInput(self):
        # Метод ручной настройки товарных групп (1й и 2й) путем ручного выбора из предлагаемых вариантов
        if not self.productGroups[1] or not self.productGroups[2]:
            self.productGroups[1], self.productGroups[2] = detectPG(self)
        self.initProperties()
    def setupPropertiesFromDatabase(self, database):
        # Метод установки свойств из базы данных database
        for someSKU in database:
            if someSKU.article == self.article:
                self.setupProperties(someSKU.properties)
# ========== Методы доступа к атрибутам объекта ==========
    def getName(self):
        # Метод возвращает традиционное написание продукта в виде <Тип продукта Бренд Модель>
        return '{} {} {}'.format(self.genus, self.brand, self.model)
    def getInfo(self):
        # Метод возвращает строковое представление всей доступной о продукте информации
        info = ''
        info += self.getName() + '\n'
        for productGroup in self.productGroups:
            if self.productGroups[productGroup]:
                info += '|{}: {} '.format(productGroup, self.productGroups[productGroup])
        info += '\n'
        for property in self.properties:
            if self.properties[property]:
                info += '{}: {}'.format(property, self.properties[property]) + '\n'
        return info
# ========== Перегруженные методы ==========
    def __str__(self):
        # Метод строковго представления объекта
        return self.getName()
    def __eq__(self, other):
        # Метод поврехностного сравнения объектов. Две SKU считаются равными, если равны их артикулы
        return self.article == other.article