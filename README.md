# ValorAI

ValorAI e um agente financeiro inteligente criado para o desafio DIO "Agente Financeiro Inteligente com IA Generativa".

App em producao: https://valorai.streamlit.app

Repositorio: https://github.com/brmarmello/ValorAI

O app analisa dados mockados de transacoes, perfil do investidor, historico de atendimento e produtos financeiros para gerar orientacoes financeiras personalizadas, alertas de gastos e sugestoes de proximos passos com uma postura segura: quando nao ha dado suficiente, ele diz isso claramente.

## O que foi entregue

- Documentacao completa do agente em `docs/`
- Base de conhecimento mockada em `data/`
- Prompts e regras anti-alucinacao em `docs/03-prompts.md`
- Aplicacao funcional em Streamlit em `src/app.py`
- Motor de analise testavel em `src/valorai_core.py`
- Metricas e roteiro de pitch
- Guia de deploy em Streamlit Community Cloud

## Como executar localmente

Requisitos:

- Python 3.12
- Git

Crie um ambiente virtual:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
py -m pip install -r requirements.txt
```

Execute o app:

```powershell
py -m streamlit run src/app.py
```

Rode os testes:

```powershell
py -m pip install -r requirements-dev.txt
py -m pytest -q
```

## Uso com LLM

O ValorAI funciona sem chave de API usando respostas deterministicas baseadas nos dados locais.

Para ativar respostas com IA generativa, configure a variavel de ambiente:

```powershell
$env:OPENAI_API_KEY="sua-chave"
```

O app continua usando os dados locais como contexto e aplica regras de seguranca para evitar respostas fora da base de conhecimento.

## Deploy

Deploy publico atual:

- URL: https://valorai.streamlit.app
- Plataforma: Streamlit Community Cloud
- Branch: `main`
- Arquivo principal: `src/app.py`
- Python: `3.12`

Para redeploy:

1. Publique este repositorio no GitHub.
2. Acesse `https://share.streamlit.io`.
3. Escolha o repositorio.
4. Defina o arquivo principal como `src/app.py`.
5. Em `Advanced settings`, selecione Python `3.12`.
6. Em secrets, opcionalmente adicione `OPENAI_API_KEY`.
7. Clique em deploy.

Observacao: no Streamlit Community Cloud, a versao do Python deve ser escolhida na interface de deploy. Arquivos como `runtime.txt` nao controlam essa configuracao na plataforma.

## Validacao

Ultima rodada executada:

- App em producao: `HTTP 200 OK`
- GitHub publico: `HTTP 200 OK`
- Testes locais: `4 passed`
- Dependencias principais importadas com sucesso

## Aviso

ValorAI e um prototipo educacional. Ele nao substitui consultoria financeira, juridica, contabil ou de investimentos.
