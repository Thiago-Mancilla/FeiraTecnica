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

            # Coordenadas da ponta do polegar (ponto 4)
            x1, y1 = lmList[4][0], lmList[4][1]

            # Definir os pontos das pontas dos outros dedos (indicador, médio, anelar e mínimo)
            pontos_dedos = [8, 12, 16, 20]
            
            # Lista para armazenar as porcentagens de abertura de cada dedo
            porcentagens = []
            
            for ponto in pontos_dedos:
                # Coordenadas da ponta do dedo atual
                x2, y2 = lmList[ponto][0], lmList[ponto][1]
                
                # Calcular a distância euclidiana entre o polegar e o dedo atual
                distancia = math.hypot(x2 - x1, y2 - y1)
                
                # Calcular a porcentagem de abertura do dedo
                porcentagem_abertura = (distancia / DISTANCIA_MAXIMA) * 100
                porcentagem_abertura = min(max(porcentagem_abertura, 0), 100)  # Limitar entre 0 e 100%
                
                # Adicionar a porcentagem à lista
                porcentagens.append(porcentagem_abertura)
                
                # Desenhar uma linha entre o polegar e o dedo atual
                cv2.line(imagem_maos, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(imagem_maos, (x1, y1), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(imagem_maos, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
            
            # Calcular a média das porcentagens de abertura dos dedos para obter a porcentagem geral
            porcentagem_geral = sum(porcentagens) / len(porcentagens)
            
            # Determinar qual mão é (direita ou esquerda) com base no índice 0
            lado_mao = 'Direita' if hand['type'] == 'Right' else 'Esquerda'
                
            # Mostrar a porcentagem geral na imagem
            cv2.putText(imagem_maos, f'Mao {lado_mao}: {porcentagem_geral:.2f}%', (10, 70 + 50 * hands.index(hand)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
    else:
        # Caso nenhuma mão seja detectada, exibir mensagem
        cv2.putText(imagem, "Mao nao detectada", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        imagem_maos = imagem

    # Mostrar a imagem com a detecção das mãos
    cv2.imshow("Projeto 04 - IA", imagem_maos)

    # Verificar se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) != -1:
        break

# Liberar a webcam e fechar as janelas
webcam.release()
cv2.destroyAllWindows()