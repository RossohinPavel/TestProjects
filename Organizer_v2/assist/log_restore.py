import os
from zipfile import ZipFile


# for file in os.listdir('../logs'):
#     os.remove(f'../logs/{file}')

with ZipFile('logs_backup.zip', 'r') as zipfile:
    zipfile.extractall('../logs')