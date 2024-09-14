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
def helloworld():
    print('Hello World!')