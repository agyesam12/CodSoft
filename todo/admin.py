from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User),
admin.site.register(Todo),
admin.site.register(LetsVibe),
admin.site.register(Profile),
admin.site.register(Subscription),
admin.site.register(FAQs),
admin.site.register(Feedback),
admin.site.register(Notifications),