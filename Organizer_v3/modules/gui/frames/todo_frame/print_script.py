import os
import modules.app_manager as APP


@APP.THREAD_MANAGER.parallel
def print_tasks(tasks: list[str]) -> None:
    """
        Сохраняет текст задач в временный файл.
        Открывает его и вызывает функцию печати.
    """
    path = 'data/temp.txt'

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(tasks)
    
    match os.name:
        case 'posix': os.popen('xdg-open ' + path)
        case 'nt': os.startfile('\\'.join(path.split('/')), 'print')
        # case 'nt': os.popen(('notepad -p ', '\\'.join(path.split('/')))'notepad ' + '\\'.join(path.split('/')) + ' -p')
        # case 'posix': os.popen('lp ' + path)
