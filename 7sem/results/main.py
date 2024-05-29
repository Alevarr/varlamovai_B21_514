from PIL import Image
import csv
import numpy as np
from math import sqrt

def get_profiles(img):
    return {
        'x': {
            'y': np.sum(img, axis=0),
            'x': np.arange(
                start=1, stop=img.shape[1] + 1).astype(int)
        },
        'y': {
            'y': np.arange(
                start=1, stop=img.shape[0] + 1).astype(int),
            'x': np.sum(img, axis=1)
        }
    }

def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def last_nonzero(arr, axis, invalid_val=-1):
    mask = arr != 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def calculate_features(img):
    img_b = np.zeros(shape=img.shape)
    img_b[img != 255] = 1

    profiles = get_profiles(img_b)

    img_b = img_b[first_nonzero(profiles['y']['x'], 0): last_nonzero(
        profiles['y']['x'], 0) + 1, first_nonzero(profiles['x']['y'], 0): last_nonzero(profiles['x']['y'], 0) + 1]

    weight = img_b.sum()
    rel_weight = weight / (img_b.shape[0] * img_b.shape[1])

    x_avg = 0
    for x, column in enumerate(img_b.T):
        x_avg += sum((x + 1) * column)
    x_avg = x_avg/weight
    rel_x_avg = (x_avg-1)/(img_b.shape[1]-1)

    y_avg = 0
    for y, row in enumerate(img_b):
        y_avg += sum((y + 1) * row)
    y_avg = y_avg/weight
    rel_y_avg = (y_avg-1)/(img_b.shape[0]-1)

    iner_x = 0
    for y, row in enumerate(img_b):
        iner_x += sum((y + 1 - y_avg)**2 * row)
    rel_iner_x = iner_x/(img_b.shape[0]**2 + img_b.shape[1]**2)

    iner_y = 0
    for x, column in enumerate(img_b.T):
        iner_y += sum((x + 1 - x_avg)**2 * column)
    rel_iner_y = iner_y/(img_b.shape[0]**2 + img_b.shape[1]**2)

    return {
        'weight': weight,
        'rel_weight': rel_weight,
        'center': (x_avg, y_avg),
        'rel_center': (rel_x_avg, rel_y_avg),
        'inertia': (iner_x, iner_y),
        'rel_inertia': (rel_iner_x, rel_iner_y)
    }

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

def load_features():
    with open('../../5sem/results/data.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        result = {}
        for row in reader:
            result[row['letter']] = {
                'rel_weight': float(row['rel_weight']),
                'rel_center': tuple(map(float, row['rel_center'][1:len(row['rel_center'])-1].split(', '))),
                'rel_inertia': tuple(map(float, row['rel_inertia'][1:len(row['rel_inertia'])-1].split(', ')))
            }

        return result

def feature_distance(features_1, features_2):
    return sqrt(
        (features_1['rel_weight'] - features_2['rel_weight'])**2 +
        (features_1['rel_center'][0] - features_2['rel_center'][0])**2 +
        (features_1['rel_center'][1] - features_2['rel_center'][1])**2 +
        (features_1['rel_inertia'][0] - features_2['rel_inertia'][0])**2 +
        (features_1['rel_inertia'][1] - features_2['rel_inertia'][1])**2
    )


def calculate_distance(features_global, features_local):
    result = {}
    for letter, features in features_global.items():
        result[letter] = feature_distance(features_local, features)

    _max = max(result.values())
    new_result = {}
    for letter, distance in result.items():
        new_result[letter] = (_max - distance) / _max

    return new_result

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

def do_stuff(img_path):

    img = np.array(Image.open(img_path).convert("L"))
    profile_y = calculate_profile(img, 1)
    img_letters, letter_borders = split_letters(img, profile_y)
    features_global = load_features()
    file = open("output/data.txt", "w+")

    for i, symbol in enumerate(img_letters):
        letter_img = Image.fromarray(symbol.astype(np.uint8), 'L').convert('1')

        letter_img.save(f"output/characters/{i}.png")
        crop(f"output/characters/{i}.png")
        symbol_img_arr = np.array(Image.open(f"output/characters/{i}.png"))
        features_local = calculate_features(symbol_img_arr)
        grades = calculate_distance(features_global, features_local)

        file.write(
            f"{i + 1}: {dict(sorted(grades.items(), key=lambda item: item[1], reverse=True))}\n")

        letter = max(grades, key=grades.get)
        print(letter, end="")
    print("")

do_stuff("../../6sem/results/1/output/Screenshot_inverse.bmp")
# do_stuff("output/smallerfont_inverse.bmp")