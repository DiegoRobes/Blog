from django.urls import path
import main.views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('post/<slug:slug>', v.post_page, name='post_page'),
]
