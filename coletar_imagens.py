import cv2
import os
import time

# Define quantas letras que você quer capturar
letras = 1

# Define o diretório onde as imagens serão salvas
output_directory = 'data'

# Cria diretórios para cada letra, se eles não existirem
for letra in range(letras):
    directory = os.path.join(output_directory, str(letra))
    if not os.path.exists(directory):
        os.makedirs(directory)

# Inicia a captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Contador para o número de imagens capturadas para cada letra
num_images = 100

# Loop para capturar imagens
for letra in range(letras):
    print(f"Capturando imagens para a letra {letra}")
    time.sleep(5)

    for i in range(num_images):
        # Captura um quadro do vídeo
        ret, frame = cap.read()
        
        # Mostra o quadro na tela
        cv2.imshow('Capturando...', frame)
        
        # Define o caminho para salvar a imagem
        filename = os.path.join(output_directory, str(letra), f"{letra}_{i}.png")
        
        # Salva o quadro como uma imagem
        cv2.imwrite(filename, frame)
        
        # Aguarda 100 milissegundos para a próxima captura
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

# Libera a captura de vídeo e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()