from django.test import TestCase
from .models import Colaborador, Setor, Solicitacao


class SolicitacaoModelTest(TestCase):
    def setUp(self):
        self.setor = Setor.objects.create(nome_setor="Produção")
        self.colaborador = Colaborador.objects.create(
            nome="João Pedro Lima",
            email="joao.lima@abrafito.org.br",
            setor=self.setor,
            cargo="Operador"
        )

    def test_criacao_solicitacao_gera_protocolo(self):
        solicitacao = Solicitacao.objects.create(
            solicitante=self.colaborador,
            destinatario=self.colaborador,
            setor_solicitante=self.setor,
            setor_destinatario=self.setor,
            descricao_atividade="Teste de solicitação",
            status="pendente"
        )
        self.assertIsNotNone(solicitacao.protocolo)
        self.assertEqual(solicitacao.status, "pendente")

    def test_protocolo_segue_formato_esperado(self):
        """Verifica se o protocolo é gerado no padrão SOL-AAAA-NNNN."""
        solicitacao = Solicitacao.objects.create(
            solicitante=self.colaborador,
            destinatario=self.colaborador,
            setor_solicitante=self.setor,
            setor_destinatario=self.setor,
            descricao_atividade="Teste de formato de protocolo",
            status="pendente"
        )
        self.assertTrue(solicitacao.protocolo.startswith("SOL-"))
        partes = solicitacao.protocolo.split("-")
        self.assertEqual(len(partes), 3)
        self.assertEqual(len(partes[1]), 4)  # ano com 4 dígitos
        self.assertEqual(len(partes[2]), 4)  # sequencial com 4 dígitos

    def test_protocolos_sao_unicos_entre_solicitacoes(self):
        """Garante que duas solicitações não geram o mesmo protocolo."""
        solicitacao1 = Solicitacao.objects.create(
            solicitante=self.colaborador,
            destinatario=self.colaborador,
            setor_solicitante=self.setor,
            setor_destinatario=self.setor,
            descricao_atividade="Primeira solicitação",
            status="pendente"
        )
        solicitacao2 = Solicitacao.objects.create(
            solicitante=self.colaborador,
            destinatario=self.colaborador,
            setor_solicitante=self.setor,
            setor_destinatario=self.setor,
            descricao_atividade="Segunda solicitação",
            status="pendente"
        )
        self.assertNotEqual(solicitacao1.protocolo, solicitacao2.protocolo)
        