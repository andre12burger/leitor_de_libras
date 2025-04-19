import os
import pickle
import mediapipe as mp
import cv2
from tqdm import tqdm  # Biblioteca para barra de progresso

# Configuração do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

# Processar cada diretório e imagem
for dir_ in tqdm(os.listdir(DATA_DIR), desc="Processando diretórios"):
    dir_path = os.path.join(DATA_DIR, dir_)
    if not os.path.isdir(dir_path):
        continue  # Ignorar arquivos que não sejam diretórios

    for img_path in tqdm(os.listdir(dir_path), desc=f"Processando imagens em {dir_}", leave=False):
        img_full_path = os.path.join(dir_path, img_path)

        # Carregar e converter a imagem
        img = cv2.imread(img_full_path)
        if img is None:
            print(f"Erro ao carregar a imagem: {img_full_path}")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processar a imagem com MediaPipe
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extrair e normalizar os landmarks
                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]

                min_x, min_y = min(x_), min(y_)
                data_aux = [(x - min_x, y - min_y) for x, y in zip(x_, y_)]
                data_aux = [coord for pair in data_aux for coord in pair]  # Achatar a lista

                data.append(data_aux)
                labels.append(dir_)

# Salvar os dados em um arquivo pickle
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Dataset criado e salvo em 'data.pickle'.")