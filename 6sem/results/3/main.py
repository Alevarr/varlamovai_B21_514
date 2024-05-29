import numpy as np
from PIL import Image, ImageDraw


def calculate_profile(img: np.array, axis: int) -> np.array:
    return np.sum(img, axis=1 - axis)

def split_letters(img: np.array, profile: np.array):
    letters = []
    letter_borders = []
    letter_start = 0
    is_empty = True

    for i in range(img.shape[1]):
        if profile[i] == 0:
            if not is_empty:
                is_empty = True
                letters.append(img[:, letter_start:i + 1])
                letter_borders.append(i+1)

        else:
            if is_empty:
                is_empty = False
                letter_start = i
                letter_borders.append(letter_start)

    letters.append(img[:, letter_start:img.shape[1] - 1])

    return letters, letter_borders

def crop(image_path):
    img = Image.open(image_path).convert('L')

    # Преобразовать изображение в массив numpy
    img_arr = np.array(img)

    # Найти индексы строк и столбцов, содержащих нечерные пиксели
    non_black_columns = np.where(np.any(img_arr != 0, axis=0))[0]
    non_black_rows = np.where(np.any(img_arr != 0, axis=1))[0]

    # Найти границы обрезки
    left, right = non_black_columns[0], non_black_columns[-1]
    top, bottom = non_black_rows[0], non_black_rows[-1]

    # Обрезать изображение
    cropped_img = img.crop((left, top, right + 1, bottom + 1))

    # Сохранить обрезанное изображение
    cropped_img.save(image_path)

img = np.array(Image.open("../1/output/Screenshot_inverse.bmp").convert("L"))
profile_y = calculate_profile(img, 1)
img_letters, letter_borders = split_letters(img, profile_y)

result_img = Image.fromarray(img.astype(np.uint8), 'L')
rgb_img = Image.new("RGB", result_img.size)
rgb_img.paste(result_img)
draw = ImageDraw.Draw(rgb_img)

for border in letter_borders:
    draw.line((border, 0, border, img.shape[1]), fill='green')

rgb_img.save(f"output/result.png")

for i, letter in enumerate(img_letters):
        for axis in (0, 1):
            letter_img = Image.fromarray(letter.astype(np.uint8), 'L').convert('1')

            letter_img.save(f"output/characters/{i}.png")
            crop(f"output/characters/{i}.png")

