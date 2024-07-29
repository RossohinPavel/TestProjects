import pickle


with open('../data/settings.pcl', 'rb') as file:
    print(pickle.load(file))