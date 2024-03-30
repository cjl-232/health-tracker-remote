from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path(
        route = 'component-definitions/', 
        view = views.component_definitions_view, 
        name = 'component_definitions',
    ),
    path(
        route = 'component-groups/', 
        view = views.component_groups_view, 
        name = 'component_groups',
    ),
]