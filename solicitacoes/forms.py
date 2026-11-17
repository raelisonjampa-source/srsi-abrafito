from django import forms
from .models import Solicitacao, Colaborador


class SolicitacaoForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(
        queryset=Colaborador.objects.all(),
        label="Destinatário",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Solicitacao
        fields = ['destinatario', 'setor_destinatario', 'descricao_atividade']
        widgets = {
            'setor_destinatario': forms.Select(attrs={'class': 'form-select'}),
            'descricao_atividade': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva a atividade solicitada...'
            }),
        }
        labels = {
            'setor_destinatario': 'Setor de destino',
            'descricao_atividade': 'Descrição da atividade',
        }