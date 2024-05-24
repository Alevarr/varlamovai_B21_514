import matplotlib.pyplot as plt
import string
import os

import numpy as np
from PIL import Image, ImageOps

# Define the letters for the Spanish alphabet including ñ
spanish_alphabet = list(string.ascii_lowercase) + ['ñ']

# Create a directory to store the images if it doesn't exist
output_dir = "spanish_lowercase_letters"
inverse_output_dir = "inverse_spanish_lowercase_letters"
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

# Function to create and save an image of a letter
def create_letter_image(letter, fontname='Times New Roman', fontsize=52):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, letter, fontsize=fontsize, ha='center', va='center', fontname=fontname)
    ax.axis('off')
    fig.canvas.draw()
    bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(f"{output_dir}/{letter}.png", bbox_inches=bbox, pad_inches=0, transparent=True)
    plt.close(fig)


# Function to crop whitespace from an image and add a white background
def crop_whitespace(image_path):
    image = Image.open(image_path).convert("RGBA")
    image.load()
    image_data = image.getdata()

    # Get the bounding box of the non-white areas in the image
    bbox = image.getbbox()
    # Crop the image to the bounding box
    if bbox:
        cropped_image = image.crop(bbox)
        # Create a white background
        white_bg = Image.new("RGBA", cropped_image.size, "WHITE")
        white_bg.paste(cropped_image, (0, 0), cropped_image)
        white_bg = white_bg.convert("RGB")  # Remove alpha for white background
        white_bg.save(image_path)
    print("Обрезание завершено.")

def save_inverted_image(image_path, output_path):
    image = Image.open(image_path)
    inverted_image = ImageOps.invert(image.convert("RGB"))
    inverted_image.save(output_path)

# Generate and crop images for all letters
for letter in spanish_alphabet:
    create_letter_image(letter)
    crop_whitespace(f"{output_dir}/{letter}.png")
    balanced_threshold(f"{output_dir}/{letter}.png", f"{output_dir}/{letter}.png")
    save_inverted_image(f"{output_dir}/{letter}.png", f"{inverse_output_dir}/{letter}.png")
