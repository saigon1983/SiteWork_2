from Libs.Logic.function_bitrixParser import parseBitrixData
from Libs.Logic.class_SKU import SKU
from Libs.Logic.class_SKUList import SKUList
from Libs.Logic.class_Database import Database

someData = parseBitrixData('Input\\no_properties.txt')

newDatabase = Database.loadDatabase()
m = 0
n = 0
g = 0
for item in newDatabase:
    if item.brand == 'Miele': m += 1
    if item.brand == 'Neff': n += 1
    if item.brand == 'Gaggenau': g += 1
print('Miele: {}'.format(m))
print('Neff: {}'.format(n))
print('Gaggenau: {}'.format(g))
print('Total: {}'.format(m+g+n))
print('Database length = {}'.format(len(newDatabase)))
print('newDatabase length must be {} after removing...'.format(len(newDatabase) - (m+g+n)))
print('======================')
newDatabase.removeAllByBrands('miele', 'neff', 'gaggenau')
m = 0
n = 0
g = 0
for item in newDatabase:
    if item.brand == 'Miele': m += 1
    if item.brand == 'Neff': n += 1
    if item.brand == 'Gaggenau': g += 1
print('Miele: {}'.format(m))
print('Neff: {}'.format(n))
print('Gaggenau: {}'.format(g))
print('Total: {}'.format(m+g+n))
print('Database length = {}'.format(len(newDatabase)))