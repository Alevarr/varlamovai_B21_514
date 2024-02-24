from PIL import Image

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

compress_image("../input/meme.png", "output/meme.png", 2)