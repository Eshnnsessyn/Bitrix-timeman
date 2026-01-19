import requests
from datetime import date

# Читаем креды
# wh[0] - вебхук с правами на работу со временем
# wh[1] - вебхук с правами на работу с пользователями
with open('creds', 'r', encoding='utf-8') as c:
    wh = c.read().splitlines()

# Составляем список пользователей, активных в Б24
IDs = []
Users = {}
json_search = {'ACTIVE': 'true',
               'SORT': 'ID',}
response = requests.post(wh[1] + 'user.get', json=json_search)
result = response.json()
for each in result['result']:
    IDs.append(each['ID'])
    Users[each['ID']] = each['LAST_NAME'] + ' ' + each['NAME']
json_search['start'] = 50
response = requests.post(wh[1] + 'user.get', json=json_search)
result = response.json()
for each in result['result']:
    IDs.append(each['ID'])
    Users[each['ID']] = each['LAST_NAME'] + ' ' + each['NAME']

# Неизменные части json_close
json_close = {'REPORT': 'Автозавершение рабочего дня'}
json_status = {}

# Начинаем перебор пользователей для поиска тех, чей день не завершён
# Сразу информация записывается в логфайл по пути logs/YYYY-MM-DD.log
logfile = 'logs/' + str(date.today()) + '.log'
with open(logfile, 'w', encoding='utf-8') as log:
    for each in IDs:
        json_status['USER_ID'] = each
        info = requests.post(wh[0] + 'timeman.status', json=json_status)
        if info.json()['result']['STATUS'] != 'CLOSED':
            json_close['USER_ID'] = each
            requests.post(wh[0] + 'timeman.close', json=json_close)
            log.write(Users[each] + ' - отключён, статус: ' + info.json()['result']['STATUS'] + '\n')