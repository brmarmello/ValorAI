# ValorAI - Base de Conhecimento

## Fontes usadas

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `data/transacoes.csv` | CSV | Calculo de renda, despesas, saldo, categorias e taxa de investimento |
| `data/historico_atendimento.csv` | CSV | Contexto de necessidades anteriores do cliente |
| `data/perfil_investidor.json` | JSON | Perfil de risco, objetivos, horizonte e preferencias |
| `data/produtos_financeiros.json` | JSON | Catalogo mockado de produtos e servicos |

## Estrategia

A base foi desenhada para ser pequena, auditavel e segura. O agente nao consulta dados bancarios reais. Isso permite testar o comportamento sem expor informacoes sensiveis.

## Transformacoes

- Valores monetarios sao convertidos para `float`.
- Transacoes de entrada compoem renda.
- Transacoes de saida compoem despesas.
- A categoria `Investimentos` calcula a taxa de investimento.
- Produtos sao filtrados por perfil de risco e objetivos declarados.

## Expansoes futuras

- Adicionar importacao de extratos OFX/CSV.
- Criar classificacao automatica de categorias.
- Adicionar memoria de metas por usuario.
- Integrar banco vetorial para busca semantica quando a base crescer.
