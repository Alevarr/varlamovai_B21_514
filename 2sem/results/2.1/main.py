from PIL import Image
import numpy as np

def convert_to_grayscale(image_path, output_path = None):
    print("Приведение изображения к полутону...")
    img = Image.open(image_path)

    if img.format.lower() not in ['bmp', 'png']:
        raise ValueError("Изображение должно быть в формате BMP или PNG.")

    grayscale_img = Image.new("L", img.size)
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            grayscale_img.putpixel((x, y), gray)


    if output_path:
        grayscale_img.save(output_path)
    print("Приведенеи изображения к полутону завершено.")
    return grayscale_img

def balanced_threshold(image_path, output_path):

    img = convert_to_grayscale(image_path)

    print("Начало бинаризации...")

    img_array = np.array(img)

    histogram = np.histogram(img_array, bins=256, range=(0, 256))

    threshold = np.mean(histogram[1][:-1])

    binary_img_array = np.where(img_array > threshold, 255, 0)

    binary_img = Image.fromarray(binary_img_array.astype(np.uint8))

    binary_img.save(output_path)
    print("Бинаризация завершена.")

balanced_threshold("../input/1200px-Chest_Xray_PA_3-8-2010.bmp", "output/1200px-Chest_Xray_PA_3-8-2010.bmp")
balanced_threshold("../input/movie.bmp", "output/movie.bmp")
balanced_threshold("../input/photo_2023-07-02_20-07-31.png", "output/photo_2023-07-02_20-07-31.bmp")
balanced_threshold("../input/photo_2024-01-01_00-43-47.png", "output/photo_2024-01-01_00-43-47.bmp")
balanced_threshold("../input/png-transparent-world-map-globe-outline-maps-globe-border-miscellaneous-globe.bmp", "output/png-transparent-world-map-globe-outline-maps-globe-border-miscellaneous-globe.bmp")

