from django.urls import path
from . import views

app_name = 'weight'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('setup/', views.setup_view, name = 'setup'),
]