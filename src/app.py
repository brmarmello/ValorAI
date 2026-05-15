from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))

from valorai_core import (  # noqa: E402
    answer_without_llm,
    build_context,
    detect_alerts,
    load_knowledge_base,
    recommend_products,
    summarize_cashflow,
)


APP_TITLE = "ValorAI"
SYSTEM_PROMPT = """
Voce e o ValorAI, um agente financeiro educacional, consultivo e seguro.
Use apenas o contexto fornecido. Nao invente saldos, produtos, taxas ou eventos.
Quando faltarem dados, diga quais dados seriam necessarios.
Nao prometa rentabilidade e nao substitua consultoria financeira profissional.
Responda em portugues brasileiro, com tom claro, acolhedor e objetivo.
"""


def ask_openai(question: str, context: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Contexto verificado:\n{context}\n\nPergunta do cliente:\n{question}",
                },
            ],
            temperature=0.2,
        )
        return response.output_text
    except Exception as exc:
        return f"Nao consegui acionar o LLM agora. Vou responder pelo motor local.\n\nDetalhe tecnico: {exc}"


def currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.set_page_config(page_title=APP_TITLE, page_icon="VA", layout="wide")

kb = load_knowledge_base()
summary = summarize_cashflow(kb.transactions)
alerts = detect_alerts(summary)
products = recommend_products(kb)

st.title("ValorAI")
st.caption("Agente financeiro inteligente com IA generativa, base de conhecimento local e respostas seguras.")

with st.sidebar:
    st.header("Base do agente")
    st.write("Dados mockados carregados:")
    st.write("- transacoes.csv")
    st.write("- historico_atendimento.csv")
    st.write("- perfil_investidor.json")
    st.write("- produtos_financeiros.json")
    st.divider()
    st.metric("Perfil", kb.investor_profile["perfil_risco"].title())
    st.metric("Horizonte", kb.investor_profile["horizonte"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Renda", currency(summary["income"]))
col2.metric("Despesas", currency(summary["expenses"]))
col3.metric("Saldo", currency(summary["balance"]))
col4.metric("Investido", currency(summary["invested"]), f"{summary['savings_rate']:.1%} da renda")

tab_chat, tab_analise, tab_produtos, tab_dados = st.tabs(
    ["Chat ValorAI", "Analise financeira", "Sugestoes", "Base de conhecimento"]
)

with tab_chat:
    st.subheader("Converse com o ValorAI")
    question = st.chat_input("Pergunte sobre gastos, alertas, reserva ou planejamento")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Ola! Sou o ValorAI. Posso analisar seus dados mockados e sugerir proximos passos com seguranca.",
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        context = build_context(kb)
        llm_answer = ask_openai(question, context)
        fallback_answer = answer_without_llm(question, kb)
        answer = llm_answer if llm_answer and "Vou responder pelo motor local" not in llm_answer else fallback_answer

        if llm_answer and "Vou responder pelo motor local" in llm_answer:
            st.info(llm_answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

with tab_analise:
    st.subheader("Resumo do periodo")
    category_df = pd.DataFrame(
        [{"categoria": key, "valor": value} for key, value in summary["by_category"].items()]
    )
    fig = px.bar(
        category_df,
        x="categoria",
        y="valor",
        color="categoria",
        title="Despesas por categoria",
        labels={"valor": "Valor (R$)", "categoria": "Categoria"},
    )
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Alertas")
    for alert in alerts:
        st.warning(alert)

with tab_produtos:
    st.subheader("Sugestoes coerentes com o perfil")
    for item in products:
        with st.container(border=True):
            st.markdown(f"### {item['nome']}")
            st.write(item["motivo"])
            st.caption(item["cuidado"])

with tab_dados:
    st.subheader("Transacoes")
    st.dataframe(pd.DataFrame(kb.transactions), use_container_width=True)
    st.subheader("Historico de atendimento")
    st.dataframe(pd.DataFrame(kb.service_history), use_container_width=True)
    st.subheader("Perfil do investidor")
    st.json(kb.investor_profile)
