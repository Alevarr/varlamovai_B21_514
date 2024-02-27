from PIL import Image

def convert_to_grayscale(image_path, output_path):
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


    grayscale_img.save(output_path)
    print("Приведенеи изображения к полутону завершено.")

convert_to_grayscale("../input/84_3.png", "output/84_3.bmp")
