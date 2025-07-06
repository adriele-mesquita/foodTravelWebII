from django.urls import path
from . import views 

urlpatterns = [
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('horario/', views.horario, name='horario'),
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('pedido/', views.pedido, name='pedido'),
    path('contato/', views.contato, name='contato'), 
    path('cadastro/', views.cadastro_page, name='alguma_url_de_cadastro'), 
    path('', views.homepage, name='homepage'),
    path('login/', views.login_page, name='login'),
    path('criar_pedido/', views.criar_pedido, name='criar_pedido'),
    path('catalogo1/', views.catalogo1, name='catalogo1'),
    path('catalogo2/', views.catalogo2, name='catalogo2'),
    path('catalogo3/', views.catalogo3, name='catalogo3'),
    path('catalogo4/', views.catalogo4, name='catalogo4'),

]

