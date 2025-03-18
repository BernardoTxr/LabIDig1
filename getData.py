from WF_SDK import device, static, supplies       # import instruments
from time import sleep                           # needed for delays
import time

device_name = "Analog Discovery"


def convert_dec(bin):
    dec = 0
    for i in range(len(bin)):
        if (bin[i]):
            dec += 2**i
    return dec


def analog_loop():
    # connect to the device
    device_data = device.open()
    device_data.name = device_name
    
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
            estados_temp = []
            for index in range(10,16):
                # set the state of every DIO channel
                estados_temp.append(static.get_state(device_data, index))
            sleep(0.01)  # delay

            numero_decimal = sum([bit * (2 ** i) for i, bit in enumerate(estados_temp)])

            if (estadoAnterior != numero_decimal):
                estadoAnterior = numero_decimal
                print("Estado no tempo "+str(time.time()-inicial)+": " + str(numero_decimal))

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

analog_loop()
