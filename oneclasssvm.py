
# coding: utf-8

# In[113]:


import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
import json


# In[ ]:





# In[105]:


def oneClassSvm():
    X =pd.read_csv('feeds.csv')
    X=X.drop(columns=['created_at','entry_id','field1'])
    xx, yy = np.meshgrid(np.linspace(-3, 3, 500), np.linspace(-5, 5, 500))
    # Generate train data

    X=X[np.isfinite(X['field3'])]
    for i in range(118,len(X)):
        j=X['field2'][i]
        j=j.partition('\r')
        j=int(j[0])
        X['field2'][i]=j

#print(isinstance(X['field2'][624],str))
    for i in range(118,len(X)+118):
        if (isinstance(X['field2'][i],str)):
            j=X['field2'][i]
            #print(j," ",i)
            j=j.partition('\r')
            #print(j[0])
            X['field2'][i]=int(j[0])
    Y=X['field4']
    X=X.drop(columns=['field4'])
    X_train,X_test,Y_train,Y_test=train_test_split(X, Y, test_size=0.2, random_state=42)
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(X_train)
    #X_test=np.reshape(X_test,[-1,1])
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    #y_pred_outliers = clf.predict(X_outliers)
    n_error_train = y_pred_train[y_pred_train == -1].size
    n_error_test = y_pred_test[y_pred_test == -1].size
    #n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

    # plot the line, the points, and the nearest vectors to the plane
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    count=0
    Y_test=np.array(Y_test)
    for i in range(len(y_pred_test)):
        if(Y_test[i]==y_pred_test[i]):
            count=1+count
            #print(count)
    #print((count*100)/len(Y_test))
    return clf


# In[139]:


def getresult(X,crop):
    d=json.loads(X)
    d=d['feeds']
    l=[]
    for i in d:
        l.append([int(i['field2']),float(i['field3'])])
    df = pd.DataFrame(columns=['fild2','field3'])
    j=0
    for i in l:
        df.loc[j]=i;
        j+=1
    #print(df)
    clf= oneClassSvm()
    result=clf.predict(df)
    return result


# In[137]:
