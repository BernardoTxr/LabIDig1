import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

METRICAS_FILEPATH = "metricas.csv"

# Configuração da página
st.set_page_config(page_title="Cognos", layout="wide")
st.title("Acompanhamento do Jogador - Cognos")
st.markdown("""
    Este dashboard mostra as métricas de desempenho de jogadores no jogo Genius.
    Os dados são atualizados automaticamente a cada 5 segundos.
""")

# Tempo de atualização automática (em segundos)
INTERVALO_ATUALIZACAO = 3

# Criação de espaços reservados para atualização dinâmica
placeholder = st.empty()

# Loop para atualização contínua
while True:
    # Carregar os dados SEM CACHE para sempre pegar os valores mais recentes
    data = pd.read_csv(METRICAS_FILEPATH)

    # Criar um bloco de exibição atualizado dentro do placeholder
    with placeholder.container():
        col1, col2, col3 = st.columns([4, 4, 1])

        # Seção de métricas
        with col1:
            st.subheader("📊 Métricas da Sessão")
            
            # Tempo médio de resposta
            st.metric("Tempo Médio de Resposta (s)", f"{np.mean(data['tempo_medio_de_resposta']):.2f} s")
            
            # Score de acerto médio
            st.metric("Score de Acerto Médio", f"{np.mean(data['numero_de_acertos']):.2f}")
            
            # Tempo mínimo de resposta
            st.metric("Tempo Mínimo de Resposta (s)", f"{np.min(data['tempo_medio_de_resposta']):.2f} s")
            
            # Variação do tempo de resposta (Desvio padrão)
            st.metric("Variação do Tempo de Resposta", f"{np.std(data['tempo_medio_de_resposta']):.2f} s")
            
            # Maior sequência de acertos
            st.metric("Maior Sequência de Acertos", f"{max(data['numero_de_acertos'])}")
            
            # Tempo médio de sessão
            st.metric("Tempo Médio de Sessão (s)", f"{np.mean(data['tempo_da_sessao']):.2f} s")
            
            # Tempo total da sessão (em minutos)
            st.metric("Tempo Total da Sessão (min)", f"{np.sum(data['tempo_da_sessao']) / 60:.2f} min")


        # Seção de gráficos
        with col2:
            st.subheader("📉 Gráficos de Desempenho")

            st.subheader("Distribuição do Tempo de Resposta")
            fig, ax = plt.subplots()
            sns.histplot(data['tempo_medio_de_resposta'], kde=True, ax=ax)
            ax.set_title("Distribuição do Tempo de Resposta")
            ax.set_xlabel("Tempo de Resposta (s)")
            ax.set_ylabel("Frequência")
            st.pyplot(fig)

            st.subheader("Acertos por jogada")
            fig, ax = plt.subplots()
            sns.lineplot(x=range(len(data)), y=data['numero_de_acertos'], ax=ax, color='red')
            ax.set_title("Acertos ao Longo do Jogo")
            ax.set_xlabel("Número da Jogada")
            ax.set_ylabel("Erros")
            st.pyplot(fig)

        with col3:
            st.image('images/icone.jpeg')



    # Aguardar antes da próxima atualização
    time.sleep(INTERVALO_ATUALIZACAO)
    
    # Atualizar os valores sem recarregar a página
    st.rerun()
