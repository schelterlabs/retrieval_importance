import json
import tldextract
from pprint import pp
from retrieval_importance import learn_importance, encode_retrievals, encode_groups, v_grouped, \
    most_important_groups, least_important_groups
from retrieval_importance.utils import get_project_root

def utility(retrieval, prediction):
    if prediction in retrieval["correct_answers"]:
        return 1.0
    else:
        return 0.0

def group(retrieved):    
    url_parts = tldextract.extract(retrieved)
    return f'{url_parts.domain}.{url_parts.suffix}'

def majority_vote(retain_list):
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
    return max_ans

def remove_acc(retrieval, remove_url, K = 10):
    retain_list = []
    for i in range(len(retrieval['retrieved_websites'])):
        if(group(retrieval['retrieved_websites'][i]) == remove_url):
            continue
        retain_list.append(retrieval['retrieved_answers'][i])
        if len(retain_list) == 10:
            break
    max_ans = majority_vote(retain_list)
    if max_ans in retrieval['correct_answers']:
        return 1
    return 0

def cal_loo(retrievals):
    result = []
    url_count = {}

    for retrieval in retrievals:

        count_dict = [group(i) for i in retrieval['retrieved_websites']]
        url_dict = list(set(count_dict))

        clean_acc = remove_acc(retrieval, "www.do_not_remove.com")

        for url in url_dict:
            acc = remove_acc(retrieval, url)
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
    
    return url_dict, url_count

def cal_acc(test_set, retrievals, v, K): 
    acc = 0
    for i in test_set:
        now_url = retrievals[i]['retrieved_websites']
        now_ans = retrievals[i]['retrieved_answers']
        now_correct = retrievals[i]['correct_answers']
        
        retain_list = []
        for url, ans in zip(now_url, now_ans):
            
            if group(url) not in v:
                continue
            if v[group(url)] == 0:
                continue

            retain_list.append(ans)
            if len(retain_list) == K:
                break
        max_ans = majority_vote(retain_list)
        if max_ans in now_correct:
            acc += 1
    return acc/len(test_set)

def experiment(random_seed, retrievals, K = 10, threshold = 0.5):
    import random
    id_list = [i for i in range(len(retrievals))]
    random.seed(random_seed)
    random.shuffle(id_list)
    val_set = id_list[:len(retrievals)//2]
    test_set = id_list[len(retrievals)//2:]
    
    val_retrievals = [retrievals[i] for i in val_set]

    v = cal_loo(val_retrievals)

    #sort values in v to v_list
    v_list = []
    total_doc = 0
    for url in v[0]:
        v_list.append((url, v[0][url], v[1][url]))
        total_doc += v[1][url]
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

        acc_dev = cal_acc(val_set, retrievals, keep_dict, K)
        acc_test = cal_acc(test_set, retrievals, keep_dict, K)
        result_list.append((remove_rate, acc_dev, acc_test))

    acc_baseline = result_list[0][2]
    result_list.sort(key=lambda x: x[1], reverse=True)
    acc_best = result_list[0][2]
    threshold = result_list[0][0]

    print(acc_baseline, acc_best, threshold)
    return acc_baseline, acc_best, threshold

def work_load(relation_name):
    retrievals = []
    with open(f'{str(get_project_root())}/test_data/wikifact_url/{relation_name}.jsonl') as f:
        for line in f:
            retrievals.append(json.loads(line))

    result_list = []
    for random_seed in [441, 1, 469, 53, 280, 123, 219, 181, 5, 9, 199, 156, 93, 313, 28, 56, 359, 108, 8, 58, 407, 451, 322, 266, 268, 297, 12, 182, 320, 474, 296, 142, 64, 201, 32, 392, 98, 242, 344, 438, 427, 35, 77, 394, 39, 55, 330, 38, 67, 358, 237, 149, 405, 420, 411, 57, 488, 49, 42, 155, 109, 73, 331, 128]:
    # for random_seed in [441, 1, 469, 53, 280, 123, 219, 181, 5, 9, 199, 156, 93, 313, 28, 56]:
        result_list.append(experiment(random_seed, retrievals, K = 10, threshold = 0.5))
    
    acc_baseline = sum([i[0] for i in result_list])/len(result_list)
    acc_loo = sum([i[1] for i in result_list])/len(result_list)
    acc_threshold = sum([i[2] for i in result_list])/len(result_list)

    print(relation_name, acc_baseline, acc_loo, acc_threshold)

    return acc_baseline, acc_loo, acc_threshold

if __name__ == '__main__':
    r = ['applies_to_jurisdiction', 'author', 'award_received', 'basic_form_of_government', 'capital', 'capital_of', 'composer', 'continent', 'country', 'country_of_citizenship', 'country_of_origin', 'creator', 'currency', 'developer', 'director', 'discoverer_or_inventor', 'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 'field_of_work', 'genetic_association', 'genre', 'has_part', 'head_of_government', 'head_of_state', 'headquarters_location', 'industry', 'influenced_by', 'instance_of', 'instrument', 'language_of_work_or_name', 'languages_spoken_written_or_signed', 'located_in_the_administrative_territorial_entity', 'location', 'location_of_discovery', 'location_of_formation', 'majority_opinion_by', 'manufacturer', 'measured_physical_quantity', 'medical_condition_treated', 'member_of', 'member_of_political_party', 'member_of_sports_team', 'movement', 'named_after', 'native_language', 'occupation', 'office_held_by_head_of_government', 'official_language', 'operating_system', 'original_language_of_film_or_TV_show', 'original_network', 'owned_by', 'part_of', 'participating_team', 'place_of_birth', 'place_of_death', 'position_held', 'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 'religion', 'shares_border_with', 'stock_exchange', 'subclass_of', 'subsidiary', 'symptoms_and_signs', 'twinned_administrative_body', 'work_location']
    # r = ['author']
    result_list = []    
    with open("./test_data/result/wiki_remove_loo_64.jsonl", "w") as f:
        for i in r:
            acc_baseline, acc_loo, acc_threshold = work_load(i)
            result_list.append((acc_baseline, acc_loo, acc_threshold))
            tmp = {'relation':i, 'acc_baseline':acc_baseline, 'acc_loo':acc_loo, 'acc_threshold':acc_threshold}
            f.write(json.dumps(tmp) + "\n")
            f.flush()
            
        acc_baseline = sum([i[0] for i in result_list])/len(result_list)
        acc_loo = sum([i[1] for i in result_list])/len(result_list)
        acc_threshold = sum([i[2] for i in result_list])/len(result_list)
        print("average", acc_baseline, acc_loo, acc_threshold)
        f.write(json.dumps({'relation':'average', 'acc_baseline':acc_baseline, 'acc_loo':acc_loo,'acc_threshold':acc_threshold }) + "\n")

