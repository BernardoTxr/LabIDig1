from WF_SDK import device, static, supplies       # import instruments
from time import sleep                           # needed for delays
import time
import json
import os
import pandas as pd

DEVICE_NAME = "Analog Discovery 2"
CSV_METRICAS = 'metricas.csv'
SLEEP_DELAY = 0.01
ESTADO_INICIAL = 0
ESTADO_PREPARACAO = 1
ESTADO_INICIA_SEQUENCIA = 2
ESTADO_CARREGA_DADO = 3
ESTADO_MOSTRA_DADO = 4
ESTADO_ZERA_LEDS = 5
ESTADO_MOSTRA_ZERO = 6
ESTADO_CONTA_LED = 7
ESTADO_COMECA_JOGADAS = 8
ESTADO_ESPERA_JOGADA = 9
ESTADO_REGISTRA_JOGADA = 10
ESTADO_COMPARA = 11
ESTADO_CONTA_E_PASSA = 12
ESTADO_FIM_SEQUENCIA = 13
ESTADO_FIM_GANHOU = 14
ESTADO_FIM_PERDEU = 15
ESTADO_FIM_TIMEOUT = 16
ESTADO_ESCRITA_RAM = 17
ESTADO_CONTA_RAM = 18
ESTADO_NOVA_JOGADA = 19
ESTADOS_FINAIS = [ESTADO_FIM_PERDEU, ESTADO_FIM_TIMEOUT]


'''
Um arquivo JSON:
1. Possui métricas consolidadas de uma única sessão:
    tempo_medio_de_resposta
    score (numero de acertos)
    tempo_de_uma_sessao
'''



class AnalogReader:
    def __init__(self) -> None:
        self.device_name = DEVICE_NAME
        self.estados_temp = [] # estados temporários ainda não consolidados
        if not os.path.exists(CSV_METRICAS):
            df = pd.DataFrame(columns=["tempo_medio_de_resposta", "numero_de_acertos", "tempo_da_sessao"])
            df.to_csv(CSV_METRICAS, index=False)
        self.analog_loop()

    def consolidate_data(self, medicoes) -> None:
        """
        Consolida os dados de medição em um arquivo JSON.
        """
        def calcula_tempo_medio_de_resposta(medicoes)->float:
            """
            Para cada medição em ESPERA_JOGADA, verifica-se o tempo
            para trocar de estado.
            """
            soma_tempo = 0
            contador = 0
            for i in range(len(medicoes)):
                if (medicoes[i][0] == ESTADO_ESPERA_JOGADA):
                    soma_tempo += medicoes[i+1][1] - medicoes[i][1]
                    contador += 1
            if contador ==0:
                retorno = 0
            else:
                retorno = soma_tempo/contador
            return retorno

        def calcula_numero_de_acertos(medicoes)-> int:
            contador = 0
            for i in range(len(medicoes)):
                if (medicoes[i][0] == ESTADO_ESPERA_JOGADA):
                    contador += 1
            if contador ==0:
                retorno = 0
            else:
                retorno = contador - 1
            return retorno
        
        def calcula_tempo_da_sessao(medicoes)->float:
            return medicoes[-1][1] - medicoes[0][1]

        
        # cria um dicionário com os dados consolidados
        dados_consolidados = {
            "tempo_medio_de_resposta": calcula_tempo_medio_de_resposta(medicoes),
            "numero_de_acertos": calcula_numero_de_acertos(medicoes),
            "tempo_da_sessao": calcula_tempo_da_sessao
        }
        
        # Carrega o CSV existente e adiciona os novos dados
        df = pd.read_csv(CSV_METRICAS)
        df = pd.concat([df, pd.DataFrame([dados_consolidados])], ignore_index=True)

        # Salva o DataFrame atualizado no CSV
        df.to_csv(CSV_METRICAS, index=False)
        print("Dados consolidados!")

        
        

    def convert_dec(self, bin):
        dec = 0
        for i in range(len(bin)):
            if (bin[i]):
                dec += 2**i
        return dec

    def analog_loop(self):
        # connect to the device
        device_data = device.open()
        device_data.name = self.device_name
        
        # start the positive supply
        supplies_data = supplies.data()
        supplies_data.master_state = True
        supplies_data.state = True
        supplies_data.voltage = 3.3
        supplies.switch(device_data, supplies_data)
    
        # set all pins as input
        for index in range(16):
            static.set_mode(device_data, index, False)
        
        try:
            estadoAnterior = -1
            inicial = time.time()
            while True:
                # go through possible states
                estados_brutos = []
                for index in range(10,16):
                    # set the state of every DIO channel
                    estados_brutos.append(static.get_state(device_data, index)) 
                sleep(SLEEP_DELAY)  # delay
                numero_decimal = sum([bit * (2 ** i) for i, bit in enumerate(estados_brutos)])

                if (estadoAnterior != numero_decimal):
                    estadoAnterior = numero_decimal
                    self.estados_temp.append((numero_decimal,time.time()-inicial))
                    print("Estado no tempo "+str(time.time()-inicial)+": " + str(numero_decimal))
                    print(estados_brutos)
                
                    # se chegar em um dos estados finais, consolida os dados
                    if (numero_decimal in ESTADOS_FINAIS):
                        print("Chegou em um estado final!")
                        self.consolidate_data(self.estados_temp)
                        self.estados_temp = []

        except KeyboardInterrupt:
            # stop if Ctrl+C is pressed
            print("ctrl c")
            pass
        
        finally:
            print("End Process!")

            # stop the static I/O
            static.close(device_data)
        
            # stop and reset the power supplies
            supplies_data.master_state = False
            supplies.switch(device_data, supplies_data)
            supplies.close(device_data)
        
            # close the connection
            device.close(device_data)