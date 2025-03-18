import streamlit as st
import pandas as pd
import plotly.express as px




# Layout do dashboard
st.title("📊 Dashboard de Métricas do Jogo Genius")


# Gráfico de acertos e erros ao longo do tempo
st.subheader("Evolução dos Acertos e Erros")
fig = px.line(
    df,
    x="Timestamp",
    y=["Acertos", "Erros", "Timeouts"],
    labels={"value": "Quantidade"},
    markers=True,
)
st.plotly_chart(fig)

# Estatísticas principais
st.subheader("📈 Estatísticas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Acertos", df["Acertos"].sum())
col2.metric("Total de Erros", df["Erros"].sum())
col3.metric("Total de Timeouts", df["Timeouts"].sum())

# Histograma do tempo de resposta
st.subheader("Distribuição do Tempo de Resposta")
fig_hist = px.histogram(
    df, x="Tempo_Resposta", nbins=10, title="Tempo de Resposta (segundos)"
)
st.plotly_chart(fig_hist)

# Média de tempo de resposta ao longo do jogo
st.subheader("Tempo Médio de Resposta")
fig_tempo = px.line(
    df.groupby("Timestamp")["Tempo_Resposta"].mean().reset_index(),
    x="Timestamp",
    y="Tempo_Resposta",
    markers=True,
)
st.plotly_chart(fig_tempo)

# Rodapé
st.caption("📌 Desenvolvido para análise do desempenho no Jogo Genius.")
