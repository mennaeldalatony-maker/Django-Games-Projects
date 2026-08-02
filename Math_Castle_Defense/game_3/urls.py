from django.contrib import admin
from django.urls import path
from Math_Defense.views import math_defense_game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', math_defense_game, name='math_defense_game'),
]