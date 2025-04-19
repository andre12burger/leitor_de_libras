import cv2
import mediapipe as mp


def main():
    # Inicialize o objeto para captura de vídeo da webcam
    cap = cv2.VideoCapture(0)

    # Inicialize o detector de mãos
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Verifique se a câmera foi aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    while True:
        # Capture o frame da câmera
        ret, frame = cap.read()

        # Verifique se o frame foi capturado corretamente
        if not ret:
            print("Erro ao capturar o frame.")
            break

        # Converta a imagem de BGR para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processamento da imagem para detecção de mãos
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    # Obtenha as coordenadas x, y do landmark (ponto)
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # Desenhe um círculo no ponto (landmark)
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

        # Display o frame resultante
        cv2.imshow('Hand Detection', frame)

        # Aguarde 1 milissegundo e verifique se a tecla 'q' foi pressionada para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libere os recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()