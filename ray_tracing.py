import numpy as np
import matplotlib.pyplot as plt
import time

from utils import *

from tqdm import tqdm

# marca o tempo de início
inicio = time.time()

def frame_framerender(width, height, max_depth, camera, screen, objects, image):
    img_number = 0
    
    x_arr = [-5, -4.5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 4.5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -4.5]
    z_arr = [0, 1.5, 3, 4, 4.5, 5, 5, 5, 4.5, 4, 3, 1.5, 0, -3, -4, -4.5, -5, -5, -5, -4.5, -4, -3, -1.5]

    #loop para renderizar frame com nova posição do sol(luz)
    for position in range(0, len(x_arr), 1):
        
        #define x e y da luz
        y = 3
        x = x_arr[position]
        z = z_arr[position]

        light = {'position': np.array([x, y, z]), 'ambient': np.array(
            [1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1])}

        # loop principal para gerar render
        for i, y in enumerate(tqdm(np.linspace(screen[1], screen[3], height), colour = 'blue', desc ="Renderizando frame "+str(img_number+1)+": ")):
            for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
                # screen is on origin
                pixel = np.array([x, y, 0])
                origin = camera
                direction = normalize(pixel - origin)

                color = np.zeros((3))
                reflection = 1

                for k in range(max_depth):
                    # check for intersections
                    nearest_object, min_distance = nearest_intersected_object(
                        objects, origin, direction)
                    if nearest_object is None:
                        break

                    intersection = origin + min_distance * direction
                    normal_to_surface = normalize(
                        intersection - nearest_object['center'])
                    shifted_point = intersection + 1e-5 * normal_to_surface
                    intersection_to_light = normalize(
                        light['position'] - shifted_point)

                    _, min_distance = nearest_intersected_object(
                        objects, shifted_point, intersection_to_light)
                    intersection_to_light_distance = np.linalg.norm(
                        light['position'] - intersection)
                    is_shadowed = min_distance < intersection_to_light_distance

                    if is_shadowed:
                        break

                    illumination = np.zeros((3))

                    # ambiant
                    illumination += nearest_object['ambient'] * light['ambient']

                    # diffuse
                    illumination += nearest_object['diffuse'] * light['diffuse'] * \
                        np.dot(intersection_to_light, normal_to_surface)

                    # specular
                    intersection_to_camera = normalize(camera - intersection)
                    H = normalize(intersection_to_light + intersection_to_camera)
                    illumination += nearest_object['specular'] * light['specular'] * np.dot(
                        normal_to_surface, H) ** (nearest_object['shininess'] / 4)

                    # reflection
                    color += reflection * illumination
                    reflection *= nearest_object['reflection']

                    origin = shifted_point
                    direction = reflected(direction, normal_to_surface)

                image[i, j] = np.clip(color, 0, 1)
            
        if(img_number < 10):
            print(F'Imagem gerada: image0{img_number}.png\n')
            plt.imsave(F'frames/image0{img_number}.png', image)
        else:
            print(F'Imagem gerada: image{img_number}.png\n')
            plt.imsave(F'frames/image{img_number}.png', image)

        img_number = img_number + 1


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
