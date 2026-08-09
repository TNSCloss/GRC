# 02 — Risk Dashboard

Dashboard interativo de riscos (Streamlit + Plotly) para acompanhamento do registro de riscos.

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Dashboard: KPIs, heatmap 5×5, perfil por categoria e status dos controles (Anexo A) |
| `risk_register.xlsx` | Registro de riscos (ID, causa, probabilidade, impacto, tratamento, dono) |
| `requirements.txt` | Dependências do dashboard |
| `docs/dashboard.png` | Screenshot de execução real |

## Executar
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Funcionalidades
- **KPIs:** riscos mapeados, riscos altos/críticos (nível ≥ 7), riscos em tratamento e controles INEFICAZ.
- **Heatmap 5×5** do risco inerente com filtros por categoria e status.
- **Aba Compliance (Anexo A):** lê `relatorio_controles.json` gerado pelo `check_controls.py` e exibe o status por controle.

## Nota
O `relatorio_controles.json` é gerado pela pipeline de compliance-as-code (`03-compliance-as-code`). Execute `python check_controls.py` antes de abrir o dashboard para carregar a aba Compliance.
