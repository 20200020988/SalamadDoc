from django.contrib import admin
from .forms import User

# Register your models here.
admin.site.unregister(User)
admin.site.register(User)