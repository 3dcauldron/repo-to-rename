from django.contrib import admin
from users.models import User
# Register your models here.
admin.site.unregister(User)
admin.site.register(User)