import streamlit as st
import pandas as pd
import plotly.express as px


# Simulação de dados (substituir pelos dados da FPGA)
def generate_mock_data():
    import numpy as np

    timestamps = pd.date_range(start="2024-01-01", periods=100, freq="S")
    estados = np.random.choice(
        ["Acerto", "Erro", "Timeout"], size=100, p=[0.7, 0.2, 0.1]
    )
    tempos_resposta = np.random.randint(1, 5, size=100)  # Tempo de resposta em segundos
    return pd.DataFrame(
        {"Timestamp": timestamps, "Estado": estados, "Tempo_Resposta": tempos_resposta}
    )


# Carregar dados (trocar pela leitura dos dados reais)
df = generate_mock_data()

# Criar colunas para análise
df["Acertos"] = df["Estado"] == "Acerto"
df["Erros"] = df["Estado"] == "Erro"
df["Timeouts"] = df["Estado"] == "Timeout"

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
