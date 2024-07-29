import pickle


with open('../data/library.pcl', 'rb') as file:
    print(pickle.load(file))