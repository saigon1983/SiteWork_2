from Libs.Logic.function_bitrixParser import parseBitrixData
from Libs.Logic.class_SKU import SKU
from Libs.Logic.class_SKUList import SKUList
from Libs.Logic.class_Database import Database

someData = parseBitrixData('Input\\no_properties.txt')

newDatabase = Database.constructDatabase()
newDatabase.saveDatabase()