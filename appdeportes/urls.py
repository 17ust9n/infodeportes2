from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),  # ahora login es la principal
    path('inicio/', views.inicio, name='inicio'),
    path('acerca/', views.acerca, name='acerca'),
    path('noticias/', views.noticias, name='noticias'),
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipo/<int:pk>/', views.detalle_equipo, name='detalle_equipo'),
    path('amistoso/', views.amistoso, name='amistoso'),
    path('guardar_partido/', views.guardar_partido, name='guardar_partido'),
    path('eliminar-partido/<int:partido_id>/', views.eliminar_partido, name='eliminar_partido'),
    path('lista_partidos/', views.lista_partidos, name='lista_partidos'),  # <--- resuelto
    path('seleccion/', views.seleccion_argentina, name='seleccion_argentina'),

    # --- nuevas rutas para usuarios ---
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]
