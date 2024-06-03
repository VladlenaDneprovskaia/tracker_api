from django.contrib import admin

from coaches.models import Coach, Mentee, Recommendation

admin.site.register(Coach)
admin.site.register(Mentee)
admin.site.register(Recommendation)
