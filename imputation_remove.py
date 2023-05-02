import pandas as pd
from tldextract import extract
from statistics import mode
from tabulate import tabulate
from retrieval_importance import learn_importance, encode_retrievals, encode_groups, v_grouped

def create_retrievals(trainset, target, test_or_valid_set, test_or_valid_answers):
    
    retrievals = []

    observed_labels = [label.lower() for label in trainset[target].unique()]

    for sample_index, row in test_or_valid_set.iterrows():

        retrieved_websites = []
        generated_answers = []

        raw_answers_for_sample = test_or_valid_answers[test_or_valid_answers.sample_index==sample_index]\
            .sort_values(by=['position'])

        for _, raw_answer in raw_answers_for_sample.iterrows():

            prediction = str(raw_answer.answer).lower()
            # use training label if predicted label is a substring
            for observed_label in observed_labels:
                if prediction in observed_label:
                    prediction = observed_label
                    break        

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

def run_experiment(dataset, target, llm, k, keep_unknown_sources):

    trainset = pd.read_csv(f'applications/imputation/data/{dataset}/train.csv')
    validset = pd.read_csv(f'applications/imputation/data/{dataset}/valid.csv')
    testset = pd.read_csv(f'applications/imputation/data/{dataset}/test.csv')

    valid_answers = pd.read_csv(f'applications/imputation/answers/{dataset}_{llm}/valid.csv')
    test_answers = pd.read_csv(f'applications/imputation/answers/{dataset}_{llm}/test.csv')
    
    validset_retrievals = create_retrievals(trainset, target, validset, valid_answers)
    encoded_retrievals, mapping = encode_retrievals(validset_retrievals, "retrieved_websites", 
                                                    "generated_answers", utility)
    grouping, group_mapping = encode_groups(mapping, group)

    v = learn_importance(encoded_retrievals, k=k, learning_rate=0.1, num_steps=500, n_jobs=-1, grouping=grouping)
    group_importances = v_grouped(v, grouping, group_mapping)    

    testset_retrievals = create_retrievals(trainset, target, testset, test_answers) 

    validation_accuracy = eval_accuracy(validset_retrievals, k=k)
    test_accuracy = eval_accuracy(testset_retrievals, k=k)

    test_accuracy_thresholded, validation_accuracy_thresholded, threshold = eval_accuracy_tune(validset_retrievals, testset_retrievals, group_importances, k) 
    
    loo = cal_loo(validset_retrievals, k)
    test_loo_accuracy, validation_loo_accuracy, threshold_loo = eval_accuracy_tune(validset_retrievals, testset_retrievals, loo, k)
    
    return validation_accuracy, validation_accuracy_thresholded, test_accuracy, test_accuracy_thresholded, threshold, validation_loo_accuracy, test_loo_accuracy, threshold_loo

if __name__ == "__main__":
    val_acc_buy, val_acc_clean_buy, test_acc_buy, test_acc_clean_buy, threshold_buy, val_loo_acc_buy, test_loo_acc_buy, loo_buy = run_experiment(
        dataset = 'buy',
        target = 'manufacturer',
        llm='gptjt6b',
        k=10,
        keep_unknown_sources=False,    
    )

    val_acc_rest, val_acc_clean_rest, test_acc_rest, test_acc_clean_rest, threshold_rest, val_loo_acc_rest, test_loo_acc_rest, loo_rest = run_experiment(
        dataset = 'restaurant',
        target = 'city',
        llm='gptjt6b',    
        k=10,
        keep_unknown_sources=False,    
    )

    print(tabulate([
    ('buy', val_acc_buy, val_loo_acc_buy, val_acc_clean_buy, 0.846, test_acc_buy, test_loo_acc_buy, test_acc_clean_buy),
    ('restaurant', val_acc_rest, val_loo_acc_rest, val_acc_clean_rest, 0.709, test_acc_rest, test_loo_acc_rest, test_acc_clean_rest),       
    ], headers=['task', 'jt+retr (val)', 'jt+retr+loo (val)', 'jt+retr+clean (val)', 'GPT-3 0-shot (test)', 
                'jt+retr (test)', 'jt+retr+loo (test)', 'jt+retr+clean (test)']))
        