import MaxOS
max_os_ver = '1.0.0'
lib_ver = '1.0.2'
def os_load(version:str):
    import time
    print(f'Запуск MaxOS версии {version}')
    time.sleep(2)
    print('Загрузка ядра python-3.12.4')
    time.sleep(1)
    print('Загрузка графического сеанса cmd')
    time.sleep(1)
def os_stop():
    import sys
    print('Остановка MaxOS...')
    import time
    time.sleep(2)
    sys.exit()
def random(num1:int, num2:int):
    import random
    print(f'Ваш результат: {random.randint(num1, num2)}')
def app_command():
    print('Данная команда будет доступна в версии MaxOS-1.1.0, и в версии библиотеки 1.1.0')
def help():
    print('Help      -           Выводит эту справку')
    print('Stop      -           Завершает работу системы')
    print('Calc      -           Считает результат')
    print('Ver       -           Показывает версию OS')
    print('LibVer    -           Показывает версию библиотеки')
    print('На этом пока и всё')
def ver(type:str):
    if type == 'os':
        print(f'Текущая версия MaxOS-{max_os_ver}')
    else:
        print(f'Текущая версия библиотеки MaxOS: {lib_ver}')
