from PIL import Image
from source.get_platforms import get_platforms
import pytmx, pygame

def get_bitmask(x, y, window_size, file, chromokey=None):
    img = Image.open(file) if file is str else file
    pixels = img.load()  # список с пикселями
    w, h = img.size  # ширина (x) и высота (y) изображения
    print(w, h)

    if chromokey is None:
        chromokey = pixels[0, 0]
    mask = [[0 for i in range(window_size[0])] for j in range(window_size[1])]
    for i in range(w):
        for j in range(h):
            try:
                if j + y < 0 or i + x < 0:
                    continue
                mask[j + y][i + x] = 0 if pixels[i, j] == chromokey else 1
            except IndexError:
                continue
    img.close()
    return mask


def get_platforms_bitmask(filename, window_size):
    sur = get_platforms(filename)
    pil_string_image = pygame.image.tostring(sur, "RGBA",False)
    pil_image = Image.frombytes("RGBA", (sur.get_width(), sur.get_height()), pil_string_image)
    return get_bitmask(0, 0, window_size, pil_image)

#print(get_platforms_bitmask('C:/Users/User/PycharmProjects/kwak_games/source/resources/maps/map.tmx'))