from django.contrib import admin
import main.models as m


# Register your models here. All of these models can now be used by the admin of the site, to edit posts and so on.
# and more importantly, to manage the relationship each model has with other, without the need to come here to the
# server and do stuff. this is a great move for admins.
admin.site.register(m.Post)
admin.site.register(m.Tag)
admin.site.register(m.Comments)
admin.site.register(m.Profile)
admin.site.register(m.WebsiteInfo)
