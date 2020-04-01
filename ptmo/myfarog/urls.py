from django.urls import include, path
from django.conf.urls import url

from . import views

app_name = 'myfarog'
urlpatterns = [
    path('api/myfarog/character/', views.CharacterApi.as_view(), name='api-character'),
    path('api/myfarog/character/<int:pk>/', views.CharacterApi.as_view(), name='api-character'),
    path('api/myfarog/battle/', views.BattleApi.as_view(), name='api-battle'),
    path('api/myfarog/battle/<int:pk>/', views.BattleApi.as_view(), name='api-battle'),
    path('api/myfarog/battle/<int:battle_id>/round/', views.BattleRoundApi.as_view(), name='api-battle-round'),
    path('api/myfarog/battle/<int:battle_id>/round/<int:round>/', views.BattleRoundApi.as_view(), name='api-battle-round'),
    path('api/myfarog/battle/<int:battle_id>/round/<int:round>/action/', views.BattleRoundActionApi.as_view(), name='api-battle-round-action'),
    
    path('view/myfarog/battle/', views.BattleView, name='view-battle'),

    path('django-rq/', include('django_rq.urls'))
]