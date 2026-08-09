# 01 — Control Testing

Matriz de 20 controles do Anexo A (ISO/IEC 27001:2022) com o resultado do teste de cada controle.

| Arquivo | Descrição |
|---------|-----------|
| `control_matrix_20_controles.xlsx` | 20 controles testados: ID, descrição, frequência, dono, como testar, evidência, resultado, status, plano e prazo |

## Status consolidado (fictício)
- **A.5.15** Controle de acesso — contas órfãs → **Ineficaz** (7 contas; plano: offboarding automatizado em 30 dias)
- **A.5.17** Autenticação multifator → **Parcial** (94% de cobertura)
- **A.8.10** Exclusão de informações → **Ineficaz** (retenção de CVs acima do prazo)
- **A.8.13** Backup e teste de restore → **Parcial** (8 meses sem teste de restore)

Consistência garantida pelo compliance-as-code: `03-compliance-as-code/check_controls.py` reproduz estes mesmos status a partir das evidências.
