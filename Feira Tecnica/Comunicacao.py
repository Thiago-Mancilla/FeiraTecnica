import serial  # Importa a biblioteca

arduino = serial
def conexao():
    while True:  # Loop para a conexão com o Arduino
        try:  # Tenta se conectar, se conseguir, o loop se encerra
            arduino = serial.Serial('COM3', 9600)
            print('Arduino conectado')
            break
        except:
            pass

def dados(cmd):
    arduino = serial.Serial('COM3', 9600)
    print('Arduino conectado')
    while True:  # Loop principal
        if cmd in [10, 11]:  # Se a resposta for 1, 2 ou 3, ele envia o comando ao Arduino
            arduino.write(cmd.encode())  # Envia o comando ('1', '2' ou '3') para o Arduino

        arduino.flush()  # Limpa a comunicação
