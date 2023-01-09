import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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
    #print(len(X),len(Y))           #Se verifica que si retorne los mismo tamaños para ambas variables
    strain, stest, rtrain, rtest=train_test_split(X,Y,test_size=0.3)
    mlp=MLPClassifier(activation='relu',hidden_layer_sizes=(10,),max_iter=1000,tol=0.0001)
    mlp.fit(strain,rtrain)
    rpred=mlp.predict(stest)
    print('accuracy score: ',mlp.score(stest,rtest)*100.0)
    print('accuracy score: ',accuracy_score(rtest,rpred)*100.0)
