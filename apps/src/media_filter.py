import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from apps.src.disassemble import disassemble

def mean_filter():
    image = np.array([[10, 10, 10, 10, 10],
                      [10, 50, 50, 50, 10],
                      [10, 50, 100, 50, 10],
                      [10, 50, 50, 50, 10],
                      [10, 10, 10, 10, 10]])
    kernel_size = 3
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    
    blurred_image = convolve(image, kernel)
    
    return blurred_image


disassemble(mean_filter)

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