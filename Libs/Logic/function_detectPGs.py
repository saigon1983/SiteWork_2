# Функция detectPG() запрашивает ручной ввод товарной группы, если не удается определить автоматически на основе
# запрограммированной логики
from configobj import ConfigObj
TGS = ConfigObj('DataFolder\\tradeGroupsTree.ini')

# Версия 1.4

def detectPG(sku):
    # Функция принимает на вход тип прибора и пытается вернуть ТГ2 и соответствующую ей ТГ1, если ТГ2 или ТГ1 однозначно
    # определить не получается, функция запрашивает у пользователя ручной ввод
    # Функция возвращает кортеж (ТГ1, ТГ2)
    sku = sku
    skuType = sku.genus.lower()
    TG1 = ''    # Название ТГ1
    TG2 = ''    # Название ТГ2
    def askTG(groupList):
        while True:
            print('Какая товарная группа у товара "{}":'.format(sku))
            try:
                for i in range(len(groupList)):
                    print('{}. {}'.format(i+1, groupList[i]))
                answer = int(input())
                if answer not in range(1,len(groupList)+1):
                    print('Введите число от 1 до {}!'.format(len(groupList)))
                else:
                    return groupList[answer-1]
                    break
            except:
                print('Введите число от 1 до {}!'.format(len(groupList)))
    if 'холодильник' in skuType:
        if sku.brand.upper() == 'SMEG':
            if         sku.model.upper().startswith('F')    or sku.model.upper().startswith('RF')\
                    or sku.model.upper().startswith('SBS')  or sku.model.upper().startswith('A')\
                    or sku.model.upper().startswith('SMEG') or sku.model.upper().startswith('CVB'): TG1 = 'Бытовая техника'
            else:                                                                                   TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() == 'MIELE':
            if 'i' in sku.model.lower():    TG1 = 'Встраиваемая техника'
            else:                           TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'GAGGENAU':
            if 'RB 29' not in sku.model.lower():    TG1 = 'Встраиваемая техника'
            else:                                   TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'NEFF':
            if sku.model.startswith('KG'):  TG1 = 'Бытовая техника'
            else:                           TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        TG2 = 'Холодильники'
    elif 'морозильн' in skuType:
        TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        TG2 = 'Морозильники'
    elif 'винны' in skuType:
        if sku.brand.upper() == 'SMEG':
            if sku.model.startswith('WF') or sku.model.startswith('SCV'):   TG1 = 'Бытовая техника'
            else:                                                           TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        TG2 = 'Винные шкафы'
    elif 'стиральн' in skuType:
        if sku.brand.upper() == 'SMEG':
            if sku.model.upper().startswith('LST'): TG1 = 'Встраиваемая техника'
            else:                                   TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'MIELE':
            if 'i' in sku.model.lower(): TG1 = 'Встраиваемая техника'
            else:                        TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'NEFF':
            TG1 = 'Встраиваемая техника'
        elif 'i' in sku.model.lower():
            TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        if TG1 == 'Бытовая техника':    TG2 = 'Стиральные машины'
        else:                           TG2 = 'Техника по уходу за бельем'
    elif 'сушильна' in skuType:
        if sku.brand.upper() in ['ASKO', 'BOSCH', 'SIEMENS', 'SMEG']:
            TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'MIELE':
            if 'i' in sku.model.lower():    TG1 = 'Встраиваемая техника'
            else:                           TG1 = 'Бытовая техника'
        else:
            TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        if TG1 == 'Бытовая техника':    TG2 = 'Сушильные машины'
        else:                           TG2 = 'Техника по уходу за бельем'
    elif 'сушильны' in skuType:
        TG1 = 'Бытовая техника'
        TG2 = 'Сушильные шкафы'
    elif 'гладиль' in skuType:
        TG1 = 'Бытовая техника'
        TG2 = 'Гладильные машины'
    elif 'посудомо' in skuType and 'машина' in skuType:
        if sku.brand.upper() in ['GAGGENAU', 'NEFF', 'DE DIETRICH']:
            TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() == 'ASKO':
            if sku.model[2] == '4': TG1 = 'Бытовая техника'
            else:                   TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() == 'MIELE':
            if 'i' in sku.model.lower():    TG1 = 'Встраиваемая техника'
            else:                           TG1 = 'Бытовая техника'
        elif sku.brand.upper() == 'SMEG':
            if sku.model.startswith('L'):   TG1 = 'Бытовая техника'
            else:                           TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Бытовая техника','Встраиваемая техника'])
        TG2 = 'Посудомоечные машины'
    elif 'плита' in skuType or 'варочный' in skuType:
        TG1 = 'Бытовая техника'
        TG2 = 'Варочные центры'
    elif 'духовой' in skuType:
        TG1 = 'Встраиваемая техника'
        TG2 = 'Духовые шкафы'
    elif 'микроволнов' in skuType or 'свч' in skuType and 'для' not in skuType:
        if sku.brand.upper() in ['GAGGENAU', 'ASKO', 'NEFF', 'DE DIETRICH', 'SMEG']:
            TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() == 'MIELE':
            if sku.model[3] == '1': TG1 = 'Малая бытовая техника'
            else:                   TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Малая бытовая техника','Встраиваемая техника'])
        TG2 = 'Микроволновые печи'
    elif 'пароварка' in skuType:
        TG1 = 'Встраиваемая техника'
        TG2 = 'Пароварки'
    elif 'варочная' in skuType:
        TG1 = 'Встраиваемая техника'
        if sku.brand.upper() == 'MIELE':
            if sku.model.startswith('C'):   TG2 = 'Панели Домино'
            elif sku.model.startswith('K'): TG2 = 'Варочные панели'
        elif sku.brand.upper() == 'BORA':
            if sku.model.startswith('B'):   TG2 = 'Варочные панели'
            else:                           TG2 = 'Панели Домино'
        elif sku.brand.upper() == 'ASKO':
            if sku.model[3] != '3': TG2 = 'Варочные панели'
            else:                   TG2 = 'Панели Домино'
        elif sku.brand.upper() == 'GAGGENAU':
            if sku.model.startswith('V') and '295' not in sku.model:    TG2 = 'Панели Домино'
            else:                                                       TG2 = 'Варочные панели'
        elif sku.brand.upper() == 'NEFF':
            if sku.model.startswith('N'):   TG2 = 'Панели Домино'
            else:                           TG2 = 'Варочные панели'
        else:
            TG2 = askTG(['Варочные панели','Панели Домино'])
    elif 'вытяж' in skuType or 'управляющий блок' in skuType or 'блок с подсветк' in skuType and 'для' not in skuType:
        TG1 = 'Встраиваемая техника'
        TG2 = 'Вытяжки'
    elif 'подогреватель' in skuType:
        TG1 = 'Встраиваемая техника'
        TG2 = 'Подогреватели, Вакууматоры'
    elif 'вакуума' in skuType and 'для' not in skuType:
        if sku.brand.upper() in ['GAGGENAU', 'ASKO', 'NEFF', 'DE DIETRICH', 'SMEG', 'MIELE', 'BOSCH', 'SIEMENS']:
            TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() in ['BORK']:
            TG1 = 'Малая бытовая техника'
        else:
            TG1 = askTG(['Малая бытовая техника','Встраиваемая техника'])
        if TG1 == 'Малая бытовая техника':  TG2 = 'Вакууматоры'
        else:                               TG2 = 'Подогреватели, Вакууматоры'
    elif 'пылесос' in skuType and 'для' not in skuType and 'мешки' not in skuType:
        TG1 = 'Пылесосы'
        if sku.brand.upper() == 'MIELE':
            if sku.model.upper().startswith('SJ') or sku.model.upper().startswith('41J'): TG2 = 'Роботы пылесосы'
            elif sku.model.upper().startswith('SH') or sku.model.upper().startswith('41H'): TG2 = 'Вертикальные пылесосы'
            else: TG2 = 'С пылесборником'
        else:
            TG2 = askTG(['С пылесборником','Роботы пылесосы','Вертикальные пылесосы'])
    elif 'кофем' in skuType or 'кофе-м' in skuType and 'для' not in skuType:
        if sku.brand.upper() in ['GAGGENAU', 'ASKO', 'NEFF', 'DE DIETRICH', 'SMEG']:
            TG1 = 'Встраиваемая техника'
        elif sku.brand.upper() == 'MIELE':
            if sku.model.startswith('CM'):  TG1 = 'Малая бытовая техника'
            else:                           TG1 = 'Встраиваемая техника'
        else:
            TG1 = askTG(['Малая бытовая техника','Встраиваемая техника'])
        TG2 = 'Кофемашины'
    elif 'чайник' in skuType and 'для' not in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Электрочайники'
    elif 'тостер' in skuType and 'для' not in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Тостеры'
    elif 'миксер' in skuType and 'для' not in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Миксеры'
    elif 'блендер' in skuType and 'для' not in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Блендеры'
    elif 'мясоруб' in skuType and 'для' not in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Мысорубки'
    elif 'соковыж' in skuType:
        TG1 = 'Малая бытовая техника'
        TG2 = 'Соковыжималки'
    elif sku.brand.upper() == 'MIELE':
        if 'щетк' in skuType or 'щётк' in skuType:
            TG1 = 'Пылесосы'
            TG2 = 'Аксессуары'
        elif 'пылесб' in skuType or 'меш' in skuType:
            TG1 = 'Пылесосы'
            TG2 = 'Расходные материалы'
        elif 'насад' in skuType:
            TG1 = 'Пылесосы'
            TG2 = 'Аксессуары'
        elif 'фильтр' in skuType:
            TG1 = 'Пылесосы'
            TG2 = 'Расходные материалы'
    else:
        TG1 = askTG(list(TGS))
        TG2 = askTG(list(TGS[TG1]))

    return (TG1,TG2)