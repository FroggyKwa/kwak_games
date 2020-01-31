from PIL import Image
from source.functions.bitmasks import get_bitmask
# example:
# filename = 'resources\warped city files\SPRITES\player\hurt\hurt.png'


'''
m1 = get_bitmask(-15, -15, (100, 100), filename)
m2 = get_bitmask(4, -15, (100, 100), filename)
print(*m1, sep='\n')
print('----------------------------------')
print('----------------------------------')
print('----------------------------------')
print(*m2, sep='\n')
'''


def collide_mask(mask1, mask2):
    for i in range(len(mask1)):
        for j in range(len(mask1[i])):
            mask1[i][j] += mask2[i][j]
    for i in range(len(mask1)):
        for j in range(len(mask1[i])):
            if mask1[i][j] > 1:
                return True
    return False


# print(collide_mask(m1, m2))
