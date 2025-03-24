import time
from dwf import DwfDevice, FDwfEnum, FDwfEnumDeviceName

# Verifica quantos dispositivos estão disponíveis
num_dispositivos = FDwfEnum()
print(f"Dispositivos disponíveis: {num_dispositivos}")

if num_dispositivos > 0:
    # Mostra informações dos dispositivos disponíveis
    for i in range(num_dispositivos):
        nome = FDwfEnumDeviceName(i)
        print(f"Dispositivo {i}: {nome}")

    # Abre o primeiro dispositivo disponível
    dispositivo = DwfDevice(idxDevice=0)
    
    if dispositivo.handle is not None:
        print("Dispositivo aberto com sucesso:", dispositivo)
    else:
        print("Falha ao abrir o dispositivo. Tente reconectar o hardware.")
else:
    print("Nenhum dispositivo encontrado. Verifique a conexão USB e o driver.")
