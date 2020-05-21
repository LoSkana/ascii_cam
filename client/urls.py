from django.urls import path

from . import views

urlpatterns = [
    path('t/', views.index_t, name='index_t'),
    path('r/', views.index_r, name='index_r'),
    path('send/', views.send, name='send'),
]
