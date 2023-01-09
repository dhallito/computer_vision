import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import StandardScaler

from sklearn import decomposition

import joblib

workbook=xlrd.open_workbook('letras.xlsx')

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
    capas = [(10,), (10,50,)]
    kernels = ['tanh', 'relu']
    X,Y=load_xlsx(workbook)

    models_mlp = []
    models_mlp_score = []
    models_mlp_kernel = []
    models_mlp_capas = []

    model_ss = StandardScaler()
    model_pca = decomposition.PCA(n_components=14) #Seleccion
    X_SS = model_ss.fit_transform(X)
    model_pca.fit(X_SS)
    X_PCA = model_pca.transform(X_SS)
    strain, stest, rtrain, rtest=train_test_split(X_PCA,Y,test_size=0.3)

    for i in capas:
        for j in kernels:
            #print(len(X),len(Y))           #Se verifica que si retorne los mismo tamaños para ambas variables
            print('##########################')
            print('Realizando modelo MLP con función ' + j + ' y ' + str(len(i)) + ' capa(s) oculta(s) de ' + str(i) + ' neuronas')
            model_mlp=MLPClassifier(activation=j,hidden_layer_sizes=i,max_iter=10000,tol=0.0001)
            model_mlp.fit(strain,rtrain)
            rpred=model_mlp.predict(stest)
            acc_score = accuracy_score(rtest,rpred)*100.0
            models_mlp.append(model_mlp)
            accuracy = model_mlp.score(stest,rtest)*100.0
            models_mlp_score.append(accuracy)
            models_mlp_kernel.append(j)
            models_mlp_capas.append(i)
            print('Resultado... ' + str(accuracy) + "%")
            print('##########################')
            print('')



    better_score_mlp = max(models_mlp_score)
    index_better = models_mlp_score.index(better_score_mlp)
    better_model_mlp = models_mlp[index_better]

    print('########################## Mejor Modelo')
    print(  'MLP con funcion ' + models_mlp_kernel[index_better] + ' y ' + str(len(models_mlp_capas[index_better])) + 
            ' capa(s) oculta(s) de ' + str(models_mlp_capas[index_better]) + ' neuronas')
    print('##########################')
    

    if better_score_mlp >= 95:
        joblib.dump(model_ss, 'model_ss.pkl')
        joblib.dump(model_pca, 'model_pca.pkl')
        joblib.dump(better_model_mlp, 'model_mlp.pkl')