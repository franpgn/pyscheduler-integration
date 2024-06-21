import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve
from disassemble import disassemble

def mean_filter(image, kernel_size = 3):
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
filtered_image = mean_filter(image)
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