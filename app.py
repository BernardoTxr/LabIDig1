import streamlit as st
import pandas as pd
import queue
import threading
import time
from analog_reader import analog_loop

# Criamos uma fila de mensagens para receber os dados
data_queue = queue.Queue()

# Iniciamos a leitura dos dados em uma thread separada
thread = threading.Thread(target=analog_loop, args=(data_queue,), daemon=True)
thread.start()

# Inicializamos o DataFrame
st.title("Monitoramento do Analog Discovery")
st.write("Exibindo os estados do dispositivo em tempo real")

data = pd.DataFrame(columns=["Tempo", "Estado"])

# Loop do Streamlit
placeholder = st.empty()

while True:
    try:
        while not data_queue.empty():
            timestamp, estado = data_queue.get()
            new_row = pd.DataFrame([[timestamp, estado]], columns=["Tempo", "Estado"])
            data = pd.concat([data, new_row], ignore_index=True)

        with placeholder.container():
            st.line_chart(data.set_index("Tempo"))  # Gráfico dinâmico
            st.dataframe(data.tail(10))  # Mostra os últimos 10 valores

        time.sleep(0.5)  # Atualiza a cada 0.5 segundos

    except Exception as e:
        st.error(f"Erro: {e}")
