"""
Скрипт для автоматизации содзания проектов django.
"""
from argparse import ArgumentParser, Namespace
import os
import shutil
import subprocess


class DjangoProjectCreator:
    """Создание django-проекта"""

    def __init__(
        self,
        project_name: str = 'NewProject',
        django_dir_name: str = 'django',
        venv_dir_name: str = 'venv',
        dependencies: list | None = None
    ) -> None:
        self.project_name = project_name
        self.django_dir_name = django_dir_name
        self.venv_dir_name = venv_dir_name
        self.dependencies = self.set_dependicies_list(dependencies)
        self.django_dir = os.path.join(self.project_name, self.django_dir_name)
        self.win_activate_str = 'call ' + os.path.join(self.django_dir, self.venv_dir_name, 'Scripts', 'activate')

    @classmethod
    def from_argparse_namespace(cls, namespace: Namespace):
        """Инициализация класса на основе пространства имен argparse"""
        return cls(
            project_name=namespace.project_name,
            django_dir_name=namespace.django_dir_name,
            venv_dir_name=namespace.venv_dir_name,
            dependencies=namespace.dependencies
        )

    @staticmethod
    def set_dependicies_list(dependencies: list[str] | None) -> list:
        """Кофигурирует список зависимостей для установки. По умолчанию, ставится django последней версии"""
        if dependencies is None:
            return ['django']
        include_django = True
        for dep in dependencies:
            if dep.startswith('django==') or dep == 'django':
                include_django = False
        if include_django:
            dependencies.append('django')
        return dependencies

    @staticmethod
    def console_output(separete_content=False):
        """Декоратор для распечатки документации функции"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                print(func.__doc__, end="", flush=True)
                if separete_content:
                    print('\n' + '-' * 30)
                res = func(*args, **kwargs)
                if separete_content:
                    print('-' * 30, end="", flush=True)
                print(' ... \033[32mdone\033[0m')
                return res
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator

    def console_call(self, *args, venv=False):
        """
        Вызов комманд перечисленных в args как команд ОС. 
        venv=True вызывает эти команды под виртальным окружением
        """
        cmds = []
        if venv:
            cmds.append(self.win_activate_str)
        cmds.extend(args)
        subprocess.call(' && '.join(cmds), shell=True)

    @console_output()
    def preparing_workspace(self):
        """Preparing workspace"""
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)
        apps = os.path.join(self.django_dir, 'apps')
        dirs = (
            self.project_name,  # Основной каталог проекта
            self.django_dir,    # Каталог с джаногой
            apps
        )
        for d in dirs:
            os.mkdir(d)
        with open(os.path.join(apps, '__init__.py'), 'w', encoding='utf-8') as file:
            pass

    @console_output()
    def creating_virtual_enviroment(self):
        """Creating virtual enviroment"""
        path = os.path.join(self.django_dir, 'venv')
        self.console_call(f'python -m venv {path}')

    @console_output(True)
    def install_dependencies(self):
        """Installing dependencies"""
        cmds = [
            'python.exe -m pip install --upgrade pip',
        ]
        for dep in self.dependencies:
            cmds.append(f'pip install {dep}')
        cmds.append(f'pip freeze > {os.path.join(self.django_dir, 'requirements.txt')}')
        self.console_call(*cmds, venv=True)
        
    @console_output(True)
    def configure_project(self):
        """Project configure"""
        manage = os.path.join(self.django_dir, 'manage.py')
        superuser_script = (
            "from django.contrib.auth import get_user_model;"
            "User = get_user_model();"
            "User.objects.create_superuser('root', 'root@mail.com', 'root')"
        )
        cmds = (
            f'django-admin startproject settings {self.django_dir}',
            f'python {manage} migrate',
            f'echo {superuser_script} | python {manage} shell'
        )
        self.console_call(*cmds, venv=True)

    @console_output()
    def create_gitignore(self):
        """Configuring .gitignore"""
        gitignore = (
            '\n'.join(('#Virtual enviroment', self.venv_dir_name)),
            '\n'.join(('#Enviroment variables', '.env')),
            '\n'.join(('#Python cache', '__pycache__')),
            '\n'.join(('#Datebase files and dirs', 'db.sqlite3'))
        )
        with open(os.path.join(self.project_name, '.gitignore'), 'w', encoding='utf-8') as file:
            print(*gitignore, sep='\n\n', file=file)

    def create(self):
        """Основная логика"""
        self.preparing_workspace()
        self.creating_virtual_enviroment()
        self.install_dependencies()
        self.configure_project()
        self.create_gitignore()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-pn',
        '--project_name',
        type=str,
        default='NewProject',
        help='Флаг для задания своего имени для проекта'
    )
    parser.add_argument(
        '-dn',
        '--django_dir_name',
        type=str,
        default='django',
        help='Флаг для задания имени каталогу c django-файлами. Обычно, используют django или backend'
    )
    parser.add_argument(
        '-vn',
        '--venv_dir_name',
        type=str,
        default='venv',
        help='Флаг для задания имени виртуальному окружению'
    )
    parser.add_argument(
        '-d',
        '--dependencies',
        nargs='+',
        default=[],
    )
    namespace = parser.parse_args()
    creator = DjangoProjectCreator.from_argparse_namespace(namespace)
    creator.create()
