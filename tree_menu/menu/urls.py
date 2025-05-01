from django.urls import path

from menu.views import home_view


app_name = "menu"

urlpatterns = [
    path('', home_view, name='home'),
]
