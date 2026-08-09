# 04 — TPRM (Gestão de Riscos de Terceiros)

Avaliação de riscos de fornecedores e parceiros antes e durante o relacionamento.

| Arquivo | Descrição |
|---------|-----------|
| `questionario_tprm.md` | Questionário com 15 perguntas, pesos por domínio, scoring 0–100 e tiers de risco |

## Como usar
1. Enviar o questionário ao fornecedor com solicitação de evidências.
2. Pontuar (Sim = 1, Parcial = 0,5, Não/N/A = 0).
3. Calcular o score ponderado: Segurança 40% · Privacidade 25% · Continuidade 15% · Contratos/Compliance 20%.
4. Classificar no tier (Baixo / Médio / Alto / Crítico) e definir a ação exigida.
5. Reavaliar conforme a periodicidade do tier (anual / semestral / 90 dias / plano de saída).

## Integração com o programa GRC
- Tiers de risco alimentam o `risk_register.xlsx` (categoria Terceiros) e o heatmap do dashboard.
- Cláusulas de segurança, DPA e direito de auditoria são pré-requisitos para qualquer contratação.
