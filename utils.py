import numpy as np
import matplotlib.pyplot as plt
import time
import os
from PIL import Image

def generate_gif():

    # caminho para a pasta contendo os arquivos
    caminho_pasta = "./frames"

    # lista os arquivos na pasta e cria uma lista com os nomes
    arquivos = sorted(os.listdir(caminho_pasta))

    # abra cada arquivo PNG
    imagens = [Image.open(f'./frames/{nome_arquivo}')
               for nome_arquivo in arquivos]

    # salve as imagens em um arquivo GIF
    imagens[0].save('animacao.gif',
                    save_all=True,
                    append_images=imagens[1:],
                    duration=200,
                    loop=0)
    
def normalize(vector):
    return vector / np.linalg.norm(vector)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis


def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [sphere_intersect(
        obj['center'], obj['radius'], ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance

def clean_path(path):
    # lista todos os arquivos da pasta
    arquivos = os.listdir(path)

    # percorre todos os arquivos e exclui
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(path, arquivo)
        os.remove(caminho_arquivo)

generate_gif()