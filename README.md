SRSI — Sistema de Registro de Solicitações Internas
Projeto desenvolvido para a ABRAFITO (Associação Brasileira de Fitoterapia) como parte de um MVP de Análise e Desenvolvimento de Sistemas.

Problema
As solicitações entre setores (produção, financeiro, atendimento ao associado, administrativo) são feitas de forma fragmentada — por fala, WhatsApp ou planilhas — sem protocolo, sem status padronizado e sem rastreabilidade. Isso gera perda de registros e atrasos na produção.

Solução (MVP)
Sistema web que permite:

Registrar uma solicitação com protocolo único gerado automaticamente (SOL-AAAA-NNNN).
Definir setor de origem/destino e colaborador destinatário.
Acompanhar o status (Pendente → Em andamento → Concluído).
Manter histórico imutável de cada mudança de status (quem alterou, quando, de qual status para qual).
Stack Técnica
Backend: Django 5.0 (Python)
Banco de dados: SQLite (ambiente de desenvolvimento/piloto)
Frontend: Templates Django + Bootstrap 5.3
Servidor de produção: Gunicorn
Estrutura do Projeto


srsi-abrafito/
├── srsi/                  # configurações do projeto Django
├── solicitacoes/          # app principal (models, views, admin)
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
Modelo de Dados
Setor — setores da associação (Produção, Financeiro, Atendimento ao Associado, Administrativo).
Colaborador — vinculado a um setor.
Solicitacao — protocolo, solicitante, destinatário, setor de origem/destino, descrição, status.
HistoricoStatus — log imutável de cada transição de status.
Como Executar Localmente
bash


# Clonar o repositório
git clone https://github.com/raelisonjampa-source/srsi-abrafito.git
cd srsi-abrafito

# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (acesso ao admin)
python manage.py createsuperuser

# Rodar o servidor
python manage.py runserver
Acesse http://127.0.0.1:8000/admin/ para gerenciar setores, colaboradores e solicitações.

Status do Projeto
🔄 MVP em fase de validação em campo (piloto com colaboradores da ABRAFITO).

Escopo Atual (RF implementados)
 RF01 — Criar solicitação com protocolo automático
 RF02 — Listar/consultar solicitações
 RF03 — Atualizar status
 RF04 — Histórico de alterações
 RF05 — Painel do gestor (desejável, pós-piloto)
Licença
Projeto acadêmico/institucional desenvolvido para fins de estudo em Análise e Desenvolvimento de Sistemas, em parceria com a ABRAFITO.
