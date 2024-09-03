import json
import numpy as np

# File paths
file_paths = [
    './eval/helpful_base_eval_results.jsonl',
    './eval/harmless_base_eval_results.jsonl',
    './eval/helpful_online_eval_results.jsonl',
    './eval/helpful_rejection_eval_results.jsonl'
]

# Initialize list to aggregate all responses
all_responses = []

# Function to load responses from JSONL files
def load_responses(file_path):
    with open(file_path, 'r') as f:
        return [json.loads(line)['suffix'] for line in f]

# Load responses from all files
for path in file_paths:
    all_responses.extend(load_responses(path))

average_length = np.mean([len(response.split()) for response in all_responses])

def distinct_ngrams(responses, n):
    total_ngrams = 0
    unique_ngrams = set()
    for response in responses:
        tokens = response.split()
        ngrams = zip(*[tokens[i:] for i in range(n)])
        ngrams_list = list(ngrams)
        total_ngrams += len(ngrams_list)
        unique_ngrams.update(ngrams_list)
    return len(unique_ngrams) / total_ngrams if total_ngrams > 0 else 0

# Recompute Distinct-1, Distinct-2, and Distinct-3
distinct_1 = distinct_ngrams(all_responses, 1)
distinct_2 = distinct_ngrams(all_responses, 2)
distinct_3 = distinct_ngrams(all_responses, 3)

def distinctness(generations):
    unigrams, bigrams, trigrams = set(), set(), set()
    total_words = 0
    for gen in generations:
        o = gen.split(' ')
        total_words += len(o)
        unigrams.update(o)
        for i in range(len(o) - 1):
            bigrams.add(o[i] + '_' + o[i + 1])
        for i in range(len(o) - 2):
            trigrams.add(o[i] + '_' + o[i + 1] + '_' + o[i + 2])

    return len(unigrams) / total_words, len(bigrams) / total_words, len(trigrams) / total_words

# Calculate Distinct-1, Distinct-2, and Distinct-3 using distinctness
distinct_1, distinct_2, distinct_3 = distinctness(all_responses)

# Display the results
print(average_length, distinct_1, distinct_2, distinct_3)