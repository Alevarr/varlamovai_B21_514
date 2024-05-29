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
            # letter_profile = calculate_profile(letter, axis)
            # letter, _ = cut_black(letter, letter_profile, axis)
            letter_img = Image.fromarray(letter.astype(np.uint8), 'L').convert('1')

            letter_img.save(f"output/characters/{i}.png")

        # letter_img = invert(letter_img)
        # letter_img.save(f"results/symbols/letter_{i}.png")