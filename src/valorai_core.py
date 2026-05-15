from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@dataclass(frozen=True)
class KnowledgeBase:
    transactions: list[dict[str, Any]]
    service_history: list[dict[str, Any]]
    investor_profile: dict[str, Any]
    products: list[dict[str, Any]]


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        if "valor" in row:
            row["valor"] = float(row["valor"])
    return rows


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_knowledge_base(data_dir: Path | str = DATA_DIR) -> KnowledgeBase:
    base = Path(data_dir)
    return KnowledgeBase(
        transactions=_read_csv(base / "transacoes.csv"),
        service_history=_read_csv(base / "historico_atendimento.csv"),
        investor_profile=_read_json(base / "perfil_investidor.json"),
        products=_read_json(base / "produtos_financeiros.json"),
    )


def summarize_cashflow(transactions: list[dict[str, Any]]) -> dict[str, Any]:
    income = sum(item["valor"] for item in transactions if item["tipo"] == "entrada")
    expenses = sum(item["valor"] for item in transactions if item["tipo"] == "saida")
    invested = sum(
        item["valor"]
        for item in transactions
        if item["tipo"] == "saida" and item["categoria"] == "Investimentos"
    )
    by_category: dict[str, float] = defaultdict(float)
    for item in transactions:
        if item["tipo"] == "saida":
            by_category[item["categoria"]] += item["valor"]

    savings_rate = (invested / income) if income else 0
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "invested": round(invested, 2),
        "savings_rate": round(savings_rate, 4),
        "by_category": dict(sorted(by_category.items(), key=lambda item: item[1], reverse=True)),
    }


def detect_alerts(summary: dict[str, Any]) -> list[str]:
    alerts: list[str] = []
    income = summary["income"]
    categories = summary["by_category"]

    if summary["balance"] < 0:
        alerts.append("O mes fechou negativo; priorize revisar despesas variaveis antes de assumir novos compromissos.")
    if income and categories.get("Lazer", 0) / income > 0.06:
        alerts.append("Gastos com lazer passaram de 6% da renda do periodo; vale definir um teto semanal.")
    if income and categories.get("Dividas", 0) / income > 0.1:
        alerts.append("Pagamentos ligados a dividas passaram de 10% da renda; acompanhe juros e vencimentos.")
    if summary["savings_rate"] < 0.15:
        alerts.append("A taxa de investimento ficou abaixo de 15%; aumentar aportes pode acelerar a reserva.")
    if not alerts:
        alerts.append("Nao encontrei alertas criticos nos dados mockados deste periodo.")

    return alerts


def recommend_products(kb: KnowledgeBase) -> list[dict[str, str]]:
    profile = kb.investor_profile
    goals = " ".join(profile.get("objetivos", [])).lower()
    risk = profile.get("perfil_risco", "").lower()
    recommendations: list[dict[str, str]] = []

    for product in kb.products:
        suitability = " ".join(product.get("adequado_para", [])).lower()
        product_risk = product.get("risco", "").lower()
        matches_goal = any(token in suitability for token in ["reserva", "imovel", "planejamento"])
        matches_profile = product_risk in {"baixo", risk}

        if matches_profile and (matches_goal or any(goal in suitability for goal in goals.split())):
            recommendations.append(
                {
                    "nome": product["nome"],
                    "motivo": f"Combina com perfil {risk} e com objetivos informados: {', '.join(profile.get('objetivos', []))}.",
                    "cuidado": "Validar taxas, prazos, garantias e adequacao antes de contratar.",
                }
            )

    return recommendations[:3]


def build_context(kb: KnowledgeBase) -> str:
    summary = summarize_cashflow(kb.transactions)
    alerts = detect_alerts(summary)
    products = recommend_products(kb)
    return "\n".join(
        [
            f"Renda: R$ {summary['income']:.2f}",
            f"Despesas: R$ {summary['expenses']:.2f}",
            f"Saldo: R$ {summary['balance']:.2f}",
            f"Investido: R$ {summary['invested']:.2f}",
            f"Taxa de investimento: {summary['savings_rate']:.1%}",
            f"Maiores categorias: {summary['by_category']}",
            f"Alertas: {alerts}",
            f"Perfil: {kb.investor_profile}",
            f"Produtos sugeridos: {products}",
        ]
    )


def answer_without_llm(question: str, kb: KnowledgeBase) -> str:
    normalized = question.lower()
    summary = summarize_cashflow(kb.transactions)
    alerts = detect_alerts(summary)
    products = recommend_products(kb)

    if any(term in normalized for term in ["gasto", "despesa", "categoria"]):
        top_categories = list(summary["by_category"].items())[:3]
        lines = [f"- {name}: R$ {value:.2f}" for name, value in top_categories]
        return "Suas maiores categorias de despesa no periodo foram:\n" + "\n".join(lines)

    if any(term in normalized for term in ["alerta", "risco", "problema"]):
        return "Principais alertas encontrados:\n" + "\n".join(f"- {item}" for item in alerts)

    if any(term in normalized for term in ["invest", "produto", "aplicar", "reserva"]):
        lines = [f"- {item['nome']}: {item['motivo']}" for item in products]
        return (
            "Com os dados mockados, eu priorizaria opcoes de baixo a moderado risco:\n"
            + "\n".join(lines)
            + "\n\nIsto nao e recomendacao individual de investimento; valide custos, prazos e riscos."
        )

    return (
        "Com base nos dados disponiveis, o mes teve "
        f"renda de R$ {summary['income']:.2f}, despesas de R$ {summary['expenses']:.2f} "
        f"e saldo de R$ {summary['balance']:.2f}. "
        "Posso detalhar gastos, alertas ou alternativas de planejamento."
    )
