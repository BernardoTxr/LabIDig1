import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

METRICAS_FILEPATH = 'metricas.csv'

# Definir título e descrição da página
st.set_page_config(page_title="Cognos", layout="wide")
st.title("Acompanhamento do Jogador - Cognos")
st.markdown("""
    Este dashboard mostra as métricas de desempenho de jogadores no jogo Genius.
    Selecione as visualizações para acompanhar o desempenho dos jogadores.
""")

response_times, correct_answers, errors, session_times = 1,2,3,4

data = pd.read_csv(METRICAS_FILEPATH)




# Função para exibir as métricas
def display_metrics():
    st.subheader("Métricas da Sessão")
    
    # Tempo médio de resposta
    avg_response_time = np.mean(data['tempo_medio_de_resposta'])
    st.metric("Tempo Médio de Resposta (s)", f"{avg_response_time:.2f} s")
    
    # Score de acerto médio
    avg_correct_score = np.mean(data['numero_de_acertos'])
    st.metric("Score de Acerto Médio", f"{avg_correct_score:.2f}")
    
    # Tempo mínimo de resposta
    min_response_time = np.min(data['tempo_medio_de_resposta'])
    st.metric("Tempo Mínimo de Resposta (s)", f"{min_response_time:.2f} s")
    
    # Variação do tempo de resposta (Desvio padrão)
    response_time_variation = np.std(data['tempo_medio_de_resposta'])
    st.metric("Variação do Tempo de Resposta", f"{response_time_variation:.2f} s")
    
    # Maior sequência de acertos
    longest_correct_streak = max(data['numero_de_acertos'])
    st.metric("Maior Sequência de Acertos", f"{longest_correct_streak}")
    
    st.metric("Tempo Médio de Sessão (min)", f"{data['tempo_da_sessao']:.2f} min")

    # Tempo de sessão médio
    avg_session_time = np.mean(data['tempo_da_sessao'])
    st.metric("Tempo Total da Sessão (min)", f"{avg_session_time:.2f} min")

# Exibir gráfico de tempos de resposta
def plot_response_time():
    st.subheader("Distribuição do Tempo de Resposta")
    fig, ax = plt.subplots()
    sns.histplot(data['tempo_medio_de_resposta'], kde=True, ax=ax)
    ax.set_title("Distribuição do Tempo de Resposta")
    ax.set_xlabel("Tempo de Resposta (s)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

# Exibir gráfico de erros ao longo do tempo
def plot_errors():
    st.subheader("Acertos por jogada")
    fig, ax = plt.subplots()
    sns.lineplot(x=range(len(data))+1, y=data['numero_de_acertos'], ax=ax, color='red')
    ax.set_title("Acertos ao Longo do Jogo")
    ax.set_xlabel("Número da Jogada")
    ax.set_ylabel("Erros")
    st.pyplot(fig)

# Layout de múltiplas colunas
col1, col2, col3 = st.columns([4,4,1])

with col1:
    display_metrics()

with col2:
    plot_response_time()
    plot_errors()

with col3:
    st.image('images/icone.jpeg')