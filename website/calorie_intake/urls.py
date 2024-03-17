from django.urls import path
from . import views

app_name = 'calorie_intake'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('definitions/', views.definitions_view, name = 'definitions'),
]