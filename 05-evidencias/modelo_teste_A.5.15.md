# Evidência de Teste — Controle A.5.15 (ISO/IEC 27001:2022)

Controle de acesso — revisão de contas e privilégios de acesso (contas órfãs).

- **Data do teste:** 2026-08-08
- **Responsável:** Equipe de Segurança da Informação (TI)
- **Escopo:** Active Directory da Vilhena Fintech S.A. (fictício)
- **Método:** Extração automatizada de contas com `lastLogon` > 90 dias cruzada com base de funcionários/contratos ativos do RH; validação manual do dono.

## Resultado
| Métrica | Valor |
|---------|-------|
| Total de contas no AD | 120 |
| Contas inativas > 90 dias | 7 |
| Contas sem dono identificado | 5 |
| Status | **INEFICAZ** |

## Achados
| Conta | Último login | Dono |
|-------|--------------|------|
| `svc_pagamento_legado` | 2025-11-02 | desconhecido |
| `roberta.queiroz` | 2025-12-20 | sem supervisor |
| `backup_srv_antigo` | 2026-01-05 | desconhecido |
| `admin_teste` | 2025-10-15 | desconhecido |
| `ex.gerente01` | 2025-08-01 | desconhecido |
| `svc_relatorio` | 2025-11-28 | desconhecido |
| `joana.prado` | 2025-12-01 | sem supervisor |

## Análise de risco
Contas órfãs representam vetor de acesso não autorizado (uso indevido de credencial de ex-funcionário ou serviço legado). Risco inerente elevado (Prob 4 × Impacto 4 = nível 8 no risk register — "Acesso ex-funcionário").

## Plano de tratamento
1. Desativar as 7 contas em até **48h** (ação corretiva imediata).
2. Automatizar desativação no offboarding via integração **RH → AD** em até **30 dias**.
3. Estabelecer job mensal de detecção de contas inativas com alerta automático.
4. Re-teste em **90 dias** e acompanhamento da remediação no relatório de compliance-as-code (`check_controls.py`).

## Evidências anexas
- `contas_ativas.json` (03-compliance-as-code) — dump utilizado no teste.
- Relatório `relatorio_controles.json` — resultado A.5.15 = INEFICAZ, exit code 1 no CI.
