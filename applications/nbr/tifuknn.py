import sys
import numpy as np
# from scipy.sparse import csr_matrix
import math
from sklearn.neighbors import NearestNeighbors


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TIFUKNN:
    def __init__(self, train_baskets, distance_metric='minkowski', k=300, kplus=0,
                 m=7, rb=1, rg=0.6, alpha=0.7):

        self.train_baskets = train_baskets

        self.k = k
        self.kplus = kplus
        self.m = m
        self.rb = rb
        self.rg = rg
        self.alpha = alpha

        self.user_keys = []
        self.user_reps = []
        self.item_id_mapper = {}
        self.id_item_mapper = {}
        self.user_map = {}
        self.distance_metric = distance_metric
        self.all_user_nns = {}

        self.all_items = self.train_baskets[['item_id']].drop_duplicates()['item_id'].tolist()
        self.all_users = self.train_baskets[['user_id']].drop_duplicates()['user_id'].tolist()

        counter = 0
        for i in range(len(self.all_items)):
            self.item_id_mapper[self.all_items[i]] = counter
            self.id_item_mapper[counter] = self.all_items[i]
            counter += 1

    def train(self):
        # sorted_baskets = self.train_baskets.sort_values(['user_id','date'])
        sorted_baskets = self.train_baskets.sort_values(['user_id', 'order_number'])
        sorted_baskets = sorted_baskets[['user_id','basket_id']].drop_duplicates()
        user_baskets_df = sorted_baskets.groupby('user_id')['basket_id'].apply(list).reset_index()
        user_baskets_dict = dict(zip(user_baskets_df['user_id'], user_baskets_df['basket_id']))

        basket_items_df = self.train_baskets[['basket_id', 'item_id']].drop_duplicates().groupby('basket_id')['item_id'] \
            .apply(list).reset_index()
        basket_items_dict = dict(zip(basket_items_df['basket_id'], basket_items_df['item_id']))

        basket_reps = {}
        counter = 0
        for basket in basket_items_dict:
            counter += 1
            #if counter % 10000 == 0:
            #    eprint(counter, ' baskets passed')
            rep = np.zeros(len(self.item_id_mapper))
            for item in basket_items_dict[basket]:
                if item in self.item_id_mapper:
                    rep[self.item_id_mapper[item]] = 1
            basket_reps[basket] = rep

        user_keys = []
        user_reps = []
        counter = 0
        for user in self.all_users:
            counter += 1
            # if counter % 1000 == 0:
            #    eprint(counter, ' users passed')
            rep = np.zeros(len(self.item_id_mapper))

            baskets = user_baskets_dict[user]
            group_size = math.ceil(len(baskets)/self.m)
            addition = (group_size * self.m) - len(baskets)

            basket_groups = []
            basket_groups.append(baskets[:group_size-addition])
            for i in range(self.m-1):
                basket_groups.append(baskets[group_size-addition+(i * group_size):group_size-addition+((i+1) * group_size)])

            for i in range(self.m):
                group_rep = np.zeros(len(self.item_id_mapper))#np.array([0.0] * len(self.item_id_mapper))
                for j in range(1, len(basket_groups[i])+1):
                    basket = basket_groups[i][j-1]
                    basket_rep = np.array(basket_reps[basket]) * math.pow(self.rb, group_size-j)
                    group_rep += basket_rep
                group_rep /= group_size

                rep += np.array(group_rep) * math.pow(self.rg, self.m-i)

            rep /= self.m
            user_reps.append(rep)
            user_keys.append(user)

        self.user_keys = user_keys
        self.user_reps = np.array(user_reps)
        self.user_map = dict(zip(user_keys, range(len(user_keys))))

        # TODO use sparse rep
        #  representations = csr_matrix(self.user_reps)
        nbrs = NearestNeighbors(n_neighbors=self.k + 1 + self.kplus, algorithm='brute', metric=self.distance_metric)\
            .fit(user_reps)
        distances, indices = nbrs.kneighbors(user_reps)
        self.nn_indices = indices

    def predict(self):
        ret_dict = {}
        for i in range(len(self.user_keys)):
            user = self.user_keys[i]
            user_rep = self.user_reps[i]
            
            nn_rep = np.zeros(len(user_rep))
            user_nns = self.nn_indices[i].tolist()[1:]
            user_nns = user_nns[:self.k]
            for neighbor in user_nns:
                nn_rep += self.user_reps[neighbor]
            self.all_user_nns[user] = user_nns
            nn_rep /= len(user_nns)

            final_rep = (user_rep * self.alpha + (1-self.alpha) * nn_rep).tolist()
            final_rep_sorted = sorted(range(len(final_rep)), key=lambda pos: final_rep[pos], reverse=True)

            top_items = []
            for item_index in final_rep_sorted:
                top_items.append(self.id_item_mapper[item_index])
            ret_dict[user] = top_items
        return ret_dict
