"""
Fundpak app's urls file
"""

from django.urls import path, re_path
from .views import index, login_view, signup_view, about_us, start_campaign_logged, start_campaign_not_logged

app_name = 'core'
urlpatterns = [
    re_path(r'^$', index, name='index'),
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('about-us/', about_us, name='about_us'),
    path("start_campaign_not_logged/", start_campaign_not_logged, name='start_camp_not_logged'),
    path("start_campaign_logged/", start_campaign_logged, name='start_camp_logged'),

]