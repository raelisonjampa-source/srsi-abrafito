from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SolicitacaoForm
from .models import Colaborador, Solicitacao, HistoricoStatus


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


@login_required
def listar_solicitacoes(request):
    colaborador = get_object_or_404(Colaborador, usuario=request.user)

    status_filtro = request.GET.get('status', '')

    solicitacoes = Solicitacao.objects.filter(
        solicitante=colaborador
    ) | Solicitacao.objects.filter(
        destinatario=colaborador
    )

    if status_filtro:
        solicitacoes = solicitacoes.filter(status=status_filtro)

    solicitacoes = solicitacoes.order_by('-data_hora_criacao')

    return render(request, 'solicitacoes/solicitacao_lista.html', {
        'solicitacoes': solicitacoes,
        'status_filtro': status_filtro,
    })


TRANSICOES_VALIDAS = {
    'pendente': 'em_andamento',
    'em_andamento': 'concluido',
}


@login_required
def atualizar_status(request, solicitacao_id):
    colaborador = get_object_or_404(Colaborador, usuario=request.user)
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if solicitacao.destinatario_id != colaborador.id:
        messages.error(request, "Você não tem permissão para alterar esta solicitação.")
        return redirect('listar_solicitacoes')

    status_atual = solicitacao.status
    novo_status = TRANSICOES_VALIDAS.get(status_atual)

    if not novo_status:
        messages.error(request, "Esta solicitação já está concluída.")
        return redirect('listar_solicitacoes')

    HistoricoStatus.objects.create(
        solicitacao=solicitacao,
        status_anterior=status_atual,
        status_novo=novo_status,
        colaborador_responsavel=colaborador,
    )

    solicitacao.status = novo_status
    solicitacao.save()

    messages.success(request, f"Status atualizado para '{novo_status}'.")
    return redirect('listar_solicitacoes')
