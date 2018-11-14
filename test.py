file = open('puppy.txt')

lines = file.read().split('\n')
if not lines[0]:
    print('no pup')