from os import listdir
from os.path import isdir
from shutil import rmtree


def recursive_deleting() -> None:
    def inner(path: str):
        for cat in listdir(path):
            if cat == '__pycache__':
                rmtree(f'{path}/__pycache__')
            else:
                if isdir(path + '/' + cat):
                    inner(path + '/' + cat)
    inner('../_assist')
    inner('../data')
    inner('../modules')

if __name__ == '__main__':
    recursive_deleting()
