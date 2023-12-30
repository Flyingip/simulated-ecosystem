import numpy as np
from opensimplex import OpenSimplex
import random
import pygame
from PIL import Image
import matplotlib.pyplot as plt


def berlin_block(shape, scale, block_size=50):
    seed = random.randint(0, 1000)
    noise_gen = OpenSimplex(seed)
    x, y = shape
    result = np.zeros(shape)

    for i in range(0, x, block_size):
        for j in range(0, y, block_size):
            block = np.vectorize(noise_gen.noise2)(
                (i + np.arange(block_size))[:, None] / scale,
                (j + np.arange(block_size)) / scale,
            )
            block_shape = block.shape
            result[i : i + block_shape[0], j : j + block_shape[1]] = block

    return (result + 1) / 2


# 使用示例
noise_grid = berlin_block((800, 800), scale=800, block_size=50)
print(noise_grid)
image = Image.fromarray(np.uint8(plt.cm.viridis(noise_grid) * 255))

# Save the image
image_file_path = "1.png"
image.save(image_file_path)
