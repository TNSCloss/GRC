# 03 — Compliance as Code

Automatização da verificação de controles do Anexo A (ISO/IEC 27001:2022) a partir de evidências versionadas. O CI falha quando um controle está **INEFICAZ**.

| Arquivo | Descrição |
|---------|-----------|
| `check_controls.py` | Verifica A.5.15 (contas órfãs), A.5.17 (MFA), A.8.10 (retenção) e A.8.13 (backup/restore). Emite JSON e retorna exit code ≠ 0 se houver INEFICAZ |
| `usuarios.csv` | Base de usuários: status (ativo/inativo) e MFA |
| `contas_ativas.json` | Contas do AD, com inativas > 90 dias sem dono (A.5.15) |
| `backup.json` | Último backup e último teste de restore (A.8.13) |
| `politicas.json` | Prazo definido × retenção real por política (A.8.10) |
| `relatorio_controles.json` | Saída gerada (versionada para rastreabilidade) |
| `requirements.txt` | Dependências (pandas) |

## Executar localmente
```bash
pip install -r requirements.txt
python check_controls.py            # imprime JSON na tela
python check_controls.py --json relatorio_controles.json
echo $?                             # 1 se algum controle INEFICAZ
```

## Pipeline (`.github/workflows/ci.yml`)
- Executa em todo `push`/`pull_request` para `main` e **toda segunda-feira 06:00** (cron).
- Instala dependências, roda `check_controls.py` e publica o relatório como artefato.
- O job **falha** se qualquer controle estiver INEFICAZ — tratando a segurança como código (deploy gate).

## Exemplo de saída
```json
{
  "gerado_em": "2026-08-08T23:23:24",
  "resumo": {"total": 4, "eficaz": 0, "parcial": 2, "ineficaz": 2},
  "controles": [
    {"id": "A.5.17", "nome": "Autenticação Multifator", "status": "PARCIAL", "detalhes": "94.1% de 17 usuários ativos com MFA (1 sem MFA)"}
  ]
}
```
