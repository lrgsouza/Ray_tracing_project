
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils import *

def frame_framerender(width, height, max_depth, camera, screen, objects, image):

    x_arr = [-5, -4.5, -4, -3, -2, -1, 0, 1, 2, 3, 4,
             5, 4.5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -4.5]
    z_arr = [0, 1.5, 3, 4, 4.5, 5, 5, 5, 4.5, 4, 3, 1.5,
             0, -3, -4, -4.5, -5, -5, -5, -4.5, -4, -3, -1.5]

    # loop para renderizar frame com nova posição do sol(luz)
    for position in range(0, len(x_arr), 1):
        img_number = position
        # define x e y da luz
        y = 3
        x = x_arr[position]
        z = z_arr[position]

        light = {'position': np.array([x, y, z]), 'ambient': np.array(
            [1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1])}

        # loop principal para gerar render
        for i, y in enumerate(tqdm(np.linspace(screen[1], screen[3], height), colour='blue', desc="Renderizando frame "+str(img_number+1)+": ")):
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
                    illumination += nearest_object['ambient'] * \
                        light['ambient']

                    # diffuse
                    illumination += nearest_object['diffuse'] * light['diffuse'] * \
                        np.dot(intersection_to_light, normal_to_surface)

                    # specular
                    intersection_to_camera = normalize(camera - intersection)
                    H = normalize(intersection_to_light +
                                  intersection_to_camera)
                    illumination += nearest_object['specular'] * light['specular'] * np.dot(
                        normal_to_surface, H) ** (nearest_object['shininess'] / 4)

                    # reflection
                    color += reflection * illumination
                    reflection *= nearest_object['reflection']

                    origin = shifted_point
                    direction = reflected(direction, normal_to_surface)

                image[i, j] = np.clip(color, 0, 1)

        if (img_number < 10):
            print(F'Imagem gerada: image0{img_number}.png\n')
            plt.imsave(F'frames/image0{img_number}.png', image)
        else:
            print(F'Imagem gerada: image{img_number}.png\n')
            plt.imsave(F'frames/image{img_number}.png', image)
