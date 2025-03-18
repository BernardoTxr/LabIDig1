import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Função para gerar dados de exemplo (substitua com seus dados reais)
def generate_sample_data():
    # Gerar dados de exemplo para o tempo de resposta
    response_times = np.random.normal(loc=2, scale=0.5, size=100)
    correct_answers = np.random.randint(1, 5, size=100)
    errors = np.random.randint(0, 2, size=100)
    session_times = np.random.randint(10, 30, size=100)
    return response_times, correct_answers, errors, session_times

# Definir título e descrição da página
st.set_page_config(page_title="Cognos", layout="wide")
st.title("Acompanhamento do Jogador - Cognos")
st.markdown("""
    Este dashboard mostra as métricas de desempenho de jogadores no jogo Genius.
    Selecione as visualizações para acompanhar o desempenho dos jogadores.
""")


# Gerar dados de exemplo
response_times, correct_answers, errors, session_times = generate_sample_data()

# Criar dataframe de exemplo
data = pd.DataFrame({
    'response_times': response_times,
    'correct_answers': correct_answers,
    'errors': errors,
    'session_times': session_times
})

# Função para exibir as métricas
def display_metrics():
    st.subheader("Métricas da Sessão")
    
    # Tempo médio de resposta
    avg_response_time = np.mean(data['response_times'])
    st.metric("Tempo Médio de Resposta (s)", f"{avg_response_time:.2f} s")
    
    # Score de acerto médio
    avg_correct_score = np.mean(data['correct_answers'])
    st.metric("Score de Acerto Médio", f"{avg_correct_score:.2f}")
    
    # Tempo mínimo de resposta
    min_response_time = np.min(data['response_times'])
    st.metric("Tempo Mínimo de Resposta (s)", f"{min_response_time:.2f} s")
    
    # Variação do tempo de resposta (Desvio padrão)
    response_time_variation = np.std(data['response_times'])
    st.metric("Variação do Tempo de Resposta", f"{response_time_variation:.2f} s")
    
    # Número total de erros
    total_errors = np.sum(data['errors'])
    st.metric("Número Total de Erros", f"{total_errors}")
    
    # Maior sequência de acertos
    longest_correct_streak = max(data['correct_answers'])
    st.metric("Maior Sequência de Acertos", f"{longest_correct_streak}")
    
    # Melhoria ao longo do tempo
    start_time = np.mean(data['response_times'][:50])  # Começo da sessão
    end_time = np.mean(data['response_times'][50:])  # Fim da sessão
    improvement = start_time - end_time
    st.metric("Melhoria ao Longo do Tempo (s)", f"{improvement:.2f} s")
    
    # Tempo de sessão médio
    avg_session_time = np.mean(data['session_times'])
    st.metric("Tempo Médio de Sessão (min)", f"{avg_session_time:.2f} min")

# Exibir gráfico de tempos de resposta
def plot_response_time():
    st.subheader("Distribuição do Tempo de Resposta")
    fig, ax = plt.subplots()
    sns.histplot(data['response_times'], kde=True, ax=ax)
    ax.set_title("Distribuição do Tempo de Resposta")
    ax.set_xlabel("Tempo de Resposta (s)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

# Exibir gráfico de erros ao longo do tempo
def plot_errors():
    st.subheader("Erros ao Longo do Tempo")
    fig, ax = plt.subplots()
    sns.lineplot(x=range(len(data)), y=data['errors'], ax=ax, color='red')
    ax.set_title("Erros ao Longo do Jogo")
    ax.set_xlabel("Jogada")
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