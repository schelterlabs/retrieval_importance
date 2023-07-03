from pathlib import Path
from statistics import mode
import random
import numpy as np
from multiprocessing import Pool
import json
import math

def encode_retrievals(retrievals, retrieved_key, prediction_key, utility):

    encoded_retrievals = []

    all_retrieveds = set()

    for retrieval in retrievals:
        for retrieved in retrieval[retrieved_key]:
            all_retrieveds.add(retrieved)

    all_retrieveds = list(all_retrieveds)
    all_retrieveds.sort()

    mapping = {retrieved:index for index, retrieved in enumerate(all_retrieveds)}

    for retrieval in retrievals:
        retrieveds = [mapping[name] for name in retrieval[retrieved_key]]
        utilities = [utility(retrieval, prediction) for prediction in retrieval[prediction_key]]
        encoded_retrievals.append({
            "retrieved": retrieveds,
            "utility_contributions": utilities
        })

    return encoded_retrievals, mapping


def encode_groups(mapping, group):
    groups = set()

    for retrieved in mapping.keys():
        assigned_group = group(retrieved)
        groups.add(assigned_group)

    all_groups = list(groups)
    all_groups.sort()

    group_mapping = {name:index for index, name in enumerate(all_groups)}

    grouping = [0 for _ in range(0, len(mapping))]

    for retrieved in mapping.keys():
        assigned_group = group(retrieved)
        retrieved_index = mapping[retrieved]
        group_index = group_mapping[assigned_group]
        grouping[retrieved_index] = group_index

    return grouping, group_mapping


def v_grouped(v, grouping, group_mapping):

    v_per_group = {}

    num_groups = len(group_mapping)

    retrieved_index_per_group = {}

    for retrieved_index, group_index in enumerate(grouping):
        retrieved_index_per_group[group_index] = retrieved_index
        # TODO add break

    for group, group_index in group_mapping.items():
        v_per_group[group] = v[retrieved_index_per_group[group_index]]

    return v_per_group


def most_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:-x[1])
    return sorted_importances[:how_many]


def least_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:x[1])

    return sorted_importances[:how_many]


def most_important_groups(v_per_group, how_many):
    sorted_importances = sorted(v_per_group.items(), key=lambda x:-x[1])
    return sorted_importances[:how_many]


def least_important_groups(v_per_group, how_many):
    sorted_importances = sorted(v_per_group.items(), key=lambda x:x[1])
    return sorted_importances[:how_many]

def get_project_root() -> Path:
    """Returns the project root folder."""
    return Path(__file__).parent.parent.parent

def cal_acc(test_set, retrievals, group, mapping, K = 0): 
    acc = 0
    for i in test_set:
        now_url = retrievals[i]['retrieved_websites']
        now_ans = retrievals[i]['retrieved_answers']
        now_correct = retrievals[i]['correct_answers']
        
        retain_list = []
        for url, ans in zip(now_url, now_ans):
            
            if group(url) not in mapping:
                continue
            if mapping[group(url)] == 0:
                continue

            retain_list.append(ans)
            if len(retain_list) == K:
                break
        if len(retain_list) == 0:
            continue
        max_ans = mode(retain_list)
        if max_ans in now_correct:
            acc += 1
    return acc/len(test_set)

def generate_val_test_set(length, seed):
    id_list = [i for i in range(length)]
    random.seed(seed)
    random.shuffle(id_list)
    val_set = id_list[:length//2]
    test_set = id_list[length//2:]
    return val_set, test_set

def sort_values(retrievals, val_set, v, group):
    url_count = {}
    for i in val_set:
        count_dict = [group(url) for url in retrievals[i]['retrieved_websites']]
        for url in count_dict:
            if url not in url_count:
                url_count[url] = 0
            url_count[url] += 1

    v_list = []
    total_doc = 0
    for url in v:
        v_list.append((url, v[url], url_count[url]))
        total_doc += url_count[url]
    v_list.sort(key=lambda x: x[1])

    return v_list, total_doc

def get_retain_urls(v_list, total_doc, remove_rate):
    keep_dict = {}
    for url, acc, count in v_list:
        keep_dict[url] = 1
    
    sum = 0
    for i in v_list:
        if sum >= remove_rate * total_doc:
            break
        keep_dict[i[0]] = 0
        sum += i[2]
    return keep_dict

def cal_acc_reweight_parallel(args):
    seed, test_set, retrievals, group, mapping, v, K, keep_all = args
    np.random.seed(seed)
    v_now = np.random.rand(len(v))
    
    acc = 0
    for i in test_set:
        now_url = retrievals[i]['retrieved_websites']
        now_ans = retrievals[i]['retrieved_answers']
        now_correct = retrievals[i]['correct_answers']
        retain_list = []
        for url, ans in zip(now_url, now_ans):
            if keep_all == False: 
                if group(url) not in v:
                    continue
                if v[group(url)] < v_now[mapping[group(url)]]:
                    continue
            retain_list.append(ans)
            if len(retain_list) == 10:
                break

        vote = {}       
        for ans in retain_list:
            if ans not in vote:
                vote[ans] = 0
            vote[ans] += 1
        max_vote = 0
        max_ans = ''
        for ans in vote:
            if vote[ans] > max_vote:
                max_vote = vote[ans]
                max_ans = ans
        if max_ans in now_correct:
            acc += 1
    return acc/len(test_set)

def cal_acc_reweight(test_set, retrievals, group, mapping, v, K = 10, keep_all = False): 
    seed = [67, 86, 55, 13, 1, 38, 81, 8, 52, 79, 10, 19, 30, 66, 36, 39, 59, 2, 21, 68, 41, 24, 31, 76, 47, 91, 99, 63, 51, 65, 26, 61]
    with Pool(32) as p:
        acc_list = p.map(cal_acc_reweight_parallel,[(seed[i], test_set, retrievals, group, mapping, v, K, keep_all) for i in range(32)])
    return sum(acc_list)/len(acc_list)

def array_split(arr, n):
    if len(arr) > n:
        res = []
        idx = np.array_split(np.arange(len(arr)), n)
        for i in idx:
            res.append([arr[j] for j in i])
    else:
        res = [[a] for i, a in enumerate(arr)]
    return res

def generate_source_list(random_seed):
    group_num = 5
    split_num = 10

    prob_list = [math.ceil(i/split_num)/group_num for i in range(1,1+group_num*split_num)]
    rank_list = []

    for i in range(group_num):
        random.seed(random_seed*5 + i) 
        all_number = [i for i in range(50)]
        random.shuffle(all_number)
        rank_list.extend(array_split(all_number, split_num))
    
    source_list = [(prob_list[i], rank_list[i]) for i in range(group_num*split_num)]

    random.seed(random_seed)
    random.shuffle(source_list)
    return source_list

def remove_acc(retrieval, remove_url, group, K = 10):
    retain_list = []
    for i in range(len(retrieval['retrieved_websites'])):
        if(group(retrieval['retrieved_websites'][i]) == remove_url):
            continue
        retain_list.append(retrieval['retrieved_answers'][i])
        if len(retain_list) == 10:
            break
    if len(retain_list) == 0:
        return 0
    max_ans = mode(retain_list)
    if max_ans in retrieval['correct_answers']:
        return 1
    return 0

def cal_loo(retrievals, group):
    result = []
    url_count = {}

    for retrieval in retrievals:

        count_dict = [group(i) for i in retrieval['retrieved_websites']]
        url_dict = list(set(count_dict))

        clean_acc = remove_acc(retrieval, "www.do_not_remove.com", group)

        for url in url_dict:
            acc = remove_acc(retrieval, url, group)
            result.append((url, clean_acc-acc))

        for url in count_dict:
            if url not in url_count:
                url_count[url] = 0
            url_count[url] += 1
    
    url_dict = {}
    for url, acc in result:
        if url not in url_dict:
            url_dict[url] = 0
        url_dict[url] += acc
    
    return url_dict

def generate_retrival(retrivals, source_list, random_seed, K = 10, max_len = 200):
    source = []
    random.seed(random_seed)
    
    for id, now in enumerate(retrivals):
        dataset = {}
        dataset["question"] = now["question"]
        dataset["correct_answers"] = now["correct_answers"]

        list = []
        for sid, i in enumerate(source_list):
            for j in i[1]:
                if(len(now["retrieved_answers"])>j):
                    now_i = random.random()
                    if now_i <i[0]:
                        list.append((j * 100 + sid, now["retrieved_answers"][j], str(sid)))
                    else:
                        list.append((j * 100 + sid, now["noise_answers"][j], str(sid)))
        sort_list = sorted(list, key=lambda x: x[0])

        dataset["retrieved_answers"] = [i[1] for i in sort_list]
        dataset["retrieved_websites"] = [i[2] for i in sort_list]
        source.append(dataset)
    return source

def load_retrievals(relation_name, scenrio, random_seed = 0):
    if scenrio == "raw":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/wikifact_url/{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        return retrievals
    if scenrio  == "fake":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/wikifact_fake/{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        return retrievals
    if scenrio == "noise":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/wikifact_noise/{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        source_list = generate_source_list(random_seed)
        retrievals = generate_retrival(retrievals, source_list, random_seed)
        return retrievals


def load_openai_retrievals(relation_name, scenrio, random_seed = 0):
    if scenrio == "raw":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/openai_raw/relation_{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        return retrievals
    if scenrio  == "fake":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/wikifact_fake/{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        return retrievals
    if scenrio == "noise":
        retrievals = []
        with open(f'{str(get_project_root())}/test_data/wikifact_noise/{relation_name}.jsonl') as f:
            for line in f:
                retrievals.append(json.loads(line))
        source_list = generate_source_list(random_seed)
        retrievals = generate_retrival(retrievals, source_list, random_seed)
        return retrievals

