from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'myfarog'
urlpatterns = [
    path('api/myfarog/character/', views.CharacterView.as_view(), name='api-character'),
    path('api/myfarog/character/<int:pk>/', views.CharacterView.as_view(), name='api-character'),
]