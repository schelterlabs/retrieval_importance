"""
-----SEED=42-----
datasize_dirty=157463, datasize_clean=102215
validation, hitrate@5_dirty=0.88000, hitrate@5_clean=0.88000
validation, precision@5_dirty=0.42800, precision@5_clean=0.43200
validation, recall@5_dirty=0.22702, recall@5_clean=0.22795
test, hitrate@5_dirty=0.77000, hitrate@5_clean=0.78000
test, precision@5_dirty=0.36600, precision@5_clean=0.37200
test, recall@5_dirty=0.19187, recall@5_clean=0.19470
-----SEED=16-----
datasize_dirty=156897, datasize_clean=99019
validation, hitrate@5_dirty=0.92000, hitrate@5_clean=0.91000
validation, precision@5_dirty=0.45600, precision@5_clean=0.45000
validation, recall@5_dirty=0.22608, recall@5_clean=0.22550
test, hitrate@5_dirty=0.84000, hitrate@5_clean=0.84000
test, precision@5_dirty=0.40000, precision@5_clean=0.40200
test, recall@5_dirty=0.20532, recall@5_clean=0.20546
-----SEED=1812-----
datasize_dirty=163196, datasize_clean=101568
validation, hitrate@5_dirty=0.78000, hitrate@5_clean=0.77000
validation, precision@5_dirty=0.38200, precision@5_clean=0.38200
validation, recall@5_dirty=0.19465, recall@5_clean=0.19458
test, hitrate@5_dirty=0.78000, hitrate@5_clean=0.79000
test, precision@5_dirty=0.36400, precision@5_clean=0.37400
test, recall@5_dirty=0.18271, recall@5_clean=0.19073
-----SEED=1312-----
datasize_dirty=162644, datasize_clean=99676
validation, hitrate@5_dirty=0.86000, hitrate@5_clean=0.87000
validation, precision@5_dirty=0.42600, precision@5_clean=0.42400
validation, recall@5_dirty=0.21690, recall@5_clean=0.21521
test, hitrate@5_dirty=0.83000, hitrate@5_clean=0.80000
test, precision@5_dirty=0.37200, precision@5_clean=0.36400
test, recall@5_dirty=0.20305, recall@5_clean=0.19842
-----SEED=35-----
datasize_dirty=162235, datasize_clean=99611
validation, hitrate@5_dirty=0.75000, hitrate@5_clean=0.75000
validation, precision@5_dirty=0.37400, precision@5_clean=0.37800
validation, recall@5_dirty=0.18795, recall@5_clean=0.18763
test, hitrate@5_dirty=0.85000, hitrate@5_clean=0.84000
test, precision@5_dirty=0.39800, precision@5_clean=0.40400
test, recall@5_dirty=0.20391, recall@5_clean=0.20504
"""
import pandas as pd
import numpy as np

from retrieval_importance import learn_importance, encode_retrievals
from applications.nbr.tifuknn import TIFUKNN
from applications.nbr.data import index_consecutive
from applications.nbr.metrics import hitrate_at_n, recall_at_n, precision_at_n

def utility(retrieval, user_vector):    

    predictions = [(item, weight) for item, weight in enumerate(user_vector) if weight > 0.0]    
    prediction_sorted = sorted(predictions, key=lambda pred: pred[1], reverse=True)
    top_items = [pred[0] for pred in prediction_sorted]
    
    recall = recall_at_n(retrieval['next_basket'], top_items, 5)    
    
    return np.around(recall, decimals=2)

def compare(tifu, users_to_retain, evaluation_baskets, num_eval_users, name):

    hitrates_dirty = []
    recalls_dirty = []
    precisions_dirty = []
    
    hitrates_clean = []
    recalls_clean = []
    precisions_clean = []
    
    for user in range(0, num_eval_users):
        
        next_basket_items = list(evaluation_baskets[evaluation_baskets.user_id==user].item_id)    

        k = 10 # TODO should be a param
        n = 5  # TODO should be a param
        all_neighbors = tifu.retrieve_for(user)
        
        # Original prediction
        prediction = tifu.predict(user, all_neighbors[:k], n)
        
        cleaned_neighbors = [neighbor for neighbor in all_neighbors if neighbor in users_to_retain]
        prediction_clean = tifu.predict(user, cleaned_neighbors[:k], n)

        
        hitrates_dirty.append(hitrate_at_n(next_basket_items, prediction, n))
        recalls_dirty.append(recall_at_n(next_basket_items, prediction, n))     
        precisions_dirty.append(precision_at_n(next_basket_items, prediction, n))             
        
        hitrates_clean.append(hitrate_at_n(next_basket_items, prediction_clean, n))
        recalls_clean.append(recall_at_n(next_basket_items, prediction_clean, n))
        precisions_clean.append(precision_at_n(next_basket_items, prediction_clean, n))  
    
    print(f'{name}, hitrate@5_dirty={np.mean(hitrates_dirty):.5f}, hitrate@5_clean={np.mean(hitrates_clean):.5f}') 
    print(f'{name}, precision@5_dirty={np.mean(precisions_dirty):.5f}, precision@5_clean={np.mean(precisions_clean):.5f}')     
    print(f'{name}, recall@5_dirty={np.mean(recalls_dirty):.5f}, recall@5_clean={np.mean(recalls_clean):.5f}')     

def ComputeProb(p, K, M, IP, RP):
    IP[0][0] = 1
    RP[0][M+1] = 1
    
    for j in range(1, M+1):
        IP[0][j] = IP[0][j-1] * (1 - p[j-1])
        for k in range(1,K+1):
            IP[k][j] = IP[k][j-1] * (1 - p[j-1]) + IP[k-1][j-1] * p[j-1]
    
    for j in range(M, 0, -1):
        RP[0][j] = RP[0][j+1] * (1 - p[j-1])
        for k in range(1,K+1):
            RP[k][j] = RP[k][j+1] * (1 - p[j-1]) + RP[k-1][j+1] * p[j-1]
    
    return IP, RP


def ComputeBoundarySetProb_anyloss(f_train, value_dict, p, K, M, B):
    n_value = len(value_dict)
    for i in range(M, 0, -1):
        for k in range(1, K+1):
            for e in range(0, n_value):
                B[k][i][e] = B[k][i+1][e] * (1 - p[i-1]) + B[k-1][i+1][e] * p[i-1]
                if (k==1) & (value_dict[e] == f_train[i-1]):
                    B[k][i][e] += p[i-1]
    return B

def Additive_anyloss_MLE_Gradient(f_train, p, K, M):
    
    if(len(p)!=M):
        print("p ", len(p))
        print("M ", M)
    
    s = np.zeros(M)

    IP = np.zeros([K+1, M+2])
    RP = np.zeros([K+1, M+2])
    IP, RP = ComputeProb(p, K, M, IP, RP)
    
    value_dict = []
    f_dict = []
    for id, i in enumerate(f_train):
        if i not in value_dict:
            value_dict.append(i)
            f_dict.append(f_train[id])
    n_value = len(value_dict)
    
    B = np.zeros([K+1, M+2, n_value])
    B = ComputeBoundarySetProb_anyloss(f_train, value_dict, p, K, M, B)

    for i in range(1, M+1):
        for e in range(0, n_value):
            u_2 = (f_train[i-1] - f_dict[e]) / K
            for j in range(0, K):
                s[i-1] = s[i-1] + u_2 * IP[j][i-1] * B[K-j][i+1][e]
    return s

def compute_mle(encoded_retrievals, K, M, learning_rate, num_steps):
    p = np.ones(M) * 0.5

    for t in range(num_steps):
        summ = 0
        for source in encoded_retrievals:
            retrieved_id = source["retrieved"]
            f_cost = source["utility_contributions"]
            p_now = [p[id] for id in retrieved_id]
            s = Additive_anyloss_MLE_Gradient(f_cost, p_now, K, len(f_cost))
            for i, id in enumerate(retrieved_id):
                p[id] = p[id] + s[i] * learning_rate
            summ += sum(s)
        if t%50 == 0:
            print("Iteration %d finished ! The sum of gradient is %.3f"%(t, summ))
    
    return p

def experiment(seed, num_users, num_eval_users, threshold, all_train_baskets, all_validation_baskets, all_test_baskets, lr = 0.1):
    np.random.seed(seed)

    unique_user_ids = list(all_train_baskets.user_id.unique())
    sampled_users = np.random.choice(unique_user_ids, num_users)
    train_baskets = all_train_baskets[all_train_baskets.user_id.isin(sampled_users)]
    validation_baskets = all_validation_baskets[all_validation_baskets.user_id.isin(sampled_users)]
    test_baskets = all_test_baskets[all_test_baskets.user_id.isin(sampled_users)] 

    index_consecutive('user_id', [train_baskets, validation_baskets, test_baskets])
    index_consecutive('item_id', [train_baskets, validation_baskets, test_baskets])    
    
    tifu = TIFUKNN(train_baskets, k=10, kplus=40)


    retrievals = []
    for user in range(0, num_eval_users):

        next_basket = list(validation_baskets[validation_baskets.user_id==user].item_id)

        neighbors = tifu.retrieve_for(user)
        neighbor_representations = [tifu.representation(neighbor) for neighbor in neighbors]       

        if len(next_basket) > 0:    
            retrievals.append({
                'user': user,
                'next_basket': next_basket,
                'neighbors': neighbors,
                'neighbor_representations': neighbor_representations,
            })    

    encoded_retrievals, mapping = encode_retrievals(retrievals, "neighbors", "neighbor_representations", utility)  

    v = compute_mle(encoded_retrievals, K=10, M=1000, learning_rate=lr, num_steps=200)

    import matplotlib.pyplot as plt
    plt.hist(v)
    plt.savefig("./figure/v_value.jpg", dpi=100, bbox_inches="tight")
    plt.cla()

    users_to_retain = set([user for (user, value) in enumerate(v) if value >= threshold])
    users_to_retain.update(range(0, num_eval_users))


    print(f'-----SEED={seed}-----')
    cleaned_train_baskets = train_baskets[train_baskets.user_id.isin(users_to_retain)]    
    print(f'datasize_dirty={len(train_baskets)}, datasize_clean={len(cleaned_train_baskets)}')
    
    compare(tifu, users_to_retain, validation_baskets, num_eval_users, 'validation')
    compare(tifu, users_to_retain, test_baskets, num_eval_users, 'test')        
    return v

if __name__ == "__main__":
    all_train_baskets = pd.read_csv("applications/nbr/data/instacart_30k/train_baskets.csv.gz")
    all_validation_baskets = pd.read_csv("applications/nbr/data/instacart_30k/valid_baskets.csv")
    all_test_baskets = pd.read_csv("applications/nbr/data/instacart_30k/test_baskets.csv") 

    print("load finished !!")

    for seed in [42, 16, 1812, 1312, 35]:
        experiment(seed, 1000, 100, 0.5, all_train_baskets, all_validation_baskets, all_test_baskets)