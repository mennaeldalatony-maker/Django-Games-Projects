from django.contrib import admin
from django.urls import path
from Dungeon_Escape.views import dungeon_game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dungeon_game, name='dungeon_game'),
]
