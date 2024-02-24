from PIL import Image


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


resize_image("../input/meme.png", "output/meme.png", 2)



