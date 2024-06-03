import numpy as np
from numpy import log


def haralik(img_arr, d=2):
    matrix = np.zeros(shape=(256, 256))

    for x in range(d, img_arr.shape[0] - d):
        for y in range(d, img_arr.shape[1] - d):
            matrix[img_arr[x - d, y], img_arr[x, y]] += 1
            matrix[img_arr[x + d, y], img_arr[x, y]] += 1
            matrix[img_arr[x, y - d], img_arr[x, y]] += 1
            matrix[img_arr[x, y + d], img_arr[x, y]] += 1

    for x in range(256):
        m = np.array(matrix[x])
        m[np.where(m == 0)] = 1
        matrix[x] = log(m)

    matrix = matrix * 256 / np.max(matrix)
    return matrix


def AV(matrix):

    normalized_matrix = matrix / np.sum(matrix)
    av = np.sum(np.square(normalized_matrix))
    return av


def D(matrix):

    d = np.sum(matrix / (1 + np.square(np.arange(matrix.shape[0]))))
    return d