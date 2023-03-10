from django.contrib import admin
import main.models as m


# Register your models here.
admin.site.register(m.Post)
admin.site.register(m.Tag)
admin.site.register(m.Comments)
admin.site.register(m.Profile)
#admin.site.register(m.Comments)
