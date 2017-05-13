from Libs.Logic.function_getSKUListsFromBitrixData import *
from Libs.Logic.constructor_excelParameters import constructParametersTable

'''
newLists = getSKUListsFromBitrixData('Input\\no_properties.txt')
for someList in newLists.values():
    if someList.type:
        someList.saveToDetailedTable(someList.type)
    else:
        print(someList.type)
'''

constructParametersTable()