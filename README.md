# ValorAI

ValorAI e um agente financeiro inteligente criado para o desafio DIO "Agente Financeiro Inteligente com IA Generativa".

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
streamlit run src/app.py
```

## Uso com LLM

O ValorAI funciona sem chave de API usando respostas deterministicas baseadas nos dados locais.

Para ativar respostas com IA generativa, configure a variavel de ambiente:

```powershell
$env:OPENAI_API_KEY="sua-chave"
```

O app continua usando os dados locais como contexto e aplica regras de seguranca para evitar respostas fora da base de conhecimento.

## Deploy

O caminho mais simples e usar Streamlit Community Cloud:

1. Publique este repositorio no GitHub.
2. Acesse `https://share.streamlit.io`.
3. Escolha o repositorio.
4. Defina o arquivo principal como `src/app.py`.
5. Em secrets, opcionalmente adicione `OPENAI_API_KEY`.
6. Clique em deploy.

## Aviso

ValorAI e um prototipo educacional. Ele nao substitui consultoria financeira, juridica, contabil ou de investimentos.
