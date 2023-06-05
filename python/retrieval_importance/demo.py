import json
from dataclasses import dataclass
import tldextract
from manifest import Manifest
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


class GPT35Generator(ABC):

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

    @abstractmethod
    def _extract_answer(self, response):
        pass


class RAGModel:

    def __init__(self, retriever, generator, k):
        self.retriever = retriever
        self.generator = generator
        self.k = k

    def generate(self, test_question):

        results = self.retriever.retrieve(test_question.text)

        predictions = []
        for snippet, _ in results[:self.k]:
            answer = self.generator.generate(test_question, snippet)
            predictions.append(answer)

        if len(predictions) > 0:
            answer = mode(predictions)
        else:
            answer = ''

        return answer


def score(test_questions, model):
    num_correct = 0
    for test_question in tqdm(test_questions, leave=False):

        answer = model.generate(test_question)

        if answer in test_question.correct_answers:
            num_correct += 1

    accuracy = num_correct / len(test_questions)
    return accuracy


class RAGBooster:

    def __init__(self, rag_model, validation_questions):
        self.rag_model = rag_model
        self._fit(validation_questions)

    def _utility(self, retrieved, prediction):
        if prediction in retrieved["correct_answers"]:
            return 1.0
        else:
            return 0.0

    def _fit(self, validation_questions):

        print('Computing validation corpus...')
        validation_corpus = []

        for question in tqdm(validation_questions, leave=False):

            retrieved_answers = []
            retrieved_websites = []

            for snippet, url in self.rag_model.retriever.retrieve(question.text):
                retrieved_websites.append(url)
                answer = self.rag_model.generator.generate(question, snippet)
                retrieved_answers.append(answer)

            validation_corpus.append({
                'question': question.text,
                'correct_answers': question.correct_answers,
                'retrieved_answers': retrieved_answers,
                'retrieved_websites': retrieved_websites,
            })

        print('Learning importance weights for data sources...')
        encoded_retrievals, mapping = encode_retrievals(validation_corpus, "retrieved_websites",
                                                        "retrieved_answers", self._utility)
        grouping, group_mapping = encode_groups(mapping, self.rag_model.retriever.group)

        # TODO these need to be class params
        weights = learn_importance(encoded_retrievals, k=self.rag_model.k, learning_rate=10, num_steps=100,
                                   n_jobs=-1, grouping=grouping)
        domain_weights = grouped_weights(weights, grouping, group_mapping)

        percentile_range = range(0, 100, 5)

        print('Tuning threshold for corpus pruning...')
        # grouping could be used here as well
        tuning_result = tune_pruning_threshold(validation_corpus, domain_weights, percentile_range,
                                               self._utility, self.rag_model.retriever.group,
                                               self.rag_model.k, normalize=True)

        print(f'Achieved accuracy of {tuning_result.best_utility:.3f} with a pruning threshold ' +\
              f'of {tuning_result.best_threshold:.5f} on the validation set.')

        self.weights = domain_weights
        self.tuning_result = tuning_result

    # TODO this could be nicer with a decorator over the retriever
    def generate(self, question):
        predictions = []
        for snippet, url in self.rag_model.retriever.retrieve(question.text):
            if len(predictions) < self.rag_model.k:
                domain = self.rag_model.retriever.group(url)
                if domain not in self.weights or \
                        self.weights[domain] >= self.tuning_result.best_threshold:

                    answer = self.rag_model.generator.generate(question, snippet)
                    predictions.append(answer)

        if len(predictions) > 0:
            answer = mode(predictions)
        else:
            answer = ''
        return answer

    def importance(self, source):
        source_group = self.rag_model.retriever.group(source)
        if source_group not in self.weights:
            return None
        else:
            return self.weights[source_group]
