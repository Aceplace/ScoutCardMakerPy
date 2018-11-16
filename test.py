import pickle
import traceback

try:
    open('nonexistent.txt','r')
except Exception as e:
    print('puppy')
    traceback.print_exc()
