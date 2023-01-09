import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
#Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib

workBook = xlrd.open_workbook("nums.xlsx")

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

    strain, stest, rtrain, rtest = \
                train_test_split(X, Y, test_size = 0.3)

    mlp = MLPClassifier(activation='logistic',
                        hidden_layer_sizes=(20,),
                        max_iter=100000, tol=0)
    mlp.fit(strain, rtrain) 
    rpredict = mlp.predict(stest)

    acc_score = accuracy_score(rtest,rpredict)*100.0
    print('accuracy score: ',mlp.score(stest,rtest)*100.0)
    print('accuracy score: ', acc_score)

    if acc_score >= 100:
        joblib.dump(mlp, 'mlp_100.pkl')

        #Sin usar SS y PCA + 0.1
        #Reto 1 > 99% + 0.3
        #Reto 2 > 98% + 0.2
        #Reto 3 > 97% + 0.1

    
    
    
    
