from rest_framework.authtoken.admin import TokenAdmin

# Возможность в админке выдавать токены доступа к api
TokenAdmin.raw_id_fields = ['user']