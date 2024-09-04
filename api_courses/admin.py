from django.contrib import admin
from . import models

admin.site.register(models.Subject)
admin.site.register(models.Module)
admin.site.register(models.Course)
admin.site.register(models.Student)
admin.site.register(models.Item)
admin.site.register(models.Content)