from django.urls import path
import main.views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('post/<slug:slug>', v.post_page, name='post_page'),
    path('tag/<slug:slug>', v.tag_page, name='tag_page'),
    path('author/<slug:slug>', v.author_page, name='author_page'),
]
