import cv2
import math
from cvzone.HandTrackingModule import HandDetector

# Inicializar a webcam
webcam = cv2.VideoCapture(0)

# Inicializar o detector de mãos
rastreador = HandDetector(detectionCon=0.8, maxHands=2)

# Definir a distância máxima entre o polegar e os outros dedos que será considerada 100% de abertura
DISTANCIA_MAXIMA = 200  # Ajuste essa distância conforme necessário

while True:
    sucesso, imagem = webcam.read()
    
    if not sucesso:
        print("Não foi possível acessar a webcam.")
        break

    # Detectar as mãos na imagem
    hands, imagem_maos = rastreador.findHands(imagem)

    # Verificar se alguma mão foi detectada
    if hands:
        for hand in hands:
            # Obter os pontos da mão (landmarks)
            lmList = hand['lmList']
            
            # Definir os pontos das pontas dos dedos e articulações intermediárias
            pontos_dedos = [4, 8, 12, 16, 20]  # Polegar, indicador, médio, anelar, mínimo
            juntas_intermediarias = [3, 6, 10, 14, 18]  # Juntas intermediárias dos dedos
            
            dedos_levantados = []

            # Verificar se o polegar está levantado (baseado na posição x)
            if hand['type'] == 'Right':  # Mão direita
                if lmList[4][0] > lmList[3][0]:  # Ponta do polegar está à direita da articulação
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)
            else:  # Mão esquerda
                if lmList[4][0] < lmList[3][0]:  # Ponta do polegar está à esquerda da articulação
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)

            # Verificar se os outros dedos estão levantados (baseado na posição y)
            for i in range(1, 5):  # Para os dedos indicador, médio, anelar e mínimo
                # Verificar se a ponta do dedo está acima da junta intermediária
                if lmList[pontos_dedos[i]][1] < lmList[juntas_intermediarias[i]][1]:  # Ponta acima da junta
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)
            
            # Determinar qual mão é (direita ou esquerda)
            lado_mao = 'Direita' if hand['type'] == 'Right' else 'Esquerda'

            # Exibir os resultados de quais dedos estão levantados
            for i, status in enumerate(dedos_levantados):
                nome_dedo = ['Polegar', 'Indicador', 'Médio', 'Anelar', 'Mínimo'][i]
                estado = 'Levantado' if status == 1 else 'Baixado'
                cv2.putText(imagem_maos, f'{nome_dedo}: {estado}', (10, 70 + 50 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Mostrar a porcentagem geral de abertura dos dedos
            porcentagem_geral = sum(dedos_levantados) / len(dedos_levantados) * 100
            cv2.putText(imagem_maos, f'Mao {lado_mao}: {porcentagem_geral:.2f}% Abertura', (10, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    else:
        # Caso nenhuma mão seja detectada, exibir mensagem
        cv2.putText(imagem, "Mao nao detectada", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        imagem_maos = imagem

    # Mostrar a imagem com a detecção das mãos
    cv2.imshow("Projeto 04 - IA", imagem_maos)

    # Verificar se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a webcam e fechar as janelas
webcam.release()
cv2.destroyAllWindows()
