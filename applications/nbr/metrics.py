import numpy as np


def recall_k(y_true, y_pred, k):
    a = len(set(y_pred[:k]).intersection(set(y_true)))
    b = len(set(y_true))
    return a/b


def ndcg_k(y_true, y_pred, k):
    a = 0
    for i,x in enumerate(y_pred[:k]):
        if x in y_true:
            a+= 1/np.log2(i+2)
    b = 0
    for i in range(k):
        b +=1/np.log2(i+2)
    return a/b
