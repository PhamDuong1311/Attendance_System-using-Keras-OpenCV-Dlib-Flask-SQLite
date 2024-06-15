import os
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
import pickle

def predict():
    path = "data"
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

    encoder = LabelEncoder()
    encoder.fit(name)
    y = encoder.transform(name)

    knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
    svm = LinearSVC()

    knn.fit(vector, y)
    svm.fit(vector, y)
    pickle.dump(svm, open('svm_model.pkl', 'wb'))

    pickle.dump(knn, open('knn_model.pkl', 'wb'))
