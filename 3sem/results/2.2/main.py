import cv2
import numpy as np
from PIL import Image

def conservative_smooth(input_path, output_path, kernel_size=7):
    # Загрузка изображения с помощью PIL
    image = Image.open(input_path)

    # Преобразование изображения PIL в массив NumPy
    image_np = np.array(image)

    # Проверка, является ли изображение черно-белым
    if len(image_np.shape) == 3:
        # Преобразование в черно-белое изображение, если это цветное
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    if kernel_size % 2 == 0:
        kernel_size += 1
    half_kernel = kernel_size // 2
    smoothed_image = np.zeros_like(image_np)
    for y in range(half_kernel, image_np.shape[0] - half_kernel):
        for x in range(half_kernel, image_np.shape[1] - half_kernel):
            neighborhood = image_np[y - half_kernel:y + half_kernel + 1, x - half_kernel:x + half_kernel + 1]
            avg = np.mean(neighborhood)
            if image_np[y, x] > avg:
                smoothed_image[y, x] = image_np[y, x]
            else:
                smoothed_image[y, x] = avg

        # Вычисление разностного изображения
        diff_image = np.abs(image_np - smoothed_image)

        # Преобразование обратно в изображение PIL для сохранения
        diff_image_pil = Image.fromarray(diff_image)

        # Сохранение разностного изображения в монохромном режиме
        diff_image_pil.convert('L').save(output_path)


conservative_smooth("../input/Screenshot_408.png", "output/Screenshot_408.png")
conservative_smooth("../input/Screenshot_409.png", "output/Screenshot_409.png")
conservative_smooth("../input/Screenshot_4081.png", "output/Screenshot_4081.png")
