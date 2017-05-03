# В этом модуле описывается функция, которая возвращает список имен брендов. Имена брендов в этом списке пишутся
# ЗАГЛАВНЫМИ буквами! Список формируется на основе значений, указанных построчно в файле Database\Config\list_brands.txt

def getBrandNames():
    BRANDS = []
    with open('Database\Config\list_brands.txt', 'r') as brandFile:
        for brand in brandFile.readlines():
            BRANDS.append(brand.strip().upper())
    return BRANDS