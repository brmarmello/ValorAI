# ValorAI - Guia de Deploy

## Streamlit Community Cloud

1. Suba o projeto para um repositorio GitHub.
2. Acesse `https://share.streamlit.io`.
3. Clique em `New app`.
4. Selecione o repositorio e a branch.
5. Em `Main file path`, informe `src/app.py`.
6. Em `Advanced settings`, selecione Python `3.12`.
7. Clique em `Deploy`.

## Versao do Python

Use Python `3.12`, a mesma versao usada nos testes locais do projeto.

O Streamlit Community Cloud nao usa `runtime.txt` para definir a versao do Python. A versao deve ser escolhida na interface, em `Advanced settings`, durante o deploy ou em um redeploy.

## Secrets

Para usar LLM, adicione em `Secrets`:

```toml
OPENAI_API_KEY = "sua-chave"
```

Sem essa chave, o app continua funcionando com o motor local.

## Alternativa com Google Colab

Colab e util para demonstracao rapida ou testes, mas o deploy funcional fica melhor no Streamlit Cloud. Em Colab, voce pode instalar dependencias, clonar o repositorio e rodar o Streamlit com tunel publico, mas isso e menos estavel para entrega final.
