from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

import json
import pickle
import csv
import os 
import argparse

def get_template(relation_name):
    file_name = "./datasets/template_old.pkl"
    with open(file_name, "rb") as fIn:
        stored_data = pickle.load(fIn)
        results = stored_data["template"]
    return results[relation_name]

def inject_noise(text, ans_list, noise):
    for i in ans_list:
        text = text.replace(i, noise)
    return text 

def get_model_and_tokenizer(args, device):
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model_name, low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
    model.to(device)
    return model, tokenizer

def generate_answer(text, model, tokenizer, device):
    encodings_dict = tokenizer(text, padding="longest", return_tensors="pt")
    input_ids = encodings_dict['input_ids'].clone().detach().to(device)
    outputs = model.generate(input_ids, max_new_tokens=args.max_new_tokens, pad_token_id=tokenizer.eos_token_id, temperature=args.temperature, top_p=args.top_p)
    output_string = tokenizer.batch_decode(outputs[:,input_ids.shape[1]:])
    ret = [i.partition("\n")[0] for i in output_string]
    return ret

def answer_search(args):
    relation_name = args.relation
    dataset_file = "./wikifact/wikifact_k=5,subject=%s,model=together_gpt-neox-20b/scenario_state.json"%(relation_name)
    bing_file = "./datasets/bing_result/relation_%s_bing.pkl"%(relation_name)
    csv_save_file = "./datasets/inference_result_old/relation_%s_inference.csv"%(relation_name)

    device = "cuda:"+args.device_cuda if torch.cuda.is_available() else "cpu"
    model,tokenizer = get_model_and_tokenizer(args, device)
    print("Finish Loading the Model:", args.model_name)

    with open(dataset_file,'r') as load_f:
        load_dict = json.load(load_f)
    queries = {}
    prompts = {}
    labels = {}
    for id,i in enumerate(load_dict["request_states"]):
        queries["id_%s"%(id)] = i["instance"]["input"]
        prompts["id_%s"%(id)] = i["request"]["prompt"]
        right_label = []
        for j in i["instance"]['references']:
            if j['tags'][0] == 'correct':
                right_label.append(j['output'])
        labels["id_%s"%(id)] = right_label
    print("Finish Loading the WikiFact:", len(queries), relation_name)

    with open(bing_file, "rb") as fIn:
        stored_data = pickle.load(fIn)
        results = stored_data["results"]

    tempelate, noise_label = get_template(relation_name)

    prev_id = []
    if os.path.exists(csv_save_file):
        with open(csv_save_file) as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                prev_id.append(row[0])

    with open(csv_save_file, 'a') as f:
        writer = csv.writer(f)

        for i in results:
            if i in prev_id:
                continue
            try:
                clean_list = []
                dirty_list = []
                length = len(results[i]["webPages"]["value"])
                
                text = []
                for id, j in enumerate(results[i]["webPages"]["value"]):
                    clean_text = tempelate + j["snippet"] + "\n" + queries[i]
                    text.append(clean_text)
                    if (len(text) == args.batch_size) | (length == id + 1):
                        ret = generate_answer(text, model, tokenizer, device)
                        clean_list += ret
                        text = []

                text = []
                for id, j in enumerate(results[i]["webPages"]["value"]):
                    e = inject_noise(j["snippet"], labels[i], noise_label)
                    dirty_text = tempelate + e + "\n" + queries[i]
                    text.append(dirty_text)
                    if (len(text) == args.batch_size) | (length == id + 1):
                        ret = generate_answer(text, model, tokenizer, device)
                        dirty_list += ret
                        text = []
                
                text = [prompts[i], tempelate + "There is no passage about this.\n" + queries[i]]
                ret = generate_answer(text, model, tokenizer, device)
                
                clean_str = "^^^^$$$$^^^^".join(clean_list)
                dirty_str = "^^^^$$$$^^^^".join(dirty_list)
                row = [i, ret[0], ret[1], clean_str, dirty_str]
                writer.writerow(row)
                f.flush()
            except:
                continue

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--model_name', type=str, default="/nfs/iiscratch-zhang.inf.ethz.ch/export/zhang/export/xialyu/HF_model/GPT-JT-6B-v1", help='Currently supported {togethercomputer/GPT-JT-6B-v1}')

    parser.add_argument('-rel', '--relation', type=str, default="composer", help='enter the name of the relation to evaluate')

    parser.add_argument('-tmp', '--temperature', type=float, default=0.01, help='The temperature of the model sampling')
    parser.add_argument('-mnt', '--max_new_tokens', type=int, default=10, help='max number of new tokens to be generated')
    parser.add_argument('-top_p', type=float, default=0.9, help='top_p')
    parser.add_argument('--batch_size', type=int, default=6, help='the size of each batch')

    parser.add_argument('--device_cuda', type=str, default="0", help='the cuda device to be used')

    args = parser.parse_args()

    answer_search(args)
