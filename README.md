# Semana 12 — Estrutura completa da aplicação (Aula 080)

Continuação da [Semana 11.B](https://github.com/ptaissa-ai/semana_11B_Flasky), mantendo: cadastro de usuários, funções (`Role`), SQLite/SQLAlchemy, histórico `/emailsEnviados` e SendGrid Web API. A principal evolução é a organização da aplicação em **pacotes e módulos**, conforme os slides da Aula 080.

## Correspondência com a Aula 080

| Requisito da aula | Implementação |
|---|---|
| `config.py` e configuração por ambiente | Classes `Config`, `DevelopmentConfig`, `TestingConfig`, `ProductionConfig` |
| `app/__init__.py` e factory `create_app()` | Registro de extensões e blueprint |
| `app/models.py` | `Role`, `User` e `EmailEnviado` |
| `app/email.py` | Requisição HTTPS à API SendGrid |
| `app/main/__init__.py` | Blueprint `main` |
| `app/main/views.py` | Rotas `/` e `/emailsEnviados` |
| `app/main/forms.py` | `NameForm` com Flask-WTF |
| `app/main/errors.py` | Tratadores 404 e 500 |
| `flasky.py` | Entrada da aplicação e comando `flask test` |
| `tests/test_basics.py` | Testes, inclusive cadastro e destinatários |
| `migrations/` | Gerar com `flask db init` (ver abaixo) |
| `venv/` | Gerar localmente; não versionar |

## Dados acadêmicos utilizados (preservados da Semana 11.B)

- Aluna: **Taissa Pieri**
- Prontuário: **PT3038084**
- E-mail institucional: **p.taissa@aluno.ifsp.edu.br**
- Destinatário do professor: **flaskaulasweb@zohomail.com**

Cada novo usuário causa tentativa obrigatória de notificação a **ambos** os destinatários. O cadastro só é persistido após aceitação da requisição pela API; aceitação não equivale a entrega efetiva. Em falha, a transação é revertida. Em cenários de rede com confirmação perdida, nova tentativa pode duplicar e-mails: produção exigiria fila e idempotência.

## Executar localmente

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Windows: copy .env.example .env
# Edite .env com chave SendGrid e remetente verificado.
export FLASK_APP=flasky.py # Windows CMD: set FLASK_APP=flasky.py
export FLASK_CONFIG=development
flask db init
flask db migrate -m "Estrutura inicial"
flask db upgrade
flask seed-roles
flask test
flask run
```

> `flask db init` gera o diretório `migrations/` conforme a Aula 080. O projeto inclui as classes, extensões e modelos necessários; o diretório não vem preenchido para não simular uma migração que ainda não foi criada. Execute os comandos e versione o diretório gerado no GitHub. Não versione `venv`, `.env` ou o banco de dados.

## Continuar usando um banco da Semana 11.B

A estrutura das tabelas foi preservada e o banco anterior se encontra em `instance/app.db`. Faça **backup** antes de copiar. Se já existir um banco com as tabelas da Semana 11, não execute uma migração inicial como se fosse banco vazio. Para um esquema comprovadamente idêntico ao dos modelos, gere a revisão inicial com `flask db migrate`, faça revisão do arquivo gerado e use `flask db stamp head` para marcar a revisão sem executar DDL. Depois execute `flask seed-roles`. Para instalações novas, use `flask db upgrade`. Nunca faça stamp sem conferir o esquema.

## PythonAnywhere

1. Crie um repositório novo, por exemplo `semana_12_Flasky`, e envie os arquivos.
2. No console Bash do PythonAnywhere, use `git clone`, crie/ative `venv` e rode `pip install -r requirements.txt`.
3. Configure `.env` **privado** no diretório do projeto com chave SendGrid e remetente verificado. Na conta gratuita, valide o acesso HTTP à API.
4. Execute `flask db upgrade` e `flask seed-roles` no console (crie a revisão inicial antes, se ainda não existir).
5. Na aba **Web**, configure a versão Python, o caminho do virtualenv e o arquivo WSGI. Use `wsgi_pythonanywhere.py` como exemplo, trocando `SEU_USUARIO` e ajustando os caminhos.
6. Clique em **Reload** e teste cadastro e `/emailsEnviados`.

**Importante:** a conta SendGrid deve ter remetente/domínio verificado. Nunca publique `API_KEY` ou `SECRET_KEY` no GitHub. O modelo registra resposta de aceitação (HTTP 202) da API, não uma confirmação de entrega final.

## Testes

`flask test` executa 6 testes: existência da aplicação, ambiente de testes, página inicial, notificação aos dois destinatários, cadastro duplicado e falha de envio. O serviço externo é simulado por mock: não envia e-mails reais durante os testes.
