from django.urls import path
from . import views

urlpatterns = [
    path('solicitacoes/nova/', views.criar_solicitacao, name='criar_solicitacao'),
    path('solicitacoes/', views.listar_solicitacoes, name='listar_solicitacoes'),
    path('solicitacoes/<int:solicitacao_id>/atualizar-status/', views.atualizar_status, name='atualizar_status'),
    
]