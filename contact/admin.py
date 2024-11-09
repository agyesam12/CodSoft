from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User),
admin.site.register(Contact),
admin.site.register(Feedback),
admin.site.register(Subscription),
admin.site.register(Notifications),

