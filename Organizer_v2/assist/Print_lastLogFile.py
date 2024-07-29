import pickle
import os


file = os.listdir('../logs')[-1]

with open(f'../logs/{file}', 'rb') as file:
    print(pickle.load(file))