from enum import Enum

class puppy(Enum):
    kitty = 'kitty'
    cat = 'kat'
    crunch = 'crunch'

yoyo = puppy.kitty


if yoyo == 'kitty':
    print('puppy')