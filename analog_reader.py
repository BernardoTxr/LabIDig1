from WF_SDK import device, static, supplies       # import instruments
from time import sleep                           # needed for delays
import time
import json

DEVICE_NAME = "Analog Discovery"
JSON_FILE = "analog_data.json"
ESTADOS_FINAIS = [31, 63, 127, 255, 511, 1023] 

class AnalogReader:
    def __init__(self) -> None:
        self.device_name = DEVICE_NAME
        self.json_file = JSON_FILE
        self.estados_temp = [] # estados temporários ainda não consolidados
        self.estados_finais = ESTADOS_FINAIS

    def consolidate_data(self, medicoes) -> None:
        """
        Consolida os dados de medição em um arquivo JSON.
        """
        def calcula_tempo_medio_de_resposta(medicoes)->float:
            """
            Calcula o tempo médio de resposta do dispositivo.
            """
            tempos = [medicao[1] for medicao in medicoes]
            return tempos[-1] - tempos[0]
        def calcula_numero_total_de_sessoes(medicoes)->int:
            """
            Calcula o número total de sessões de medição.
            """
            return len(medicoes)
        # cria um dicionário com os dados consolidados
        dados_consolidados = {
            "tempo_medio_de_resposta": calcula_tempo_medio_de_resposta(medicoes),
            "numero_total_de_sessoes": calcula_numero_total_de_sessoes(medicoes)
        }
        # salva os dados consolidados em um arquivo JSON
        with open(self.json_file, "w") as file:
            json.dump(dados_consolidados, file)

        
        

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
                for index in range(10,16):
                    # set the state of every DIO channel
                    estados_brutos = []
                    estados_brutos.append(static.get_state(device_data, index)) # TODO: tirar esse append daqui
                sleep(0.01)  # delay
                numero_decimal = sum([bit * (2 ** i) for i, bit in enumerate(estados_brutos)])

                if (estadoAnterior != numero_decimal):
                    estadoAnterior = numero_decimal
                    self.estados_temp.append((numero_decimal,time.time()-inicial))
                    print("Estado no tempo "+str(time.time()-inicial)+": " + str(numero_decimal))
                
                # se chegar em um dos estados finais, consolida os dados
                if (numero_decimal in self.estados_finais):
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