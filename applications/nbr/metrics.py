def hitrate_at_n(y_true, y_pred, n):
    predicted_items = set(y_pred[:n])
    true_items = set(y_true)
    num_relevant = len(predicted_items.intersection(true_items))

    if num_relevant > 0:
        return 1.0
    else:
        return 0.0


def recall_at_n(y_true, y_pred, n):
    predicted_items = set(y_pred[:n])
    true_items = set(y_true)
    num_relevant = len(predicted_items.intersection(true_items))

    return num_relevant / len(true_items)


def precision_at_n(y_true, y_pred, n):
    predicted_items = set(y_pred[:n])
    true_items = set(y_true)
    num_relevant = len(predicted_items.intersection(true_items))

    return num_relevant / n

# def ndcg_k(y_true, y_pred, k):
#     a = 0
#     for i,x in enumerate(y_pred[:k]):
#         if x in y_true:
#             a+= 1/np.log2(i+2)
#     b = 0
#     for i in range(k):
#         b +=1/np.log2(i+2)
#     return a/b
