from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_gastos, name='lista_gastos'),
    path('excluir/<int:id>/', views.excluir_gasto, name='excluir_gasto'),
    path('editar/<int:id>/', views.editar_gasto, name='editar_gasto'),
]