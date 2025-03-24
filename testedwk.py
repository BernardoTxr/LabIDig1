import time
from dwf import DwfDevice, FDwfEnum, FDwfEnumDeviceName

# Função para verificar se há dispositivos conectados
def verificar_conexao():
    return FDwfEnum() > 0  # Retorna True se há dispositivos conectados

# Verificar se há dispositivos antes de tentar abrir um
if verificar_conexao():
    dispositivo = DwfDevice(idxDevice=0)  # Abre o primeiro dispositivo encontrado
    print(dispositivo)
    if dispositivo.handle is not None:  # Verifica se o handle do dispositivo é válido
        print("Dispositivo aberto com sucesso.")
    else:
        print("Falha ao abrir o dispositivo.")
else:
    print("Nenhum dispositivo encontrado para abrir.")
