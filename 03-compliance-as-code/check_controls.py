#!/usr/bin/env python3
"""GRC Compliance-as-Code — Verificação automatizada de controles ISO 27001:2022.

Lê evidências (CSV/JSON) e emite um relatório estruturado em JSON com o status
de cada controle. Retorna exit code != 0 quando algum controle está INEFICAZ,
para falhar a pipeline de CI (compliance-as-code).

Uso:
    python3 check_controls.py [--json relatorio.json] [--base-dir DIR]
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd

CURRENT = datetime.now()


@dataclass
class Controle:
    id: str
    nome: str
    status: str  # EFICAZ | PARCIAL | INEFICAZ
    evidencia: str
    detalhes: str = ""
    recomendacao: str = ""


def check_mfa(users_path: Path) -> Controle:
    """A.5.17 — Autenticação multifator."""
    df = pd.read_csv(users_path)
    ativos = df[df["status"] == "ativo"]
    com_mfa = ativos[ativos["mfa_ativo"] == True]  # noqa: E712
    sem_mfa = ativos[~ativos["mfa_ativo"]]
    cobertura = round(100 * len(com_mfa) / len(ativos), 1) if len(ativos) else 0.0
    alvo = 0.95  # meta definida no programa GRC (94% atual = Parcial)
    if cobertura >= alvo * 100:
        status, rec = "EFICAZ", "Manter cobertura e revisar contas de serviço trimestralmente."
    elif cobertura >= 0.70:
        status, rec = "PARCIAL", f"Faltam {len(sem_mfa)} usuário(s) sem MFA: migrar contas de serviço."
    else:
        status, rec = "INEFICAZ", "Implementar MFA obrigatório em toda a base ativa."
    return Controle(
        id="A.5.17",
        nome="Autenticação Multifator",
        status=status,
        evidencia="usuarios.csv",
        detalhes=f"{cobertura}% de {len(ativos)} usuários ativos com MFA ({len(sem_mfa)} sem MFA)",
        recomendacao=rec,
    )


def check_backup(backup_path: Path) -> Controle:
    """A.8.13 — Backups de informações e testes de restore."""
    data = json.loads(backup_path.read_text())
    hoje = CURRENT
    restore = datetime.fromisoformat(data["ultimo_teste_restore"])
    dias = (hoje - restore).days
    if dias <= 90:
        status, rec = "EFICAZ", "Teste de restore dentro do prazo de 90 dias."
    elif dias <= 365:
        status, rec = "PARCIAL", "Agendar teste de restore do ambiente ERP (prioridade)."
    else:
        status, rec = "INEFICAZ", "Executar teste de restore imediatamente e reavaliar SLA."
    return Controle(
        id="A.8.13",
        nome="Backup e Teste de Restore",
        status=status,
        evidencia="backup.json",
        detalhes=f"Último teste de restore: {restore.date()} ({dias} dias) · último backup: {data['ultimo_backup']}",
        recomendacao=rec,
    )


def check_retencao(policies_path: Path) -> Controle:
    """A.8.10 — Exclusão de informações (retenção vs. prazo definido)."""
    violacoes = []
    for pol in json.loads(policies_path.read_text()):
        if pol["retencao_real_dias"] > pol["prazo_definido_dias"]:
            violacoes.append(pol["politica"])
    if not violacoes:
        return Controle(
            id="A.8.10",
            nome="Retenção e Exclusão de Dados",
            status="EFICAZ",
            evidencia="politicas.json",
            detalhes="Todas as políticas dentro do prazo definido",
            recomendacao="Manter job de purga programado.",
        )
    return Controle(
        id="A.8.10",
        nome="Retenção e Exclusão de Dados",
        status="INEFICAZ",
        evidencia="politicas.json",
        detalhes=f"Prazos excedidos: {', '.join(violacoes)}",
        recomendacao="Purgar dados excedentes e automatizar job de descarte.",
    )


def check_contas_orfas(accounts_path: Path) -> Controle:
    """A.5.15 — Controle de acesso (contas inativas sem dono identificado)."""
    data = json.loads(accounts_path.read_text())
    total = data["total_contas_ad"]
    orfas = data.get("contas_inativas_90d", [])
    sem_dono = [c for c in orfas if c.get("dono") in (None, "desconhecido")]
    n = len(orfas)
    if not orfas:
        status, rec = "EFICAZ", "Nenhuma conta inativa sem dono identificado."
    elif n <= 2:
        status, rec = "PARCIAL", "Poucas contas órfãs: validar e desativar em até 30 dias."
    else:
        status, rec = "INEFICAZ", "Automatizar desativação de contas no offboarding (integração RH x AD)."
    return Controle(
        id="A.5.15",
        nome="Controle de Acesso (contas órfãs)",
        status=status,
        evidencia="contas_ativas.json",
        detalhes=f"{n} contas inativas >90d em {total} contas AD ({len(sem_dono)} sem dono)",
        recomendacao=rec,
    )


def run(base_dir: Path) -> list[Controle]:
    return [
        check_mfa(base_dir / "usuarios.csv"),
        check_backup(base_dir / "backup.json"),
        check_retencao(base_dir / "politicas.json"),
        check_contas_orfas(base_dir / "contas_ativas.json"),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GRC Compliance-as-Code")
    parser.add_argument("--json", dest="saida", default="relatorio_controles.json")
    parser.add_argument("--base-dir", dest="base", default=".")
    args = parser.parse_args(argv)

    controles = run(Path(args.base))
    eficaz = sum(1 for c in controles if c.status == "EFICAZ")
    parcial = sum(1 for c in controles if c.status == "PARCIAL")
    ineficaz = sum(1 for c in controles if c.status == "INEFICAZ")

    relatorio = {
        "gerado_em": CURRENT.isoformat(),
        "framework": "ISO/IEC 27001:2022 (Anexo A)",
        "resumo": {
            "total": len(controles),
            "eficaz": eficaz,
            "parcial": parcial,
            "ineficaz": ineficaz,
        },
        "controles": [asdict(c) for c in controles],
    }

    out = Path(args.saida)
    out.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2))
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    print(f"\nResumo: {eficaz} EFICAZ · {parcial} PARCIAL · {ineficaz} INEFICAZ "
          f"(relatório em {out.name})")
    return 1 if ineficaz > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
