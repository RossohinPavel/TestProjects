import os
from zipfile import ZipFile


with ZipFile('logs_backup.zip', 'w') as zipfile:
    for file in os.listdir('../logs'):
        zipfile.write(os.path.abspath(f'../logs/{file}'), arcname=file)
        os.remove(f'../logs/{file}')
