from PIL import Image


#example:
#filename = 'resources\warped city files\SPRITES\player\hurt\hurt.png'


def get_bitmask(x, y, window_size, filename, chromokey=None):
    img = Image.open(filename)
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


'''
print(*get_bitmask(-15, -15, (100, 100), filename), sep='\n')
print('----------------------------------')
print('----------------------------------')
print('----------------------------------')
print(*get_bitmask(4, -15, (100, 100), filename), sep='\n')
'''


def collide_mask(x1, y1, filename1,  # координаты 1-ого спрайта, путь к картинке
                 x2, y2, filename2,  # координаты 2-ого спрайта, путь к картинке
                 window_size, chromokey1=None, chromokey2=None):
    mask1 = get_bitmask(x1, y1, window_size, filename1, chromokey1)
    mask2 = get_bitmask(x2, y2, window_size, filename2, chromokey2)
    for i in range(window_size[0]):
        for j in range(window_size[1]):
            mask1[i][j] += mask2[i][j]
    for i in range(window_size[0]):
        for j in range(window_size[1]):
            if mask1[i][j] > 1:
                return True
    return False

#print(collide_mask(14, -15, filename, -15, -15, filename, (100, 100)))
