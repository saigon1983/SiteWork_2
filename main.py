from Libs.Logic.function_getSKUListsFromBitrixData import *

newLists = getSKUListsFromBitrixData('Input\\no_properties.txt')
for someList in newLists.values():
    if someList.type:
        someList.saveToDetailedTable(someList.type)
    else:
        print(someList.type)
