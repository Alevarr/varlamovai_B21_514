import os

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def load_image(image_path):
    image = Image.open(image_path).convert('L')
    return np.array(image)


def glcm_matrix(image, distance, angle):
    rows, cols = image.shape
    glcm = np.zeros((256, 256), dtype=int)

    if angle == 0:
        offset = (0, distance)
    elif angle == 45:
        offset = (-distance, distance)
    elif angle == 90:
        offset = (-distance, 0)
    elif angle == 135:
        offset = (-distance, -distance)
    elif angle == 180:
        offset = (0, -distance)
    elif angle == 225:
        offset = (distance, -distance)
    elif angle == 270:
        offset = (distance, 0)
    elif angle == 315:
        offset = (distance, distance)

    for i in range(rows):
        for j in range(cols):
            if 0 <= i + offset[0] < rows and 0 <= j + offset[1] < cols:
                pixel_value = image[i, j]
                neighbor_value = image[i + offset[0], j + offset[1]]
                glcm[pixel_value, neighbor_value] += 1

    return glcm


def calculate_features(glcm):
    total_pairs = np.sum(glcm)
    av = np.mean(glcm)
    d = np.max(glcm) - np.min(glcm)
    return av, d

image_path = '../input/wallpaper.png'
image = load_image(image_path)

# Получение базового имени файла без пути и расширения
base_filename = os.path.splitext(os.path.basename(image_path))[0]

# Сохранение grayscale версии исходного изображения
grayscale_image_filename = f'output/{base_filename}_grayscale.png'
grayscale_image_pil = Image.fromarray(image)
grayscale_image_pil.save(grayscale_image_filename)

distance = 2
angles = [45, 135, 225, 315]

glcm_total = np.zeros((256, 256), dtype=int)
for angle in angles:
    glcm = glcm_matrix(image, distance, angle)
    glcm_total += glcm

glcm_normalized = glcm_total / glcm_total.sum()

av, d = calculate_features(glcm_normalized)



features_filename = f'output/{base_filename}_features.txt'
with open(features_filename, 'w') as f:
    f.write(f"Average Value (AV): {av}\n")
    f.write(f"Difference (D): {d}\n")

visualization_filename = f'output/{base_filename}_haralick.png'
plt.figure(figsize=(10, 8))
plt.title('GLCM')
plt.imshow(glcm_total, cmap='gray', vmin=0, vmax=glcm_total.max())
plt.colorbar()
plt.savefig(visualization_filename)
plt.close()


def power_transform(image, gamma):
    norm_image = image / 255.0
    transformed_image = np.power(norm_image, gamma)
    transformed_image = (transformed_image * 255).astype(np.uint8)
    return transformed_image

gamma = 2.0
transformed_image = power_transform(image, gamma)
transformed_image_filename = f'output/{base_filename}_transformed.png'
transformed_image_pil = Image.fromarray(transformed_image)
transformed_image_pil.save(transformed_image_filename)


glcm_total_transformed = np.zeros((256, 256), dtype=int)
for angle in angles:
    glcm = glcm_matrix(transformed_image, distance, angle)
    glcm_total_transformed += glcm


av_transformed, d_transformed = calculate_features(glcm_total_transformed)


features_filename_transformed = f'output/{base_filename}_features_transformed.txt'
with open(features_filename_transformed, 'w') as f:
    f.write(f"Average Value (AV): {av_transformed}\n")
    f.write(f"Difference (D): {d_transformed}\n")


visualization_filename_transformed = f'output/{base_filename}_haralick_transformed.png'
plt.figure(figsize=(10, 8))
plt.title('GLCM Transformed')
plt.imshow(glcm_total_transformed, cmap='gray', vmin=0, vmax=glcm_total_transformed.max())
plt.colorbar()
plt.savefig(visualization_filename_transformed)
plt.close()
