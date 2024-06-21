import numpy as np
from scipy.ndimage import convolve
import dis

def mean_filter(image, kernel_size = 3):
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    
    blurred_image = convolve(image, kernel)
    
    return blurred_image


print(list(dis.get_instructions(mean_filter)))
