from Libs.Logic.function_getSKUListsFromBitrixData import *
from Libs.Logic.function_1CParser import parse1CData

'''
newLists = getSKUListsFromBitrixData('Input\\no_properties.txt')
for someList in newLists.values():
    if someList.type:
        someList.saveToDetailedTable(someList.type)
    else:
        print(someList)
'''

Table1C = parse1CData('Database/Excel/1CData.xlsx')