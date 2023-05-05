import json
import pandas as pd
from tldextract import extract
from pprint import pp
from statistics import mode
from tabulate import tabulate
from retrieval_importance import learn_importance, encode_retrievals, encode_groups, v_grouped, \
    most_important_groups, least_important_groups
from retrieval_importance.utils import get_project_root

def create_retrievals(target, test_or_valid_set, test_or_valid_answers):

    retrievals = []

    for sample_index, row in test_or_valid_set.iterrows():

        retrieved_websites = []
        generated_answers = []

        raw_answers_for_sample = test_or_valid_answers[test_or_valid_answers.sample_index==sample_index]\
            .sort_values(by=['position'])

        for _, raw_answer in raw_answers_for_sample.iterrows():

            prediction = str(raw_answer.answer).lower()
            retrieved_websites.append(raw_answer.url)
            generated_answers.append(prediction)

        retrievals.append({
            "sample_index": sample_index,
            "correct_answers": [row[target].lower()],
            "retrieved_websites": retrieved_websites,
            "generated_answers": generated_answers,
        })    
        
    return retrievals     

def utility(retrieval, prediction):
    if prediction in retrieval["correct_answers"]:
        return 1.0
    else:
        return 0.0

def group(retrieved):    
    _, domain_name, ending = extract(retrieved)
    return f'{domain_name}.{ending}'

def eval_accuracy(retrievals, k):
    correct = 0

    for retrieval in retrievals:
        prediction = mode(retrieval['generated_answers'][:k])
        if prediction in retrieval['correct_answers']:
            correct += 1

    accuracy = correct / len(retrievals)
    return accuracy

def cal_acc(test_retrievals, v, K): 
    acc = 0
    for i in test_retrievals:
        now_url = i['retrieved_websites']
        now_ans = i['generated_answers']
        now_correct = i['correct_answers']
        
        retain_list = []
        for url, ans in zip(now_url, now_ans):
            
            if group(url) not in v:
                continue
            if v[group(url)] == 0:
                continue

            # if group(url) in v:
            #     if v[group(url)] == 0:
            #         continue

            retain_list.append(ans)
            if len(retain_list) == K:
                break
        if(len(retain_list) == 0):
            continue
        if mode(retain_list) in now_correct:
            acc += 1
    return acc/len(test_retrievals)

def eval_accuracy_tune(val_retrievals, test_retrievals, v, K):
    url_count = {}
    for i in val_retrievals:
        count_dict = [group(url) for url in i['retrieved_websites']]
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

    result_list = [] 
    for remove_rate in range(0, 10, 1):
        keep_dict = {}
        for url, acc, count in v_list:
            keep_dict[url] = 1
        
        sum = 0
        for i in v_list:
            if sum >= remove_rate * total_doc / 10:
                break
            keep_dict[i[0]] = 0
            sum += i[2]

        acc_dev = cal_acc(val_retrievals, keep_dict, K)
        acc_test = cal_acc(test_retrievals, keep_dict, K)
        result_list.append({"remove_rate": remove_rate, "acc_dev": acc_dev, "acc_test": acc_test})

    result_list.sort(key=lambda x: x["acc_dev"], reverse=True)
    threshold = result_list[0]["remove_rate"]
    acc_dev = result_list[0]["acc_dev"]
    acc_test = result_list[0]["acc_test"]

    return acc_test, acc_dev, threshold

def remove_acc(retrieval, remove_url, K):
    retain_list = []
    for i in range(len(retrieval['retrieved_websites'])):
        if(group(retrieval['retrieved_websites'][i]) == remove_url):
            continue
        retain_list.append(retrieval['generated_answers'][i])
        if len(retain_list) == 10:
            break
    if mode(retain_list) in retrieval['correct_answers']:
        return 1
    return 0

def cal_loo(retrievals, K):
    result = []
    url_count = {}

    for retrieval in retrievals:

        count_dict = [group(i) for i in retrieval['retrieved_websites']]
        url_dict = list(set(count_dict))

        clean_acc = remove_acc(retrieval, "www.do_not_remove.com", K)

        for url in url_dict:
            acc = remove_acc(retrieval, url, K)
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

def cal_acc_reweight_parallel(args):
    seed, test_set, retrievals, mapping, v, K, threshold, keep_all = args
    import numpy as np
    np.random.seed(seed)
    v_now = np.random.rand(len(v))
    
    acc = 0
    for i in test_set:
        now_url = retrievals[i]['retrieved_websites']
        now_ans = retrievals[i]['generated_answers']
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

def cal_acc_reweight(test_set, retrievals, mapping, v, K = 10, threshold = 0.5, keep_all = False): 
    from multiprocessing import Pool
    seed = [67, 86, 55, 13, 1, 38, 81, 8, 52, 79, 10, 19, 30, 66, 36, 39, 59, 2, 21, 68, 41, 24, 31, 76, 47, 91, 99, 63, 51, 65, 26, 61]
    # run cal_acc_reweight_parallel with 32 different processes with different random seed
    with Pool(32) as p:
        acc_list = p.map(cal_acc_reweight_parallel,[(seed[i], test_set, retrievals, mapping, v, K, threshold, keep_all) for i in range(32)])
    return sum(acc_list)/len(acc_list)

def experiment(random_seed, retrievals, K = 10):
    import random
    id_list = [i for i in range(len(retrievals))]
    random.seed(random_seed)
    random.shuffle(id_list)
    val_set = id_list[len(retrievals)//2:]
    test_set = id_list[:len(retrievals)//2]
    
    val_retrievals = [retrievals[i] for i in val_set]
    test_retrievals = [retrievals[i] for i in test_set]

    #compute the excution time of the algorithm
    encoded_retrievals, mapping = encode_retrievals(val_retrievals, "retrieved_websites", "generated_answers", utility)
    grouping, group_mapping = encode_groups(mapping, group)
    v = learn_importance(encoded_retrievals, k=K, learning_rate=100, num_steps=50, n_jobs=-1, grouping=grouping)
    group_importances = v_grouped(v, grouping, group_mapping)    

    val_accuracy = eval_accuracy(val_retrievals, k=K)
    test_accuracy = eval_accuracy(test_retrievals, k=K)
    test_accuracy_reweight = cal_acc_reweight(test_set, retrievals, group_mapping, group_importances, K)
    test_accuracy_thresholded, validation_accuracy_thresholded, threshold = eval_accuracy_tune(val_retrievals, test_retrievals, group_importances, K) 
    
    loo = cal_loo(val_retrievals, K)
    test_loo_accuracy, validation_loo_accuracy, threshold_loo = eval_accuracy_tune(val_retrievals, test_retrievals, loo, K)
    
    print("%.2f %.2f %.2f %.2f %.2f %d %.2f %d "%(val_accuracy, validation_accuracy_thresholded, test_accuracy, test_accuracy_reweight, test_accuracy_thresholded, threshold, test_loo_accuracy, threshold_loo))
    return test_accuracy, test_accuracy_thresholded, threshold, test_loo_accuracy, threshold_loo, val_accuracy, validation_accuracy_thresholded, test_accuracy_reweight

def run_experiment(dataset, target, llm, K):

    trainset = pd.read_csv(f'applications/imputation/data/{dataset}/train.csv')
    validset = pd.read_csv(f'applications/imputation/data/{dataset}/valid.csv')
    testset = pd.read_csv(f'applications/imputation/data/{dataset}/test.csv')

    valid_answers = pd.read_csv(f'applications/imputation/answers/{dataset}_{llm}/valid.csv')
    test_answers = pd.read_csv(f'applications/imputation/answers/{dataset}_{llm}/test.csv')
    train_answers = pd.read_csv(f'applications/imputation/answers/{dataset}_{llm}/train.csv')

    validset_retrievals = create_retrievals(target, validset, valid_answers)
    testset_retrievals = create_retrievals(target, testset, test_answers)
    trainset_retrievals = create_retrievals(target, trainset, train_answers)
    
    retrieval = []
    retrieval.extend(validset_retrievals)
    retrieval.extend(testset_retrievals)
    retrieval.extend(trainset_retrievals)

    result_list = []
    for random_seed in [441, 1, 469, 53, 280, 123, 219, 181, 5, 9, 199, 156, 93, 313, 28, 56, 359, 108, 8, 58, 407, 451, 322, 266, 268, 297, 12, 182, 320, 474, 296, 142, 64, 201, 32, 392, 98, 242, 344, 438, 427, 35, 77, 394, 39, 55, 330, 38, 67, 358, 237, 149, 405, 420, 411, 57, 488, 49, 42, 155, 109, 73, 331, 128]:
    # for random_seed in [156, 93, 313, 28]:
        result_list.append(experiment(random_seed, retrieval, K = 10))
    
    test_accuracy = sum([i[0] for i in result_list])/len(result_list)
    test_accuracy_thresholded = sum([i[1] for i in result_list])/len(result_list)
    threshold = sum([i[2] for i in result_list])/len(result_list)
    test_loo_accuracy = sum([i[3] for i in result_list])/len(result_list)
    threshold_loo = sum([i[4] for i in result_list])/len(result_list)
    val_accuracy = sum([i[5] for i in result_list])/len(result_list)
    validation_accuracy_thresholded = sum([i[6] for i in result_list])/len(result_list)
    test_accuracy_reweight = sum([i[7] for i in result_list])/len(result_list)


    print(dataset, target, llm, test_accuracy, test_accuracy_reweight, test_accuracy_thresholded, threshold, test_loo_accuracy, threshold_loo)
    return test_accuracy, test_accuracy_thresholded, threshold, test_loo_accuracy, threshold_loo, val_accuracy, validation_accuracy_thresholded, test_accuracy_reweight

if __name__ == '__main__':
    
    with open("./test_data/result/imputation_experiment_64_100_50.jsonl", "w") as f:
        test_accuracy_buy, test_accuracy_thresholded_buy, threshold_buy, test_loo_accuracy_buy, threshold_loo_buy, val_accuracy_buy, validation_accuracy_thresholded_buy, test_accuracy_reweight_buy = run_experiment("buy", "manufacturer", "gptjt6b", 10)
        f.write(json.dumps({"dataset": "buy", "target": "manufacturer", "llm": "gptjt6b", "test_accuracy": test_accuracy_buy, "test_accuracy_thresholded": test_accuracy_thresholded_buy, "threshold": threshold_buy, "test_loo_accuracy": test_loo_accuracy_buy, "threshold_loo": threshold_loo_buy}) + "\n")
        test_accuracy_rest, test_accuracy_thresholded_rest, threshold_rest, test_loo_accuracy_rest, threshold_loo_rest, val_accuracy_rest, validation_accuracy_thresholded_rest, test_accuracy_reweight_rest = run_experiment("restaurant", "city", "gptjt6b", 10)
        f.write(json.dumps({"dataset": "restaurant", "target": "city", "llm": "gptjt6b", "test_accuracy": test_accuracy_rest, "test_accuracy_thresholded": test_accuracy_thresholded_rest, "threshold": threshold_rest, "test_loo_accuracy": test_loo_accuracy_rest, "threshold_loo": threshold_loo_rest}) + "\n")

        print(tabulate([
            ('buy', val_accuracy_buy, validation_accuracy_thresholded_buy, 0.846, test_accuracy_buy, test_loo_accuracy_buy, test_accuracy_reweight_buy, test_accuracy_thresholded_buy),
            ('restaurant', val_accuracy_rest, validation_accuracy_thresholded_rest, 0.709, test_accuracy_rest, test_loo_accuracy_rest, test_accuracy_reweight_rest, test_accuracy_thresholded_rest),       
            ], headers=['task', 'jt+retr (val)', 'jt+retr+clean (val)', 'GPT-3 0-shot (test)', 
                        'jt+retr (test)', 'jt+retr+loo (test)', 'jt+retr+reweight (test)', 'jt+retr+clean (test)']))

