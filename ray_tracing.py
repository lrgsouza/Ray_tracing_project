import os
import numpy as np
import matplotlib.pyplot as plt
import time

from tqdm import tqdm


# marca o tempo de início
inicio = time.time()

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


def frame_framerender(width, height, max_depth, camera, screen, objects, image, frame_rate):

    ini_rng = int(0 - (frame_rate/2))
    end_rng = int(0 + (frame_rate/2) + 1)
    img_number = 0
    #loop para renderizar frame com nova posição do sol(luz)
    for position in range(ini_rng, end_rng, 1):
        
        #define x e y da luz
        y = 5
        x = position

        light = {'position': np.array([x, y, 5]), 'ambient': np.array(
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
            
        plt.imsave(F'frames/image{img_number}.png', image)
        print(F'Imagem gerada: image{img_number}.png\n')

        img_number = img_number + 1


def generate_gif():

    import os
    from PIL import Image
    # caminho para a pasta contendo os arquivos
    caminho_pasta = "./frames"

    # lista os arquivos na pasta e cria uma lista com os nomes
    arquivos = os.listdir(caminho_pasta)

    # abra cada arquivo PNG
    imagens = [Image.open(f'./frames/{nome_arquivo}')
               for nome_arquivo in arquivos]

    # salve as imagens em um arquivo GIF
    imagens[0].save('animacao.gif',
                    save_all=True,
                    append_images=imagens[1:],
                    duration=100,
                    loop=0)


#define largura e altura da cena
width = 900
height = 600
max_depth = 3

#define posição da camera
camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

#definindo as esferas da cena
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

# DEFINE QUANTOS FRAMES QUEREMOS RENDERIZAR
frame_rate = 10

# CHAMA FUNÇÃO PRINCIPAL
frame_framerender(width, height, max_depth, camera,
                  screen, objects, image, frame_rate)


#gerando GIF animado
generate_gif()

# marca o tempo de fim
fim = time.time()
# calcula o tempo total de execução
tempo_total = fim - inicio
if(tempo_total>300):
    print(f"O tempo total foi de: {tempo_total/60} minutos")
else:
    print(f"O tempo total foi de: {tempo_total} segundos")
