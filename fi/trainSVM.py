import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

from pyexpat.errors import XML_ERROR_SUSPENDED
import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
#Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.svm import SVC

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score ##Para hacer combinaciones distintas de folders de entrenamiento

from sklearn.metrics import confusion_matrix

import joblib

import pandas as pd

workBook = xlrd.open_workbook("caracteres.xlsx")

##Funcion para extraer carac y class
def load_xlsx(book):
    sh = book.sheet_by_index(0)
    x = np.zeros((sh.nrows, sh.ncols-1))
    y = []
    for i in range(0, sh.nrows):
        for j in range(0, sh.ncols-1):
            x[i,j] = sh.cell_value(rowx=i, colx=j+1)
        y.append(sh.cell_value(rowx=i, colx=0))
        
    y = np.array(y, np.float32)
    return x,y

##### Inicio del programa ######
if __name__ == '__main__':
    X, Y = load_xlsx(workBook)
    print(len(X), len(Y))

    model_ss = StandardScaler()
    model_ss.fit(X)
    x_ss = model_ss.transform(X)

    n_components = 10
    model_pca = PCA(n_components)
    model_pca.fit(x_ss)
    x_pca = model_pca.transform(x_ss)

    '''expl_var = model_pca.explained_variance_ratio_
    print(expl_var)
    for i in range(1, n_components + 1):
        print('suma de componentes', i, 'es:', sum(expl_var[0:i]))

    plt.plot(np.cumsum(expl_var))
    plt.xlabel('numer of components')
    plt.ylabel('cumulative explained variance')
    plt.show()'''

    strain, stest, rtrain, rtest = \
                train_test_split(x_ss, Y, test_size = 0.3)

    model_svm = SVC(C=50, kernel="rbf")

    '''cross_scores_svm = cross_val_score(model_svm, x_ss, Y, cv = 4)     #cv son los folders
    print("cross_scores_svm:", cross_scores_svm.mean())'''


    model_svm.fit(strain, rtrain) 
    rpredict_svm = model_svm.predict(stest)

    print(pd.DataFrame(confusion_matrix(rtest, rpredict_svm)))

    acc_score_svm = accuracy_score(rtest,rpredict_svm)*100.0
    print('accuracy score: ', acc_score_svm)    


    if acc_score_svm >= 90:
        joblib.dump(model_ss, 'model_ss.pkl')
        joblib.dump(model_svm, 'model_svm.pkl')