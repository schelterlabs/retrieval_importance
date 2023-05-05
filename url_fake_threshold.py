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

    #compute the excution time of the algorithm
    encoded_retrievals, mapping = encode_retrievals(val_retrievals, "retrieved_websites", "retrieved_answers", utility)
    grouping, group_mapping = encode_groups(mapping, group)
    v_ungrouped = learn_importance(encoded_retrievals, k=K, learning_rate=500, num_steps=50, n_jobs=-1, grouping=grouping)
    v = v_grouped(v_ungrouped, grouping, group_mapping)

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
    # print(result_list)
    acc_baseline = result_list[0][2]
    result_list.sort(key=lambda x: x[1], reverse=True)
    acc_best = result_list[0][2]
    threshold = result_list[0][0]

    print(acc_baseline, acc_best, threshold)
    return acc_baseline, acc_best, threshold


def work_load(relation_name):
    retrievals = []
    with open(f'{str(get_project_root())}/test_data/wikifact_fake/{relation_name}.jsonl') as f:
        for line in f:
            retrievals.append(json.loads(line))

    result_list = []
    for random_seed in [441, 1, 469, 53, 280, 123, 219, 181, 5, 9, 199, 156, 93, 313, 28, 56, 359, 108, 8, 58, 407, 451, 322, 266, 268, 297, 12, 182, 320, 474, 296, 142, 64, 201, 32, 392, 98, 242, 344, 438, 427, 35, 77, 394, 39, 55, 330, 38, 67, 358, 237, 149, 405, 420, 411, 57, 488, 49, 42, 155, 109, 73, 331, 128]:
    # for random_seed in [441, 1, 469, 53, 280, 123, 219, 181, 5, 9, 199, 156, 93, 313, 28, 56]:
        result_list.append(experiment(random_seed, retrievals, K = 10, threshold = 0.5))
    
    acc_baseline = sum([i[0] for i in result_list])/len(result_list)
    acc_retrieval = sum([i[1] for i in result_list])/len(result_list)
    acc_threshold = sum([i[2] for i in result_list])/len(result_list)

    print(relation_name, acc_baseline, acc_retrieval, acc_threshold)

    return acc_baseline, acc_retrieval, acc_threshold

if __name__ == '__main__':
    r = ['applies_to_jurisdiction', 'author', 'award_received', 'basic_form_of_government', 'capital', 'capital_of', 'composer', 'continent', 'country', 'country_of_citizenship', 'country_of_origin', 'creator', 'currency', 'developer', 'director', 'discoverer_or_inventor', 'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 'field_of_work', 'genetic_association', 'genre', 'has_part', 'head_of_government', 'head_of_state', 'headquarters_location', 'industry', 'influenced_by', 'instance_of', 'instrument', 'language_of_work_or_name', 'languages_spoken_written_or_signed', 'located_in_the_administrative_territorial_entity', 'location', 'location_of_discovery', 'location_of_formation', 'majority_opinion_by', 'manufacturer', 'measured_physical_quantity', 'medical_condition_treated', 'member_of', 'member_of_political_party', 'member_of_sports_team', 'movement', 'named_after', 'native_language', 'occupation', 'office_held_by_head_of_government', 'official_language', 'operating_system', 'original_language_of_film_or_TV_show', 'original_network', 'owned_by', 'part_of', 'participating_team', 'place_of_birth', 'place_of_death', 'position_held', 'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 'religion', 'shares_border_with', 'stock_exchange', 'subclass_of', 'subsidiary', 'symptoms_and_signs', 'twinned_administrative_body', 'work_location']
    # r = ["author"]
    result_list = []    
    with open("./test_data/result/wiki_fake_threshold_64_500_50.jsonl", "w") as f:
        for i in r:
            acc_baseline, acc_retrieval, acc_threshold = work_load(i)

            result_list.append((acc_baseline, acc_retrieval, acc_threshold))

            tmp = {'relation':i, 'acc_baseline':acc_baseline, 'acc_retrieval':acc_retrieval, 'acc_threshold':acc_threshold}
            f.write(json.dumps(tmp) + "\n")
            f.flush()
        acc_baseline = sum([i[0] for i in result_list])/len(result_list)
        acc_retrieval = sum([i[1] for i in result_list])/len(result_list)
        acc_threshold = sum([i[2] for i in result_list])/len(result_list)
        print("average", acc_baseline, acc_retrieval, acc_threshold)
        f.write(json.dumps({'relation':'average', 'acc_baseline':acc_baseline, 'acc_retrieval':acc_retrieval, 'acc_threshold':acc_threshold}) + "\n")

