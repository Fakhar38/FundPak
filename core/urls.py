"""
Fundpak app's urls file
"""

from django.urls import path, re_path
from .views import index, login_view, signup_view

app_name = 'core'
urlpatterns = [
    re_path(r'^$', index, name='index'),
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]