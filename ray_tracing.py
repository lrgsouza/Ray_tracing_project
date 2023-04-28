import numpy as np
import matplotlib.pyplot as plt
import time
from utils import *
from tqdm import tqdm
from render import frame_framerender

# marca o tempo de início
inicio = time.time()

#define largura e altura da cena
width = 90
height = 60
max_depth = 3

#define posição da camera
camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

#definindo as esferas da cena

# center = ponto central da esfera
# radius = raio da esfera
# ambient, diffuse, specular, shininess & reflection = caracteristicas do material
objects = [
    {'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array(
        [0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array(
        [0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array(
        [0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]),
     'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5}
]

# cria uma imagem de tamanho height x width com 3 páginas
image = np.zeros((height, width, 3))

# limpa todos os arquivos da pasta "frames"
clean_path("frames")

# CHAMA FUNÇÃO PRINCIPAL
frame_framerender(width, height, max_depth, camera,
                  screen, objects, image)


#gerando GIF animado
gif_name = f"./gifs/circle_animation_{width}x{height}.gif"
generate_gif(gif_name)

# marca o tempo de fim
fim = time.time()
# calcula o tempo total de execução
tempo_total = fim - inicio
if(tempo_total>300):
    print(f"O tempo total foi de: {tempo_total/60} minutos")
else:
    print(f"O tempo total foi de: {tempo_total} segundos")
