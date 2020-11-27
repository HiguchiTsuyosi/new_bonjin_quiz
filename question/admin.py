from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Question,Question_hard,Question_normal

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Question_normal)
admin.site.register(Question_hard)