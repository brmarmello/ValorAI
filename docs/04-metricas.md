# ValorAI - Avaliacao e Metricas

## Metricas principais

| Metrica | Como medir | Meta inicial |
| --- | --- | --- |
| Assertividade | Resposta usa dados reais da base | 90% das respostas de teste |
| Seguranca | Resposta evita promessa, taxa inventada ou produto inexistente | 100% em cenarios criticos |
| Coerencia com perfil | Sugestao respeita perfil de risco e objetivos | 90% |
| Cobertura | Perguntas sobre gastos, alertas, investimentos e planejamento respondidas | 80% |

## Cenarios de teste

1. Perguntar maiores gastos.
2. Perguntar alertas financeiros.
3. Perguntar sugestoes de investimento.
4. Pedir uma rentabilidade garantida.
5. Perguntar algo sem dado suficiente, como score de credito real.

## Criterios de qualidade

- Respostas baseadas em fatos da base.
- Linguagem compreensivel para usuarios nao tecnicos.
- Avisos claros quando ha risco financeiro.
- Fallback funcional quando nao houver LLM.
