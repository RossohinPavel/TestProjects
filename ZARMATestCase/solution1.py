"""
# 1. Подключение к API и получение данных
Напишите скрипт на Python, который подключается к API и получает данные. 
Например, используйте публичное API https://jsonplaceholder.typicode.com/posts. 
Сохраните полученные данные в формате JSON в файл.

"""
# Воспользуемся библиотекой requests для отправки запроса на API
import requests


response = requests.get('https://jsonplaceholder.typicode.com/posts')


# Так как данные с этого api нам возвращаются в формате json 
# (это можно проверить по заголовку 'Content-Type'),
# то их можно сохранить побайтово без лишних преобразований.
if not ('Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']):
    exit()


with open('file.json', 'wb') as file:
    file.write(response.content)


# Проверим, что все сохранилось верно и информация  конвертируется в json
import json


with open('file.json') as file:
    res = json.load(file)


print(*res, sep='\n')
