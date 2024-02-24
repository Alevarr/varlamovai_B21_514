from PIL import Image
import os

def resize_image(image_path, output_path, scale_factor):
    print('Начало интерполяции...')

    image = Image.open(image_path)

    if image.format.lower() not in ['bmp', 'png']:
        raise ValueError("Изображение должно быть в формате BMP или PNG.")

    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    new_image = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            old_x = int(x / scale_factor)
            old_y = int(y / scale_factor)
            pixel = image.getpixel((old_x, old_y))
            new_image.putpixel((x, y), pixel)

    new_image.save(output_path)
    print('Интерполяция завершена.')

def compress_image(image_path, output_path, scale_factor):
    print('Начало децимации...')
    image = Image.open(image_path)

    if image.format.lower() not in ['bmp', 'png']:
        raise ValueError("Изображение должно быть в формате BMP или PNG.")

    width, height = image.size
    new_width = int(width / scale_factor)
    new_height = int(height / scale_factor)
    new_image = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            new_x = x * scale_factor
            new_y = y * scale_factor
            pixel = image.getpixel((new_x, new_y))
            new_image.putpixel((x, y), pixel)

    new_image.save(output_path)
    print('Децимация завершена.')

def resize_and_compress(image_path, output_path, scale_factor_resize, scale_factor_compress):
    print("Начало передескретизации в 2 прохода...")
    temp_path = "temp_resized.png"
    resize_image(image_path, temp_path, scale_factor_resize)

    # Сжатие
    compress_image(temp_path, output_path, scale_factor_compress)

    if os.path.exists(temp_path):
        os.remove(temp_path)
    print("Передескретизации в 2 прохода завершена...")

resize_and_compress("../input/meme.png", "output/meme.png", 3, 4)
