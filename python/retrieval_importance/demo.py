import json
from dataclasses import dataclass
import tldextract
from retrieval_importance.retrieval_importance import learn_importance
from tqdm.notebook import tqdm
import os
import requests
import shelve
from abc import ABC, abstractmethod

from retrieval_importance import tune_pruning_threshold, grouped_weights, encode_groups, \
    encode_retrievals, mode


@dataclass
class Question:
    text: str
    correct_answers: list[str]


def load_wikifact_questions():

    with open('wikifact_place_of_birth_helm.json', 'r') as myfile:
        helm_json = json.loads(myfile.read())

    questions = []

    for request_state in helm_json['request_states']:

        text = request_state['instance']['input']
        correct_answers = []
        for reference in request_state['instance']['references']:
            correct_answers.append(reference['output'])

        questions.append(Question(text, correct_answers))

    return questions




class BingRetriever(ABC):

    def __init__(self, from_cache_only=False, max_results_per_query=50):
        self.subscription_key = os.getenv('BING_SUBSCRIPTION_KEY')
        self.from_cache_only = from_cache_only
        self.max_results_per_query = max_results_per_query

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.query_cache.close()

    def group(self, source):
        url_parts = tldextract.extract(source)
        return f'{url_parts.domain}.{url_parts.suffix}'

    def _search(self, query):

        try:
            query_cache = shelve.open('__bing_cache.pkl')

            if query in query_cache:
                return query_cache[query]
            elif self.from_cache_only:
                raise Exception(f'Query [{query}] not in cache, but we run in cache-only mode!')

            search_url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
            params = {
                "q": query,
                'count': self.max_results_per_query,
                'mkt': 'en-US',
                'setLang': 'en',
                'responseFilter': 'Webpages',
            }

            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()

            result = response.json()

            query_cache[query] = result

            return result

        finally:
            query_cache.close()



    @abstractmethod
    def create_query(self, prompt):
        pass

    def retrieve(self, prompt):

        query = self.create_query(prompt)
        result = self._search(query)

        return [(page['snippet'], page['url']) for page in result['webPages']['value']]



from manifest import Manifest
import re

class GPT35Generator(ABC):

#     FEW_SHOT_PROMPT = '''
# Jerry Beck (born February 9, 1955, in New York City) is an American animation historian, author, blogger, and video producer.Beck wrote or edited several books on classic American animation and classic characters.
# Jerry Beck was born in New York
#
# Ettore Maria Fizzarotti (1916–1985) was an Italian film director and screenwriter. Born in Naples, the son of the director Armando, he debuted as assistant director in the films of his father.
# Ettore Maria Fizzarotti was born in Naples
# '''

    def __init__(self):
        self.manifest = Manifest(
            client_name="openai",
            engine="text-davinci-003",
            cache_name="sqlite",
            cache_connection="manifest-cache.sqlite",
        )

    def generate(self, question, snippet=None):
        prompt = self._create_prompt(question, snippet)
        response = self.manifest.run(prompt, max_tokens=10, return_response=True)
        return self._extract_answer(response)

    @abstractmethod
    def _create_prompt(self, question, snippet):
        pass
#
#        if snippet is None:
#            return f"{self.FEW_SHOT_PROMPT}\n\n{question.text}"
#        else:
#            return f"{self.FEW_SHOT_PROMPT}\n\n{snippet}\n\n{question.text}"

    @abstractmethod
    def _extract_answer(self, response):
        pass
        # answer = response.get_response()
        #
        # answer = re.sub(r'[0-9]+', '', answer)
        # answer = answer.strip()
        #
        # if ',' in answer:
        #     answer = answer.split(',')[0]
        #
        # if '.' in answer:
        #     answer = answer.split('.')[0]
        #
        # answer = answer.strip()
        # return answer


def score_no_retrieval(test_questions, generator):

    num_correct = 0
    for test_question in tqdm(test_questions):

        answer = generator.generate(test_question)

        if answer in test_question.correct_answers:
            num_correct += 1

    accuracy = num_correct / len(test_questions)
    return accuracy


def score_with_retrieval_augmentation(test_questions, retriever, generator, k):
    num_correct = 0

    for test_question in tqdm(test_questions):

        results = retriever.retrieve(test_question.text)

        predictions = []
        for snippet, _ in results[:k]:
            answer = generator.generate(test_question, snippet)
            predictions.append(answer)

        if len(predictions) > 0:
            answer = mode(predictions)
        else:
            answer = ''

        if answer in test_question.correct_answers:
            num_correct += 1

    accuracy = num_correct / len(test_questions)
    return accuracy


def score_with_ragbooster(validation_questions, test_questions, retriever, generator, k):

    print('Computing validation corpus...')
    validation = validation_corpus(validation_questions, retriever, generator)

    print('Learning importance weights for data sources...')
    encoded_retrievals, mapping = encode_retrievals(validation, "retrieved_websites", "retrieved_answers", utility)
    grouping, group_mapping = encode_groups(mapping, retriever.group)

    weights = learn_importance(encoded_retrievals, k=k, learning_rate=10, num_steps=100, n_jobs=-1, grouping=grouping)
    domain_weights = grouped_weights(weights, grouping, group_mapping)

    percentile_range = range(0, 100, 5)

    print('Tuning threshold for corpus pruning...')
    # grouping could be used here as well
    tuning_result = tune_pruning_threshold(validation, domain_weights, percentile_range,
                                           utility, retriever.group, k, normalize=True)

    print('Computing pruned predictions...')
    num_correct = 0
    for test_question in tqdm(test_questions):

        predictions = []
        for snippet, url in retriever.retrieve(test_question.text):
            if len(predictions) < k:
                domain = retriever.group(url)
                if domain not in domain_weights or domain_weights[domain] >= tuning_result.best_threshold:

                    answer = generator.generate(test_question, snippet)
                    predictions.append(answer)

        if len(predictions) > 0:
            answer = mode(predictions)
        else:
            answer = ''

        if answer in test_question.correct_answers:
            num_correct += 1

    accuracy = num_correct / len(test_questions)
    return accuracy


def utility(retrieved, prediction):
    if prediction in retrieved["correct_answers"]:
        return 1.0
    else:
        return 0.0


def validation_corpus(questions, retriever, generator):

    corpus = []

    for question in tqdm(questions):

        retrieved_answers = []
        retrieved_websites = []

        for snippet, url in retriever.retrieve(question.text):
            retrieved_websites.append(url)
            answer = generator.generate(question, snippet)
            retrieved_answers.append(answer)

        corpus.append({
            'question': question.text,
            'correct_answers': question.correct_answers,
            'retrieved_answers': retrieved_answers,
            'retrieved_websites': retrieved_websites,
        })

    return corpus
