from django.contrib import admin
from django.urls import path
from Word_Cipher.views import word_cipher_game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', word_cipher_game, name='word_cipher_game'),
]