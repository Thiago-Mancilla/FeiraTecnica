import cv2
import math
from cvzone.HandTrackingModule import HandDetector
import serial

# Conexão com o Arduino
'''while True:
    try:
        arduino = serial.Serial('COM3', 9600)
        print('Arduino conectado')
        break
    except:
        pass

def dados(cmd):
    arduino.write((str(cmd) + '\n').encode())
    arduino.flush()'''

# Inicializar a webcam
webcam = cv2.VideoCapture(0)

# Inicializar o detector de mãos
rastreador = HandDetector(detectionCon=0.8, maxHands=2)

# Armazenar o lado da mão detectada
mao_detectada = None

cv2.namedWindow("Projeto 04 - IA", cv2.WINDOW_NORMAL)  # Permite redimensionar a janela

while True:
    sucesso, imagem = webcam.read()
    
    if not sucesso:
        print("Não foi possível acessar a webcam.")
        break

    # Detectar as mãos na imagem
    hands, imagem_maos = rastreador.findHands(imagem)

    # Verificar se alguma mão foi detectada
    if hands:
        if mao_detectada is not None:
            for hand in hands:
                if hand['type'] == mao_detectada:
                    lmList = hand['lmList']
                    if len(lmList) < 21:
                        continue
                    
                    pontos_dedos = [4, 8, 12, 16, 20]
                    juntas_intermediarias = [3, 6, 10, 14, 18]

                    dedos_levantados = []

                    if hand['type'] == 'Right':  # Mão direita
                        dedos_levantados.append(1 if lmList[4][0] > lmList[3][0] else 0)
                    else:  # Mão esquerda
                        dedos_levantados.append(1 if lmList[4][0] < lmList[3][0] else 0)

                    for i in range(1, 5):
                        dedos_levantados.append(1 if lmList[pontos_dedos[i]][1] < lmList[juntas_intermediarias[i]][1] else 0)

                    lado_mao = 'Direita' if hand['type'] == 'Right' else 'Esquerda'
                    valor = int

                    for i, status in enumerate(dedos_levantados):
                        nome_dedo = ['Polegar', 'Indicador', 'Médio', 'Anelar', 'Mínimo'][i]
                        estado = 'Levantado' if status == 1 else 'Abaixado'

                        if nome_dedo == 'Polegar':
                            valor = '11' if estado == 'Levantado' else '10'
                        elif nome_dedo == 'Indicador':
                            valor = '21' if estado == 'Levantado' else '20'
                        elif nome_dedo == 'Médio':
                            valor = '31' if estado == 'Levantado' else '30'
                        elif nome_dedo == 'Anelar':
                            valor = '41' if estado == 'Levantado' else '40'
                        else:  # Mínimo
                            valor = '51' if estado == 'Levantado' else '50'

                        #dados(valor)

                        cv2.putText(imagem_maos, f'{nome_dedo}: {estado} - {valor}', (10, 50 + 30 * i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                    porcentagem_geral = sum(dedos_levantados) / len(dedos_levantados) * 100
                    cv2.putText(imagem_maos, f'Mão {lado_mao}: {porcentagem_geral:.2f}% de Abertura', (10, 250),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        else:
            mao_detectada = hands[0]['type']
    else:
        cv2.putText(imagem, "Mão não detectada", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        imagem_maos = imagem
        mao_detectada = None

    # Obter o tamanho da janela
    height, width = imagem.shape[:2]
    
    # Redimensionar a imagem para caber na tela
    imagem_maos = cv2.resize(imagem_maos, (width, height), interpolation=cv2.INTER_LINEAR)

    # Mostrar a imagem
    cv2.imshow("Projeto 04 - IA", imagem_maos)

    if cv2.waitKey(1) & 0xFF == 27:  # 27 é o código ASCII para a tecla ESC
        break

# Liberar a webcam e fechar as janelas
webcam.release()
cv2.destroyAllWindows()
