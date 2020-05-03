from __future__ import print_function, division

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from keras.models import Sequential
from keras.layers import Dense, Input
from helper.utilities import _randuniform,_randchoice,_randint
from helper.utilities import *
from keras import backend as K
import numpy as np

def DT():
    a=_randuniform(0.0,1.0)
    b=_randchoice(['gini','entropy'])
    c=_randchoice(['best','random'])
    model = DecisionTreeClassifier(criterion=b, splitter=c, min_samples_split=a, max_features=None, min_impurity_decrease=0.0)
    tmp=str(a)+"_"+b+"_"+c+"_"+DecisionTreeClassifier.__name__
    return model,tmp

def RF():
    a = _randint(50, 150)
    b = _randchoice(['gini', 'entropy'])
    c = _randuniform(0.0, 1.0)
    model = RandomForestClassifier(n_estimators=a,criterion=b,min_samples_split=c, max_features=None, min_impurity_decrease=0.0, n_jobs=-1)
    tmp=str(a)+"_"+b+"_"+str(round(c,5))+"_"+RandomForestClassifier.__name__
    return model,tmp

def SVM():
    # from sklearn.preprocessing import MinMaxScaler
    # scaling = MinMaxScaler(feature_range=(-1, 1)).fit(train_data)
    # train_data = scaling.transform(train_data)
    # test_data = scaling.transform(test_data)
    a = _randint(1, 500)
    b = _randchoice(['linear', 'poly', 'rbf', 'sigmoid'])
    c = _randint(2,10)
    d = _randuniform(0.0,1.0)
    e = _randuniform(0.0,0.1)
    f = _randuniform(0.0, 0.1)
    model = SVC(C=float(a), kernel=b, degree=c, gamma=d, coef0=e, tol=f, cache_size=20000)
    tmp = str(a) + "_" + b+"_"+str(c) + "_" + str(round(d,5)) + "_" + str(round(e,5)) + "_"+str(round(f,5)) + "_"+SVC.__name__
    return model, tmp

def KNN():
    a = _randint(2, 25)
    b = _randchoice(['uniform', 'distance'])
    c = _randchoice(['minkowski','chebyshev'])
    if c=='minkowski':
        d=_randint(1,15)
    else:
        d=2
    model = KNeighborsClassifier(n_neighbors=a, weights=b, algorithm='auto', p=d, metric=c, n_jobs=-1)
    tmp = str(a) + "_" + b + "_" +c+"_"+str(d) + "_" + KNeighborsClassifier.__name__
    return model,tmp

def NB():
    model = GaussianNB()
    return model, GaussianNB.__name__

def LR():
    a=_randchoice(['l1','l2'])
    b=_randuniform(0.0,0.1)
    c=_randint(1,500)
    model = LogisticRegression(penalty=a, tol=b, C=float(c), solver='liblinear', multi_class='warn')
    tmp=a+"_"+str(round(b,5))+"_"+str(c)+"_"+LogisticRegression.__name__
    return model,tmp


# from https://gist.github.com/wassname/ce364fddfc8a025bfab4348cf5de852d
def weighted_categorical_crossentropy(weights):
    """  
    A weighted version of keras.objectives.categorical_crossentropy
                                   
    Variables:
    weights: numpy array of shape (C,) where C is the number of classes
    """ 
    weights = K.variable(weights)
    def loss(y_true, y_pred):
        return K.mean(
            K.binary_crossentropy(y_true, y_pred) * weights)
                                                                                                            
    return loss

def DeepLearner(inputs=20):
    n_layers = randint(1, 4)
    n_units = randint(2, 20)

    model = Sequential()

    for i in range(n_layers):
        model.add(Dense(n_units, activation='relu', input_shape=(inputs,)))

    model.add(Dense(1, activation='sigmoid'))
    tmp = str(n_layers) + "_" + str(n_units) + "_DL"
    return model, tmp

def run_model(train_data,test_data,model,metric,training=-1):
    frac = sum(train_data["bug"]) * 1.0 / len(train_data["bug"])
    weights = np.array([1., 1. / frac])

    model.compile('sgd', loss=weighted_categorical_crossentropy(weights))
    model.fit(train_data[train_data.columns[:training]], train_data["bug"], epochs=10, verbose=0)
    prediction = model.predict_classes(test_data[test_data.columns[:training]])
    test_data.loc[:,"prediction"]=prediction
    return round(get_score(metric,prediction, test_data["bug"].tolist(),test_data ),5)

