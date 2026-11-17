from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SolicitacaoForm
from .models import Colaborador


@login_required
def criar_solicitacao(request):
    colaborador_solicitante = get_object_or_404(Colaborador, usuario=request.user)

    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.solicitante = colaborador_solicitante
            solicitacao.setor_solicitante = colaborador_solicitante.setor
            solicitacao.save()

            messages.success(
                request,
                f"Solicitação registrada com sucesso! Protocolo: {solicitacao.protocolo}"
            )
            return redirect('criar_solicitacao')
    else:
        form = SolicitacaoForm()

    return render(request, 'solicitacoes/solicitacao_form.html', {
        'form': form,
        'solicitante': colaborador_solicitante,
    })
