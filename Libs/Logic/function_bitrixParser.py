# Функция parseBitrixData возвращает кортеж из двух списков. В первом перечислены полученные названия продуктов,
# во втором - список строк, которые не удалось распарсить
from Libs.Logic.function_getBrands import getBrandNames

def parseBitrixData(bitrixDataFile):
    trueList = []                                                               # Список определенных продуктов
    junkList = []                                                               # Список неопределнных продуктов
    BRANDS = getBrandNames()                                                    # Получаем список доступных брендов
    with open(bitrixDataFile, 'r') as workFile: fileData = workFile.readlines() # Считываем файл
    # Производим фильтрацию и разбиение данных
    # По разделителю "-----" отсекаем правую часть - артикул, и левую часть - название
    for line in fileData:
        firstSplitResult = {}
        splittedArray = line.split('-----')
        if len(splittedArray) > 1:  article = splittedArray[-1].strip().upper()
        else:                       article = ''
        product = splittedArray[0].strip().upper().split(')')[1].strip()
        firstSplitResult['Product'] = product
        firstSplitResult['Article'] = article
        for brand in BRANDS:
            if brand in firstSplitResult['Product']:
                trueList.append(firstSplitResult)
                break
        if firstSplitResult not in trueList:
            junkList.append(firstSplitResult)
    trueList.sort(key = lambda k: k['Product'])
    return(trueList, junkList)