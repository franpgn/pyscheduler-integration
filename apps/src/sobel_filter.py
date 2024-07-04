import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from apps.src.disassemble import disassemble

def sobel_filter():
    image = np.array([[10, 10, 10, 10, 10],
                      [10, 50, 50, 50, 10],
                      [10, 50, 100, 50, 10],
                      [10, 50, 50, 50, 10],
                      [10, 10, 10, 10, 10]])

    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

    Ky = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]])

    Ix = convolve(image, Kx)
    Iy = convolve(image, Ky)

    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    return G

if __name__ == "__main__":
    disassemble(sobel_filter.__code__)

    # Test
    image = np.array([[10, 10, 10, 10, 10],
                      [10, 50, 50, 50, 10],
                      [10, 50, 100, 50, 10],
                      [10, 50, 50, 50, 10],
                      [10, 10, 10, 10, 10]])
    filtered_image = sobel_filter()
    print(filtered_image)
    # View
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Sobel Filter')
    plt.imshow(filtered_image, cmap='gray')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Sobel Filter')
    plt.imshow(filtered_image, cmap='gray')
    plt.axis('off')

    plt.show()
    plt.show()

