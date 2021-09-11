from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('travels', views.travels),
    path('travels/add', views.add),
    path('travels/destination/<id>', views.show),
    path('travels/destination/join/<id>', views.join),
    path('travels/destination/cancel/<id>', views.cancel),
    path('travels/destination/destroy/<id>', views.destroy),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout)
]
