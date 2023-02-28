from django.contrib import admin

from .models import *
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(Organiztaion)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)

admin.site.register(Configuration)


admin.site.register(PasswordResetOTP)
