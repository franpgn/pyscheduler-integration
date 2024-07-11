import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve
import sys
import os
from apps.src.disassemble import disassemble

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def mean_filter():
    image = np.array([[10, 10, 10, 10, 10],
                      [10, 50, 50, 50, 10],
                      [10, 50, 100, 50, 10],
                      [10, 50, 50, 50, 10],
                      [10, 10, 10, 10, 10]])

    kernel = np.array([[0.11111111, 0.11111111, 0.11111111],
                       [0.11111111, 0.11111111, 0.11111111],
                       [0.11111111, 0.11111111, 0.11111111]])

    blurred_image = convolve(image, kernel)
    
    return blurred_image


def to_byte_code():
    disassemble(mean_filter.__code__)

    #Test
    image = np.array([[10, 10, 10, 10, 10],
                      [10, 50, 50, 50, 10],
                      [10, 50, 100, 50, 10],
                      [10, 50, 50, 50, 10],
                      [10, 10, 10, 10, 10]])
    filtered_image = mean_filter()
    print(filtered_image)
    plt.figure(figsize=(10, 5))
    # View
    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Mean Filter')
    plt.imshow(filtered_image, cmap='gray')
    plt.axis('off')

    plt.show()
