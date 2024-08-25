@echo off
@chcp 65001 > nul

set line=------------------------------
set project_name=NewProject

:: Парсинг параметров командной строки
:loop
  if "%1" == "" goto :main
  if "%1" == "-n" (
  	if not "%2" == "" (
  	  set project_name=%2
  	)
  )
  shift
  goto loop


:main
:: Создание каталога
echo %line%
echo Preparing workspace
rd /S /Q %project_name%
md %project_name%
cd %project_name%


:: Инициализация виртуального окружения
echo %line%
echo Creating virtual enviroment
mkdir django
python -m venv django/venv
call django/venv/scripts/activate.bat


:: Установка зависимостей
echo %line%
echo Installing dependencies
echo %line%
python -m pip install --upgrade pip
pip install django
pip freeze > django/requirements.txt


:: Основная конфигурация прокта
echo %line%
echo Project configure
django-admin startproject settings
move settings\* django > NUL
move settings/settings django > NUL
rd /S /Q settings
cd django
echo %line%
echo Applying migrations
python manage.py migrate


:: Создание папок

:: Под приложения
mkdir apps


cd ..
:: Создание git-репозитория


:: Создание .gitignore
echo #Virtual enviroment>> .gitignore
echo venv>> .gitignore
echo.>> .gitignore

echo #Enviroment variables>> .gitignore
echo .env>> .gitignore
echo.>> .gitignore

echo #Python cache>> .gitignore
echo __pycache__>> .gitignore
echo.>> .gitignore

echo #Datebase files and dirs>> .gitignore
echo db.sqlite3>> .gitignore
echo.>> .gitignore


echo %line%
cd ..
deactivate
