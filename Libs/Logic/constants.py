# В этом модуле содержатся константы, используемые при формировании SKU и наборов SKU
from string import ascii_letters
from configobj import ConfigObj
from Libs.Logic.function_getBrands import getBrandNames

LATIN_LETTERS = ascii_letters
RUSSIAN_LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
VALID_ARTICLE_SYMBOLS = LATIN_LETTERS + '1234567890-/.'
AVAILABLE_BRANDS = getBrandNames()
CAPS_BRANDS = ('AEG', 'BORA', 'BORK', 'CASO', 'MBS', 'SMEG', 'V-ZUG', 'WMF')
RUS_TO_LAT = {'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X'}
IGNORE_HEADERS = ('ТИП ТОВАРА','КОЭФ.',"ЕД. ИЗМЕРЕНИЯ", "ЗАРЕЗЕРВИРОВАНО", "ДАТА ИЗМ.", "АКТИВНОСТЬ", "СОРТ.", "ID",
                  "НЕТ СИЦ","УМЕНЬШАТЬ КОЛИЧЕСТВО ПРИ ЗАКАЗЕ", "ДОСТУПНОЕ КОЛИЧЕСТВО", "ДОСТУПНОСТЬ", "КОЛИЧЕСТВО ПОДПИСОК")
USED_HEADERS = ('ТОВАРНАЯ ГРУППА 3', 'ТОВАРНАЯ ГРУППА 4', 'ТОВАРНАЯ ГРУППА 5', 'АРТИКУЛ', 'НАЗВАНИЕ')
GROUPS_TREE = ConfigObj('Database\\Config\\tree_product_groups.ini')
PROPERTIES_DATA = ConfigObj('Database\\Config\\tree_parameters.ini')