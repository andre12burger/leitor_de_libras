import pickle
import cv2
import mediapipe as mp
import numpy as np

# Carregar o modelo
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Inicializar a captura de vídeo
cap = cv2.VideoCapture(0)

# Configurar MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5)

# Dicionário de rótulos
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'I', 8: 'L', 9: 'M', 10: 'N', 11: 'O', 12: 'P', 13: 'Q', 14: 'R', 15: 'S', 16: 'T', 17: 'U', 18: 'V', 19: 'W'}

def process_landmarks(hand_landmarks, W, H):
    """Processa os landmarks da mão e retorna os dados normalizados e as coordenadas do retângulo."""
    x_ = [lm.x for lm in hand_landmarks.landmark]
    y_ = [lm.y for lm in hand_landmarks.landmark]

    min_x, max_x = min(x_), max(x_)
    min_y, max_y = min(y_), max(y_)

    # Normalizar os dados
    data_aux = [(x - min_x, y - min_y) for x, y in zip(x_, y_)]
    data_aux = [coord for pair in data_aux for coord in pair]  # Achatar a lista

    # Coordenadas do retângulo
    x1 = int(min_x * W) - 10
    y1 = int(min_y * H) - 10
    x2 = int(max_x * W) - 10
    y2 = int(max_y * H) - 10

    return data_aux, x1, y1, x2, y2

def draw_prediction(frame, predicted_character, x1, y1, x2, y2):
    """Desenha o retângulo e o caractere previsto no frame."""
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Erro ao capturar o frame da câmera.")
        break

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processar a imagem com MediaPipe
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenhar landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Processar landmarks
            data_aux, x1, y1, x2, y2 = process_landmarks(hand_landmarks, W, H)

            if data_aux:
                # Fazer a previsão
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])] #lembrar de modificar o dicionario para o numero certo de letras

                # Desenhar a previsão no frame
                draw_prediction(frame, predicted_character, x1, y1, x2, y2)
    else:
        # Exibir mensagem se nenhuma mão for detectada
        cv2.putText(frame, "Nenhuma mao detectada", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Mostrar o frame
    cv2.putText(frame, 'Aperte "q" para sair', (10, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame)

    # Encerrar o programa ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()