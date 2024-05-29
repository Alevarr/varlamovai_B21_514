import matplotlib.pyplot as plt
import string
import os

import numpy as np
from PIL import Image, ImageOps

# Define the letters for the Spanish alphabet including ñ
spanish_alphabet = list(string.ascii_lowercase) + ['ñ']

# Create a directory to store the images if it doesn't exist
output_dir = "output"
inverse_output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def convert_to_grayscale(image_path, output_path = None):
    # print("Приведение изображения к полутону...")
    img = Image.open(image_path).convert('RGB')

    grayscale_img = Image.new("L", img.size)
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            grayscale_img.putpixel((x, y), gray)


    if output_path:
        grayscale_img.save(output_path)
    # print("Приведенеи изображения к полутону завершено.")
    return grayscale_img

def balanced_threshold(image_path, output_path):

    img = convert_to_grayscale(image_path)

    # print("Начало бинаризации...")

    img_array = np.array(img)

    histogram = np.histogram(img_array, bins=256, range=(0, 256))

    threshold = np.mean(histogram[1][:-1])

    binary_img_array = np.where(img_array > threshold, 255, 0)

    binary_img = Image.fromarray(binary_img_array.astype(np.uint8))

    binary_img.save(output_path)
    print("Бинаризация завершена.")

def save_inverted_image(image_path, output_path):
    image = Image.open(image_path)
    inverted_image = ImageOps.invert(image.convert("RGB"))
    inverted_image.save(output_path)

balanced_threshold("input/smallerfont.bmp", f"{output_dir}/smallerfont.bmp")
save_inverted_image(f"{output_dir}/smallerfont.bmp", f"{inverse_output_dir}/smallerfont_inverse.bmp")
