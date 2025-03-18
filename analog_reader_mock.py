import queue
import threading
import time
import random

def mock_analog_loop(data_queue):
    """
    Simula a leitura do Analog Discovery, gerando valores aleatórios para os estados dos pinos.
    """
    try:
        estado_anterior = -1
        inicial = time.time()

        while True:
            # Simulamos os estados com valores binários aleatórios (0 ou 1)
            estados_temp = [random.randint(0, 1) for _ in range(6)]
            time.sleep(2)  # Simula o delay de leitura do dispositivo

            # Converte os bits em um número decimal
            numero_decimal = sum([bit * (2 ** i) for i, bit in enumerate(estados_temp)])

            if estado_anterior != numero_decimal:
                estado_anterior = numero_decimal
                timestamp = time.time() - inicial
                data_queue.put((timestamp, numero_decimal))
                print(f"[Mock] Estado no tempo {timestamp:.2f}s: {numero_decimal}")

    except KeyboardInterrupt:
        print("Encerrando Mock")
