from django.conf import settings
from django.db import models
from django.utils import timezone


class Setor(models.Model):
    nome_setor = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome_setor']

    def __str__(self):
        return self.nome_setor


class Colaborador(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='colaborador',
        null=True,
        blank=True,
        help_text='Vínculo com o usuário de login do Django.'
    )
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='colaboradores')

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Solicitacao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluido'),
    ]

    protocolo = models.CharField(max_length=20, unique=True, editable=False)
    solicitante = models.ForeignKey(Colaborador, on_delete=models.PROTECT, related_name='solicitacoes_feitas')
    destinatario = models.ForeignKey(Colaborador, on_delete=models.PROTECT, related_name='solicitacoes_recebidas')
    setor_solicitante = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='solicitacoes_origem')
    setor_destinatario = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='solicitacoes_destino')
    descricao_atividade = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_hora_criacao = models.DateTimeField(auto_now_add=True)
    data_hora_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_hora_criacao']

    def save(self, *args, **kwargs):
        if not self.protocolo:
            ano = timezone.now().year
            ultimo = Solicitacao.objects.filter(
                protocolo__startswith=f"SOL-{ano}"
            ).count() + 1
            self.protocolo = f"SOL-{ano}-{ultimo:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.protocolo


class HistoricoStatus(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='historico')
    status_anterior = models.CharField(max_length=20)
    status_novo = models.CharField(max_length=20)
    data_hora_alteracao = models.DateTimeField(auto_now_add=True)
    colaborador_responsavel = models.ForeignKey(Colaborador, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-data_hora_alteracao']

    def __str__(self):
        return f"{self.solicitacao.protocolo}: {self.status_anterior} -> {self.status_novo}"