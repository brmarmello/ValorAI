# ValorAI - Guia de Deploy

## Streamlit Community Cloud

1. Suba o projeto para um repositorio GitHub.
2. Acesse `https://share.streamlit.io`.
3. Clique em `New app`.
4. Selecione o repositorio e a branch.
5. Em `Main file path`, informe `src/app.py`.
6. Clique em `Deploy`.

## Secrets

Para usar LLM, adicione em `Secrets`:

```toml
OPENAI_API_KEY = "sua-chave"
```

Sem essa chave, o app continua funcionando com o motor local.

## Alternativa com Google Colab

Colab e util para demonstracao rapida ou testes, mas o deploy funcional fica melhor no Streamlit Cloud. Em Colab, voce pode instalar dependencias, clonar o repositorio e rodar o Streamlit com tunel publico, mas isso e menos estavel para entrega final.
