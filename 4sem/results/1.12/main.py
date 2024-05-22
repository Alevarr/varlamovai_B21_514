import numpy as np
from PIL import Image, ImageChops, ImageFilter

def convert_to_grayscale(image_path):
    image = Image.open(image_path)
    rgb_image = image.convert('RGB')
    print("Приведение изображения к полутону завершено.")
    return rgb_image.convert('L')

def apply_blackhat_morphology(gray_image, kernel_size=(5, 5)):
    dilated = gray_image.filter(ImageFilter.MaxFilter(kernel_size[0]))
    closed = dilated.filter(ImageFilter.MinFilter(kernel_size[0]))
    blackhat = ImageChops.subtract(closed, gray_image)
    print("Черное морфологическое расширение выполнено.")
    return blackhat

def binarize_image(image, threshold_value=128):
    threshold = image.point(lambda p: p > threshold_value and 255)
    print("Бинаризация завершена.")
    return threshold.convert('1')

def run(image_path, bin_threshold, grayscale_output_path, blackhat_output_path, binary_output_path):
    grayscale = convert_to_grayscale(image_path)
    blackhat = apply_blackhat_morphology(grayscale)
    binary = binarize_image(blackhat, bin_threshold)
    grayscale.save(grayscale_output_path)
    blackhat.save(blackhat_output_path)
    binary.save(binary_output_path)

run("../input/img.png", 64, "output/g_rickandmorty.png", "output/bl_rickandmorty.png", "output/bi_rickandmorty.png")
run("../input/img_1.png", 64, "output/g_textbook.png", "output/bl_textbook.png", "output/bi_textbook.png")
run("../input/img_2.png", 8, "output/g_hasbik.png", "output/bl_hasbik.png", "output/bi_hasbik.png")