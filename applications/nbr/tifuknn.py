import sys
import numpy as np
# from scipy.sparse import csr_matrix
import math
from sklearn.neighbors import NearestNeighbors


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TIFUKNN:
    def __init__(self, train_baskets, k=300, kplus=0, m=7, rb=1, rg=0.6, alpha=0.7):

        self.k = k
        self.kplus = kplus
        self.m = m
        self.rb = rb
        self.rg = rg
        self.alpha = alpha

        self.num_users = train_baskets['user_id'].max() + 1
        self.num_items = train_baskets['item_id'].max() + 1
        self.user_reps = []
        self.nn_indices = []

        self._compute_user_representations(train_baskets)

    def _compute_user_representations(self, train_baskets):

        sorted_baskets = train_baskets.sort_values(['user_id', 'order_number'])
        sorted_baskets = sorted_baskets[['user_id', 'basket_id']].drop_duplicates()
        user_baskets_df = sorted_baskets.groupby('user_id')['basket_id'].apply(list).reset_index()
        user_baskets_dict = dict(zip(user_baskets_df['user_id'], user_baskets_df['basket_id']))

        basket_items_df = train_baskets[['basket_id', 'item_id']].drop_duplicates().groupby('basket_id')['item_id'] \
            .apply(list).reset_index()
        basket_items_dict = dict(zip(basket_items_df['basket_id'], basket_items_df['item_id']))

        basket_reps = {}

        for basket in basket_items_dict:
            rep = np.zeros(self.num_items)
            for item in basket_items_dict[basket]:
                rep[item] = 1
            basket_reps[basket] = rep

        user_reps = []

        for user in range(self.num_users):

            rep = np.zeros(self.num_items)

            baskets = user_baskets_dict[user]
            group_size = math.ceil(len(baskets) / self.m)
            addition = (group_size * self.m) - len(baskets)

            basket_groups = []
            basket_groups.append(baskets[:group_size-addition])
            for i in range(self.m-1):
                basket_groups.append(baskets[group_size-addition+(i * group_size):group_size-addition+((i+1) * group_size)])

            for i in range(self.m):
                group_rep = np.zeros(self.num_items)
                for j in range(1, len(basket_groups[i])+1):
                    basket = basket_groups[i][j-1]
                    basket_rep = np.array(basket_reps[basket]) * math.pow(self.rb, group_size-j)
                    group_rep += basket_rep
                group_rep /= group_size

                rep += np.array(group_rep) * math.pow(self.rg, self.m-i)

            rep /= self.m
            user_reps.append(rep)

        self.user_reps = np.array(user_reps)  # TODO use sparse rep
        nbrs = NearestNeighbors(n_neighbors=self.k + 1 + self.kplus, algorithm='brute', metric='cosine') \
            .fit(user_reps)

        # We need to make sure that we don't receive neighbors with zero overlap, therefore a radius query is required
        distances, indices = nbrs.radius_neighbors(X=user_reps, radius=0.99, return_distance=True, sort_results=True)
        how_many = self.k + 1 + self.kplus
        for indices_for_one in indices:
            self.nn_indices.append(indices_for_one[:how_many])

    def retrieve_for(self, user):
        how_many = self.k + 1 + self.kplus
        # Skip user itself
        return self.nn_indices[user][1:how_many]

    def representation(self, user):
        return self.user_reps[user]

    def predict(self, user, neighbors, how_many):
        user_rep = self.user_reps[user]

        nn_rep = np.zeros(self.num_items)
        for neighbor in neighbors:
            nn_rep += self.user_reps[neighbor]

        nn_rep /= len(neighbors)

        final_rep = (user_rep * self.alpha + (1-self.alpha) * nn_rep).tolist()
        top_items = sorted(range(len(final_rep)), key=lambda pos: final_rep[pos], reverse=True)

        return top_items[:how_many]
