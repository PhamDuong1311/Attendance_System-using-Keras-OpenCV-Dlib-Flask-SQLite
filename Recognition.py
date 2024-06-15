import cv2
import pickle
import embedded_model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
import json
# from Threshold import opt_tau
def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

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

def nguoiquen(x):
    k = 0
    for i in vector:
        if distance(x,i) < 0.3:
            k+=1
            if k==5:
                return True
    return False

def check(path1):
    with open('svm_model.pkl', 'rb') as file:
        svm = pickle.load(file)
    path = 'data'
    data = []
    for i in sorted(os.listdir(path)):
        with open(os.path.join(path,i), 'r') as file:
            data.append(json.load(file))
    name=np.array([])
    k=0
    for i,n in enumerate(data):
        for j in range(5):
            if not k:
                name = data[i]['name']
                k=k+1
            else:
                name=np.hstack((name,data[i]['name']))
    encoder = LabelEncoder()
    encoder.fit(name)
    img= cv2.imread(path1)
    anhdep = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    anh_embedded= embedded_model.embedded(anhdep)
    if anh_embedded is False:
        cap = 'Vui lòng đưa mặt vào giữa camera'
        return  cap 
    if not nguoiquen(anh_embedded):
        cap = 'Tôi chưa gặp người này bao giờ'
        return cap    
    example_prediction = svm.predict([anh_embedded])
    anh_embedded = anh_embedded.reshape(1, -1)
    example_identity = encoder.inverse_transform(example_prediction)[0]
    cap = f'{example_identity} đúng không?'
    return cap
