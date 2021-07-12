"""
Fundpak app's urls file
"""

from django.urls import path, re_path
from . import views

app_name = 'core'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('about-us/', views.about_us, name='about_us'),
    path("start_campaign_not_logged/", views.start_campaign_not_logged, name='start_camp_not_logged'),
    path("start_campaign_logged/", views.start_campaign_logged, name='start_camp_logged'),
    path("logout/", views.logout, name='logout'),
    path("product-detail/<prod_id>/", views.product_detail, name='product_detail'),
    path("product_categories/", views.product_categories, name='product_categories'),
    path("featured/", views.featured, name='featured'),
    path("create_checkout_session/", views.create_checkout_session, name='create_checkout'),
    path("payment_success/", views.payment_success, name='payment_success'),
    path("payment_cancel/", views.payment_cancel, name='payment_cancel'),
    path("hooks/", views.hook_listener, name='hooks'),
    path("campaign_1/<prod_id>", views.campaign_1, name='campaign_1'),
    path("campaign_2/<prod_id>", views.campaign_2, name='campaign_2')
]