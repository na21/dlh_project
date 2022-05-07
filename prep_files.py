import os
import pickle
import numpy as np
from sklearn.model_selection import StratifiedKFold


def pipeline():
    skf = StratifiedKFold(n_splits=5)
    count = 0
    
    X = np.load('local_mimic/save/X19.npy')
    y = get_task()
    ref_target = y
    
    X, y = np.array(X), np.array(y)

    for train_index, test_index in skf.split(X, ref_target):
        count += 1
        print ("KFold #{0}".format(count))
        
        X_tr, X_te = X[train_index], X[test_index]
        y_tr, y_te = y[train_index], y[test_index]

    Y_tr = np.zeros((y_tr.shape[0],2))
    Y_te = np.zeros((y_te.shape[0],2))
    for i, v in enumerate(y_tr):
        if v == 0 :
            Y_tr[i][1] = 1
        else:
            Y_tr[i][0] = 1
    for i, v in enumerate(y_te):
        if v == 0:
            Y_te[i][1]=1
        else:
            Y_te[i][0]=1

    os.makedirs('processed_files', exist_ok=True)
    
    with open('processed_files/data_train.pkl', 'wb') as f:
        pickle.dump(X_tr, f)
    with open('processed_files/target_train.pkl', 'wb') as f:
        pickle.dump(Y_tr, f)
    with open('processed_files/data_test.pkl', 'wb') as f:
        pickle.dump(X_te, f)
    with open('processed_files/target_test.pkl', 'wb') as f:
        pickle.dump(Y_te, f)


def get_task():
    with open('local_mimic/save/y', 'rb') as f:
        labels = pickle.load(f)
    dct = {'mort': 0}
    task = [yy[dct['mort']] for yy in labels]

    return np.array(task)


if __name__ == '__main__':
    pipeline()
