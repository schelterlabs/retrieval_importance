import json
import tldextract
from pprint import pp
from retrieval_importance import learn_importance, encode_retrievals, encode_groups, v_grouped, \
    most_important_groups, least_important_groups
from retrieval_importance import cal_acc, generate_val_test_set, sort_values, get_retain_urls, cal_acc_reweight, cal_loo, load_retrievals, load_retrievals_new
from retrieval_importance.utils import get_project_root

def utility(retrieval, prediction):
    if prediction in retrieval["correct_answers"]:
        return 1.0
    else:
        return 0.0

def group(retrieved):    
    url_parts = tldextract.extract(retrieved)
    return f'{url_parts.domain}.{url_parts.suffix}'

def experiment_prune(random_seed, retrievals, K = 10, lr = 500, epoch = 50):
    val_set, test_set = generate_val_test_set(len(retrievals), random_seed)
    val_retrievals = [retrievals[i] for i in val_set]
    
    encoded_retrievals, mapping = encode_retrievals(val_retrievals, "retrieved_websites", "retrieved_answers", utility)
    grouping, group_mapping = encode_groups(mapping, group)
    v_ungrouped = learn_importance(encoded_retrievals, k=K, learning_rate=lr, num_steps=epoch, n_jobs=-1, grouping=grouping)
    v = v_grouped(v_ungrouped, grouping, group_mapping)

    v_dict = {}
    for i in val_retrievals:
        list = [group(j) for j in i["retrieved_websites"]]
        for id, j in enumerate(list):
            if j not in v_dict:
                v_dict[j] = [0, 0]
            rank, count = v_dict[j]
            v_dict[j] = [rank + id + 1, count + 1]

    for i in v_dict:
        v_dict[i] = [v[i], v_dict[i][1]]
    # sort the v_dict by first value, if same, sort by second value
    v_dict = sorted(v_dict.items(), key=lambda x: (-x[1][0], -x[1][1]))
    webs = v_dict
    # print(webs)

    

    v_sorted, total_doc = sort_values(retrievals, val_set, v, group)

    results = [] 
    for remove_rate in range(0, 10, 1):
        retain_urls = get_retain_urls(v_sorted, total_doc, remove_rate/10)
        acc_dev = cal_acc(val_set, retrievals, group, retain_urls, K)
        acc_test = cal_acc(test_set, retrievals, group, retain_urls, K)
        results.append((remove_rate/10, acc_dev, acc_test, retain_urls))

    acc_baseline = results[0][2]

    results.sort(key=lambda x: x[1], reverse=True)
    acc_best = results[0][2]
    threshold = results[0][0]
    webs = results[0][3]

    return acc_baseline, acc_best, threshold, webs

def work_load(relation_name, metric, senerio, model):
    retrievals = load_retrievals_new(relation_name, senerio, model)
    if senerio == "noise":
        # save the original retrievals
        with open(f"./test_data/noise_retrievals/{relation_name}_{model}_original.json", "w") as f:
            json.dump(retrievals, f)
    acc_baseline, acc_best, acc_threshold, webs = experiment_prune(0, retrievals)
    return acc_baseline, acc_best, acc_threshold, webs

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', type=str, default="prune", help='loo/reweight/prune')
    parser.add_argument('-s', type=str, default="raw", help='raw/fake/noise')
    parser.add_argument('-t', type=str, default="opt", help='model name')

    args = parser.parse_args()

    # relation = ['applies_to_jurisdiction', 'author', 'award_received', 'basic_form_of_government', 'capital', 'capital_of', 'composer', 'continent', 'country', 'country_of_citizenship', 'country_of_origin', 'creator', 'currency', 'developer', 'director', 'discoverer_or_inventor', 'drug_or_therapy_used_for_treatment', 'educated_at', 'employer', 'field_of_work', 'genetic_association', 'genre', 'has_part', 'head_of_government', 'head_of_state', 'headquarters_location', 'industry', 'influenced_by', 'instance_of', 'instrument', 'language_of_work_or_name', 'languages_spoken_written_or_signed', 'located_in_the_administrative_territorial_entity', 'location', 'location_of_discovery', 'location_of_formation', 'majority_opinion_by', 'manufacturer', 'measured_physical_quantity', 'medical_condition_treated', 'member_of', 'member_of_political_party', 'member_of_sports_team', 'movement', 'named_after', 'native_language', 'occupation', 'office_held_by_head_of_government', 'official_language', 'operating_system', 'original_language_of_film_or_TV_show', 'original_network', 'owned_by', 'part_of', 'participating_team', 'place_of_birth', 'place_of_death', 'position_held', 'position_played_on_team', 'programming_language', 'recommended_unit_of_measurement', 'record_label', 'religion', 'shares_border_with', 'stock_exchange', 'subclass_of', 'subsidiary', 'symptoms_and_signs', 'twinned_administrative_body', 'work_location']
    # relation = ['applies_to_jurisdiction', 'author', 'award_received', 'basic_form_of_government', 'capital', 'capital_of', 'composer']
    relation = ['author', 'award_received', 'basic_form_of_government', 'capital', 'composer']

    result_list = []    
    # with open("./test_data/result/qa_web_%s_%s.jsonl"%(args.s, args.m), "w") as f:
    with open("./test_data/result/qa_all_web_%s_%s_%s.jsonl"%(args.s, args.m, args.t), "w") as f:
        if args.m == "prune":
            for i in relation:
                acc_baseline, acc_prune, acc_threshold, webs = work_load(i, args.m, args.s, args.t)
                result_list.append((acc_baseline, acc_prune, acc_threshold))
                tmp = {'relation':i, 'acc_baseline':acc_baseline, 'acc_prune':acc_prune, 'acc_threshold':acc_threshold, 'webs':webs}
                print(i, acc_baseline, acc_prune, acc_threshold)
                f.write(json.dumps(tmp) + "\n")
                f.flush()
            acc_baseline = sum([i[0] for i in result_list])/len(result_list)
            acc_prune = sum([i[1] for i in result_list])/len(result_list)
            acc_threshold = sum([i[2] for i in result_list])/len(result_list)
            print("average", acc_baseline, acc_prune, acc_threshold)
            f.write(json.dumps({'relation':'average', 'acc_baseline':acc_baseline, 'acc_prune':acc_prune, 'acc_threshold':acc_threshold}) + "\n")
