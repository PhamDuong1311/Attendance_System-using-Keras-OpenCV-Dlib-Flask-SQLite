import numpy as np
import os
import json
from sklearn.metrics import f1_score, accuracy_score
#import matplotlib.pyplot as plt
path = 'data'
data = []
for i in sorted(os.listdir(path)):
    with open(os.path.join(path,i), 'r') as file:
        data.append(json.load(file))
vector = np.array([])
name=np.array([])
for i,n in enumerate(data):
    vector_list= json.loads(data[i]['vector'])
    numpy_array = np.array(vector_list)
    
    for j in numpy_array:
        if vector.size == 0:
            vector=j
            name = data[i]['name']
        else:
            vector=np.vstack((vector,j))
            name=np.hstack((name,data[i]['name']))

def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))


distances = []
identical = []

num = len(vector)

for i in range(num - 1):
    for j in range(i + 1, num):
        distances.append(distance(vector[i], vector[j]))
        identical.append(1 if name[i] == name[j] else 0)
        
distances = np.array(distances)
identical = np.array(identical)

thresholds = np.arange(0.3, 1.0, 0.01)

f1_scores = [f1_score(identical, distances < t) for t in thresholds]
acc_scores = [accuracy_score(identical, distances < t) for t in thresholds]

opt_idx = np.argmax(f1_scores)
# Threshold at maximal F1 score
opt_tau = thresholds[opt_idx]
# Accuracy at maximal F1 score
opt_acc = accuracy_score(identical, distances < opt_tau)
