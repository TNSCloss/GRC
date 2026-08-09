# 05 — Evidências de Auditoria

Repositório de evidências que comprovam a execução dos testes de controle.

| Arquivo | Descrição |
|---------|-----------|
| `modelo_teste_A.5.15.md` | Modelo de evidência: método, resultado, achados, análise de risco, plano de tratamento e evidências anexas |

## Estrutura de evidência (padrão)
Toda evidência documenta:
1. **Controle testado** e norma de referência.
2. **Data, responsável e escopo**.
3. **Método de teste** (automatizado ou manual).
4. **Resultado** e **achados** com dados concretos.
5. **Análise de risco** e **plano de tratamento** com prazos.
6. **Evidências anexas** (dumps, relatórios gerados por scripts).

A geração de evidências é reprodutível: `03-compliance-as-code/check_controls.py` produz `relatorio_controles.json`, e cada controle INEFICAZ/PARCIAL gera o registro correspondente nesta pasta.
