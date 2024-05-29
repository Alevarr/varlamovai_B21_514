# import numpy as np
# from matplotlib import pyplot as plt
# from PIL import Image
#
# def get_profiles(img):
#     return {
#         'x': {
#             'y': np.sum(img, axis=0),
#             'x': np.arange(
#                 start=1, stop=img.shape[1] + 1).astype(int)
#         },
#         'y': {
#             'y': np.arange(
#                 start=1, stop=img.shape[0] + 1).astype(int),
#             'x': np.sum(img, axis=1)
#         }
#     }
#
#
# def write_profile(img, output_name, type='x'):
#     profiles = get_profiles(img)
#
#     if type == 'x':
#         plt.bar(x=profiles['x']['x'], height=profiles['x']['y'], width=0.9)
#
#         plt.ylim(0, 52)
#
#     elif type == 'y':
#         plt.barh(y=profiles['y']['y'], width=profiles['y']['x'], height=0.9)
#
#         plt.ylim(52, 0)
#
#     else:
#         raise Exception('Unsupported profile')
#
#     plt.xlim(0, 55)
#
#     plt.savefig(f'output/{type}/{output_name}.png')
#     plt.clf()
#
#
# if __name__ == '__main__':
#     method_prefix = 'Image_Profiles'
#
#
#     img_src = Image.open(f'../1/output/Screenshot.bmp').convert('L')
#     img_src_arr = np.array(img_src)
#
#     img_src_arr[img_src_arr == 0] = 1
#     img_src_arr[img_src_arr == 255] = 0
#
#     write_profile(img_src_arr, "profile", type='x')
#     write_profile(img_src_arr, "profile", type='y')

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def calculate_profile(img: np.array, axis: int) -> np.array:
    print(img)
    return np.sum(img, axis=1 - axis)

def bar(data, bins, axis):
    if axis == 1:
        plt.bar(x=bins, height=data)

    elif axis == 0:
        plt.barh(y=bins, width=data)

    else:
        raise ValueError('Invalid axis')



img = np.array(Image.open("../1/output/Screenshot_inverse.bmp").convert("L"))

profile_x = calculate_profile(img, 0)
profile_y = calculate_profile(img, 1)
bins_x = np.arange(start=1, stop=img.shape[0] + 1).astype(int)
bins_y = np.arange(start=1, stop=img.shape[1] + 1).astype(int)

bar(profile_x / 255, bins_x, 0)
plt.savefig("output/profile_x.png")
plt.clf()

bar(profile_y / 255, bins_y, 1)
plt.savefig("output/profile_y.png")
plt.clf()