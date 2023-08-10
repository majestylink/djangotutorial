from django.urls import path

from .views import IndexView, detail, search, add_recipe

app_name = 'recipe'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('s/', search, name='search'),
    path('<slug:slug>/', detail, name='detail'),
]
