import json
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="GRC Risk Dashboard", layout="wide", page_icon="🛡️")
st.title("🛡️ GRC Risk Dashboard — Vilhena Fintech S.A.")
st.caption(f"Fictício · atualizado em {datetime.now():%d/%m/%Y}")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_COM = os.path.join(BASE, "03-compliance-as-code")


@st.cache_data
def carregar_riscos():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "risk_register.xlsx")
    df = pd.read_excel(path)
    df["Prob"] = pd.to_numeric(df["Prob"], errors="coerce")
    df["Impacto"] = pd.to_numeric(df["Impacto"], errors="coerce")
    df["Nivel"] = df[["Prob", "Impacto"]].sum(axis=1)
    return df


@st.cache_data
def carregar_controles():
    path = os.path.join(DIR_COM, "relatorio_controles.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        dados = json.load(f)
    return dados


df = carregar_riscos()
controles = carregar_controles()

# ---- KPIs ----
total_riscos = len(df)
kpi_altos = (df["Nivel"] >= 7).sum()
kpi_abertos = (df["Status"] != "Aceito").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Riscos mapeados", total_riscos)
col2.metric("Riscos altos/críticos (≥7)", kpi_altos)
col3.metric("Riscos em tratamento", kpi_abertos)
if controles:
    r = controles["resumo"]
    col4.metric("Controles INEFICAZ (Anexo A)", r["ineficaz"], delta=f"{r['eficaz']} eficazes")
else:
    col4.metric("Controles INEFICAZ", "—", delta="rode check_controls.py")

# ---- Sidebar: filtros ----
st.sidebar.header("Filtros")
categorias = ["Todas"] + sorted(df["Categoria"].dropna().unique().tolist())
categoria = st.sidebar.selectbox("Categoria", categorias)
statuses = ["Todos"] + sorted(df["Status"].dropna().unique().tolist())
status_f = st.sidebar.selectbox("Status", statuses)

df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]
if status_f != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status"] == status_f]

aba_heatmap, aba_riscos, aba_controles = st.tabs(
    ["Heatmap de Risco", "Registro de Riscos", "Compliance (Anexo A)"]
)

with aba_heatmap:
    matrix = [[0] * 5 for _ in range(5)]
    for _, r in df_filtrado.iterrows():
        if pd.notna(r["Prob"]) and pd.notna(r["Impacto"]):
            p = int(r["Prob"]) - 1
            i = int(r["Impacto"]) - 1
            matrix[4 - i][p] += 1
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=["1-Raro", "2-Improv", "3-Possível", "4-Provável", "5-Quase Certo"],
            y=["5-Catast", "4-Maior", "3-Mod", "2-Menor", "1-Insig"],
            colorscale="Reds",
            text=matrix,
            texttemplate="%{text}",
        )
    )
    fig.update_layout(title="Mapa de Calor — Inerente (5×5)", height=480)
    st.plotly_chart(fig, width="stretch")

with aba_riscos:
    st.dataframe(df_filtrado, width="stretch", hide_index=True)
    if total_riscos:
        fig_bar = px.bar(
            df_filtrado.sort_values("Nivel"),
            x="Risco",
            y="Nivel",
            color="Categoria",
            labels={"Risco": "Risco", "Nivel": "Nível (Prob+Impacto)"},
            title="Perfil de risco por item",
            height=420,
        )
        st.plotly_chart(fig_bar, width="stretch")

with aba_controles:
    if controles:
        dfc = pd.DataFrame(controles["controles"])
        cores = {"EFICAZ": "green", "PARCIAL": "orange", "INEFICAZ": "red"}
        dfc["cor"] = dfc["status"].map(cores)
        fig_c = go.Figure(
            go.Bar(
                x=dfc["id"],
                y=[1] * len(dfc),
                marker_color=dfc["cor"],
                text=dfc["status"],
                textposition="outside",
            )
        )
        fig_c.update_layout(
            title="Status dos controles verificados por compliance-as-code",
            yaxis=dict(visible=False),
            height=360,
        )
        st.plotly_chart(fig_c, width="stretch")
        st.dataframe(
            dfc[["id", "nome", "status", "detalhes", "recomendacao"]],
            width="stretch",
            hide_index=True,
        )
    else:
        st.warning("Relatório ausente. Rode `python check_controls.py` em 03-compliance-as-code.")
