from django.contrib import admin
from .models import Setor, Colaborador, Solicitacao, HistoricoStatus

admin.site.register(Setor)
admin.site.register(Colaborador)
admin.site.register(Solicitacao)
admin.site.register(HistoricoStatus)
