# Выполнение тестового задания для Robita


## Ручной запуск

### Тестовый веб-сервер django

Веб Сервер-Plus, который иитирует протокол https.
Производить запуск командой:
```bash
python manage.py runserver_plus --cert-file cert.crt
```

### backend-сервер 

Производить запуск командой:
```bash
uvicorn main:app --reload --host=127.0.0.1
```
