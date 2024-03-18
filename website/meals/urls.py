from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('components/', views.components_view, name = 'components'),
]