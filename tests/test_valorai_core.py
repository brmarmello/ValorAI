from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from valorai_core import (  # noqa: E402
    answer_without_llm,
    detect_alerts,
    load_knowledge_base,
    recommend_products,
    summarize_cashflow,
)


def test_cashflow_summary_has_expected_totals():
    kb = load_knowledge_base()
    summary = summarize_cashflow(kb.transactions)

    assert summary["income"] == 8046.2
    assert summary["expenses"] == 7294.85
    assert summary["balance"] == 751.35
    assert summary["invested"] == 1200.0


def test_alerts_and_recommendations_are_generated():
    kb = load_knowledge_base()
    summary = summarize_cashflow(kb.transactions)

    assert detect_alerts(summary)
    assert recommend_products(kb)


def test_local_answer_uses_available_context():
    kb = load_knowledge_base()
    answer = answer_without_llm("Quais sao meus maiores gastos?", kb)

    assert "maiores categorias" in answer.lower()
    assert "Moradia" in answer
