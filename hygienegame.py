import cv2
import pygame
import sys
import numpy as np

# Inicializar Pygame e OpenCV
pygame.init()
cap = cv2.VideoCapture(0)  # Iniciar a captura de vídeo (webcam)
pygame.display.set_caption("Jogo de Lavagem de Mãos")

# Configurações da janela do Pygame
LARGURA_JANELA, ALTURA_JANELA = 800, 600
screen = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))

# Carregar GIFs (substituir com os caminhos dos seus arquivos)
gifs = [
    pygame.image.load("gifexample.gif"),
    pygame.image.load("gifexample2.gif"),
    # Adicione mais conforme necessário
]

# Constantes
TEMPO_DE_EXIBICAO = 3000  # Tempo de exibição de cada GIF em milissegundos

# Função para exibir um GIF
def exibir_gif(numero):
    gif = pygame.transform.scale(gifs[numero], (400, 300))  # Redimensionar o GIF
    screen.blit(gif, (400, 0))  # Posicionar o GIF na tela

# Função para detectar movimento
def detectar_movimento(frame_anterior, frame_atual):
    # Convertendo as imagens para escala de cinza
    frame_anterior_gray = cv2.cvtColor(frame_anterior, cv2.COLOR_BGR2GRAY)
    frame_atual_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)

    # Calculando a diferença entre os quadros consecutivos
    diff = cv2.absdiff(frame_anterior_gray, frame_atual_gray)

    # Aplicando um limiar para identificar áreas com diferença significativa
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Encontrar contornos nas áreas diferenciadas
    contornos, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return len(contornos) > 0  # Retorna True se houver movimento

# Função para exibir o feed da câmera
def exibir_camera(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    frame = pygame.transform.scale(frame, (400, 300))  # Redimensionar para caber na tela
    screen.blit(frame, (0, 0))  # Posicionar na tela

# Capturando o primeiro frame
ret, frame_anterior = cap.read()
if not ret:
    print("Falha ao capturar vídeo da webcam. Verifique se a webcam está conectada e funcionando.")
    sys.exit()
    
# Função principal do jogo
def jogo():
    global frame_anterior  # Utiliza a variável global frame_anterior

    running = True
    inicio_tempo = pygame.time.get_ticks()
    indice_gif_atual = 0

    while running:
        ret, frame_atual = cap.read()
        if not ret:
            print("Falha ao ler frame da webcam.")
            break

        if detectar_movimento(frame_anterior, frame_atual):
            print("Movimento Detectado!")

        frame_anterior = frame_atual.copy()  # Atualizando o frame anterior

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - inicio_tempo > TEMPO_DE_EXIBICAO:
            inicio_tempo = tempo_atual
            indice_gif_atual = (indice_gif_atual + 1) % len(gifs)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Limpa a tela
        exibir_gif(indice_gif_atual)  # Exibe o GIF atual
        exibir_camera(frame_atual)  # Exibir o feed da câmera

        pygame.display.update()

    pygame.quit()
    cap.release()

# Executar o jogo
jogo()
