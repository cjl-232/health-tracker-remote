from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('about/', views.about_view, name = 'about'),
    path('login/', views.login_view, name = 'login'),
]