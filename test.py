from configobj import ConfigObj


a = ConfigObj(encoding='UTF8')
a.filename = 'output.ini'
a['Тема'] = {}
a['Тема']['Подтема'] = '"Значение"'

a.write()