import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import StandardScaler

from sklearn import decomposition

import joblib

workbook=xlrd.open_workbook('nums.xlsx')

##Funcion para extraer carac y clases
def load_xlsx(book):
    sh=book.sheet_by_index(0)
    x=np.zeros((sh.nrows,sh.ncols-1))
    y=[]
    for i in range(0,sh.nrows):
        for j in range(0,sh.ncols-1):
            x[i,j]=sh.cell_value(rowx=i,colx=j+1)
        y.append(sh.cell_value(rowx=i,colx=0))
        
    y=np.array(y,np.float32)
    return x,y


if __name__=='__main__':
    X,Y=load_xlsx(workbook)

    model_ss = StandardScaler()
    model_pca = decomposition.PCA(n_components=15) #Seleccion

    X_SS = model_ss.fit_transform(X)

    model_pca.fit(X_SS)
    X_PCA = model_pca.transform(X_SS)

    #print(len(X),len(Y))           #Se verifica que si retorne los mismo tamaños para ambas variables
    strain, stest, rtrain, rtest=train_test_split(X_PCA,Y,test_size=0.3)
    model_mlp=MLPClassifier(activation='relu',hidden_layer_sizes=(100,),max_iter=1000,tol=0.0001)
    model_mlp.fit(strain,rtrain)
    rpred=model_mlp.predict(stest)
    acc_score = accuracy_score(rtest,rpred)*100.0
    print('accuracy score: ',model_mlp.score(stest,rtest)*100.0)
    print('accuracy score: ', acc_score)

    if acc_score >= 90:
        joblib.dump(model_ss, 'model_ss.pkl')
        joblib.dump(model_pca, 'model_pca.pkl')
        joblib.dump(model_mlp, 'model_mlp.pkl')

        #Sin usar SS y PCA + 0.1
        #Reto 1 > 99% + 0.3
        #Reto 2 > 98% + 0.2
        #Reto 3 > 97% + 0.1