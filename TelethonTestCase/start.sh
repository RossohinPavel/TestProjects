#!/bin/sh
python manage.py test api.tests.EnviromentTestCase
python manage.py runserver 0.0.0.0:80

# # Wait for any process to exit
# wait -n

# # Exit with status of process that exited first
# exit $?
