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
st.markdown(
    """
    Este dashboard mostra as métricas de desempenho do jogador no Cognos.
    Os dados são atualizados automaticamente a cada 3 segundos.
"""
)

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
        col1, col2 = st.columns([2, 8])

        # Seção de métricas
        with col1:
            st.subheader("📊 Métricas da Sessão")

            # Score de acerto médio
            st.metric(
                "Sequênia de Acertos Média", f"{np.mean(data['numero_de_acertos']):.2f}"
            )

            # Maior sequência de acertos
            st.metric("Maior Sequência de Acertos", f"{max(data['numero_de_acertos'])}")

            # Tempo médio de resposta
            st.metric(
                "Tempo Médio de Resposta (s)",
                f"{np.mean(data['tempo_medio_de_resposta']):.2f} s",
            )

            # Tempo mínimo de resposta
            st.metric(
                "Tempo Mínimo de Resposta (s)",
                f"{np.min(data['tempo_medio_de_resposta']):.2f} s",
            )

            # Variação do tempo de resposta (Desvio padrão)
            st.metric(
                "Variação do Tempo de Resposta",
                f"{np.std(data['tempo_medio_de_resposta']):.2f} s",
            )

            # Tempo médio de sessão
            st.metric(
                "Tempo Médio por Rodada (s)",
                f"{np.mean(data['tempo_da_sessao']):.2f} s",
            )

            # Tempo total da sessão (em minutos)
            st.metric(
                "Tempo Total da Sessão (min)",
                f"{np.sum(data['tempo_da_sessao']) / 60:.2f} min",
            )

        # Seção de gráficos
        with col2:
            col21, col22 = st.columns(2)
            figsize = (4, 3)
            with col21:
                # Gráfico de distribuição do tempo médio de resposta
                fig, ax = plt.subplots(figsize=figsize)
                sns.histplot(
                    data["tempo_medio_de_resposta"],
                    kde=True,
                    ax=ax,
                    bins=20,
                    color="lightblue",
                )
                ax.set_title(
                    "Distribuição do Tempo de Resposta", fontsize=10, color="black"
                )
                ax.set_xlabel("Tempo de Resposta (s)", fontsize=6, color="black")
                ax.set_ylabel("Frequência", fontsize=6, color="black")
                ax.tick_params(axis="both", colors="gray")  # Torna os ticks cinzas
                for spine in ax.spines.values():  # Remover a borda (spines)
                    spine.set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)

                # Gráfico de dispersão com linha de regressão: Tempo Médio de Resposta vs Número de Acertos
                fig, ax = plt.subplots(figsize=figsize)
                sns.regplot(
                    x=data["tempo_medio_de_resposta"],
                    y=data["numero_de_acertos"],
                    ax=ax,
                    scatter_kws={
                        "color": "gray",
                        "alpha": 0.6,
                    },  # Pontos em cinza suave
                    line_kws={
                        "color": "lightblue",
                        "lw": 2,
                    },  # Linha de regressão em vermelho claro
                    ci=None,  # Não mostrar intervalo de confiança
                )
                ax.set_title(
                    "Tempo Médio de Resposta vs Número de Acertos",
                    fontsize=10,
                    color="black",
                )
                ax.set_xlabel("Tempo Médio de Resposta (s)", fontsize=6, color="black")
                ax.set_ylabel("Número de Acertos", fontsize=6, color="black")
                ax.tick_params(axis="both", colors="gray")  # Torna os ticks cinzas
                for spine in ax.spines.values():  # Remover a borda (spines)
                    spine.set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)

            with col22:
                # Gráfico de distribuição do número de acertos
                fig, ax = plt.subplots(figsize=figsize)
                sns.histplot(
                    data["numero_de_acertos"],
                    kde=True,
                    ax=ax,
                    bins=20,
                    color="lightblue",
                )
                ax.set_title(
                    "Distribuição do Número de Acertos", fontsize=10, color="black"
                )
                ax.set_xlabel("Número de Acertos", fontsize=6, color="black")
                ax.set_ylabel("Frequência", fontsize=6, color="black")
                ax.tick_params(axis="both", colors="gray")  # Torna os ticks cinzas
                for spine in ax.spines.values():  # Remover a borda (spines)
                    spine.set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)

                # Gráfico de acertos ao longo da sessão
                fig, ax = plt.subplots(figsize=figsize)
                sns.lineplot(
                    x=range(len(data)),
                    y=data["numero_de_acertos"],
                    ax=ax,
                    color="lightblue",  # Linha em vermelho claro
                    lw=2,  # Largura da linha
                )
                ax.set_title("Acertos ao Longo da Sessão", fontsize=10, color="black")
                ax.set_xlabel("Número da Rodada", fontsize=6, color="black")
                ax.set_ylabel("Número de Acertos", fontsize=6, color="black")
                ax.tick_params(axis="both", colors="gray")  # Torna os ticks cinzas
                for spine in ax.spines.values():  # Remover a borda (spines)
                    spine.set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)

    # Aguardar antes da próxima atualização
    time.sleep(INTERVALO_ATUALIZACAO)

    # Atualizar os valores sem recarregar a página
    st.rerun()
