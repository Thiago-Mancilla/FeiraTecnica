import cv2
import math
from cvzone.HandTrackingModule import HandDetector
import serial  # Importa a biblioteca

# Conexão com o Arduino
while True:  # Loop para a conexão com o Arduino
    try:
        arduino = serial.Serial('COM3', 9600)  # Adiciona timeout
        print('Arduino conectado')
        break
    except:
        pass

def dados(cmd):
    # Envia o comando para o Arduino
    arduino.write(str(cmd).encode())  # Converte o comando para string antes de enviar
    arduino.flush()  # Limpa a comunicação

# Inicializar a webcam
webcam = cv2.VideoCapture(0)

# Inicializar o detector de mãos
rastreador = HandDetector(detectionCon=0.8, maxHands=2)

# Configurar janela em modo janela
cv2.namedWindow("Projeto 04 - IA")

while True:
    sucesso, imagem = webcam.read()
    
    if not sucesso:
        print("Não foi possível acessar a webcam.")
        break

    # Detectar as mãos na imagem
    hands, imagem_maos = rastreador.findHands(imagem)

    # Verificar se alguma mão foi detectada
    if hands:
        if hands:
            for hand in hands:
                lmList = hand['lmList']
                if len(lmList) < 21:  # Verifique se há pontos suficientes
                    continue
                
                # Definir os pontos das pontas dos dedos e articulações intermediárias
                pontos_dedos = [4, 8, 12, 16, 20]
                juntas_intermediarias = [3, 6, 10, 14, 18]

                dedos_levantados = []

                # Verificar se o polegar está levantado
                if hand['type'] == 'Right':  # Mão direita
                    dedos_levantados.append(1 if lmList[4][0] > lmList[3][0] else 0)
                else:  # Mão esquerda
                    dedos_levantados.append(1 if lmList[4][0] < lmList[3][0] else 0)

                # Verificar se os outros dedos estão levantados
                for i in range(1, 5):
                    dedos_levantados.append(1 if lmList[pontos_dedos[i]][1] < lmList[juntas_intermediarias[i]][1] else 0)

                lado_mao = 'Direita' if hand['type'] == 'Right' else 'Esquerda'
                valor = int

                # Exibir os resultados de quais dedos estão levantados
                for i, status in enumerate(dedos_levantados):
                    nome_dedo = ['Polegar', 'Indicador', 'Médio', 'Anelar', 'Mínimo'][i]
                    estado = 'Levantado' if status == 1 else 'Abaixado'

                    # Definir o valor a ser enviado ao Arduino
                    if nome_dedo == 'Polegar':
                        if estado == 'Levantado':
                            valor = '11'
                        else: 
                            valor = '10'
                        dados(valor)                            
                    elif nome_dedo == 'Indicador':
                        valor = '21' if estado == 'Levantado' else '20'
                    elif nome_dedo == 'Médio':
                        valor = '31' if estado == 'Levantado' else '30'
                    elif nome_dedo == 'Anelar':
                        valor = '41' if estado == 'Levantado' else '40'
                    else:  # Mínimo
                        valor = '51' if estado == 'Levantado' else '50'

                    # Enviar o valor ao Arduino
                    #dados(valor)

                    # Exibir na imagem
                    cv2.putText(imagem_maos, f'{nome_dedo}: {estado} - {valor}', (10, 50 + 30 * i),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                # Mostrar a porcentagem geral de abertura dos dedos
                porcentagem_geral = sum(dedos_levantados) / len(dedos_levantados) * 100
                cv2.putText(imagem_maos, f'Mão {lado_mao}: {porcentagem_geral:.2f}% de Abertura', (10, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    else:
        cv2.putText(imagem, "Mão não detectada", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        imagem_maos = imagem

    # Mostrar a imagem
    cv2.imshow("Projeto 04 - IA", imagem_maos)

    # Verificar se a tecla 'ESC' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == 27:  # 27 é o código ASCII para a tecla ESC
        break

# Liberar a webcam e fechar as janelas
webcam.release()
cv2.destroyAllWindows()
