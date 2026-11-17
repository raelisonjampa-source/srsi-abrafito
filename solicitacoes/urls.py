from django.urls import path
from . import views

urlpatterns = [
    path('solicitacoes/nova/', views.criar_solicitacao, name='criar_solicitacao'),
    # path('solicitacoes/', views.listar_solicitacoes, name='listar_solicitacoes'),  # RF02
]

