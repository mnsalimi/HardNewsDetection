import pickle
import random
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_most_similar_text(target):
    file_path = "train.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter=",", skiprows=1)
    results = []
    for index, row in df.iterrows():
        if row[2] != target:
            title = row[1]
            text = row[2]
            similarity_score = fuzz.ratio(title, target)
            results.append((title + '\n' + text[:300], row[-1], similarity_score))
            # results.append((title, row[-1], similarity_score))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:4]

class SBERT:
    def __init__(self):
        self.model_name = 'embaas/sentence-transformers-e5-large-v2'
        self.model = SentenceTransformer(self.model_name)
        try:
            with open('data/sbert/{}_test_fa_embeddings.pickle'.format(self.model_name.replace('/', '-')), 'rb') as f:
                self.test_fa_embeddings = pickle.load(f)
            with open('data/sbert/{}_train_fa_embeddings.pickle'.format(self.model_name.replace('/', '-')), 'rb') as f:
                self.train_fa_embeddings = pickle.load(f)

            self.positive_train_fa_embeddings = {
                x: y
                for x, y in self.train_fa_embeddings.items()
                if y[1]==1
            }
            self.negative_train_fa_embeddings = {
                x: y
                for x, y in self.train_fa_embeddings.items()
                if y[1]==0
            }
        except:
            print('ERRROR in loading sbert embeddings')

    def encode_docs_to_pickle(self, datas, path):
        new_sentnece_embeddings = {}
        try:
            with open(path, 'rb') as f:
                pickle_embeddings_dict = pickle.load(f)
        except:
            pickle_embeddings_dict = {}
            print('exept')
        i = 0
        for data in datas:
            if data[0] not in pickle_embeddings_dict:
                new_sentnece_embeddings[data[0]] =\
                    (self.model.encode(data[0]), data[1])
            if i % 100 == 0:
                print('number {} finished'.format(i))
            i += 1
        pickle_embeddings_dict = {**pickle_embeddings_dict, **new_sentnece_embeddings}
        with open(path, 'wb') as f:
            pickle.dump(pickle_embeddings_dict, f)

    def get_similarity(self, target, k, balance=True):
        if target not in self.test_fa_embeddings:
            print('target not in self.test_fa_embeddings')
            target_embedding = self.model.encode(target)
        else:
            target_embedding = self.test_fa_embeddings[target][0],
        similarity_scores = util.cos_sim(
            target_embedding,
            [item[0] for item in list(self.train_fa_embeddings.values())]
        )

        similarity_scores_np = similarity_scores.numpy().flatten()
        most_similar_indices = similarity_scores_np.argsort()[-k*20 if balance else -k:][::-1]
        keys_list = list(self.train_fa_embeddings.keys())
        values_list = list(self.train_fa_embeddings.values())
        if balance:
            docs = [(keys_list[index], values_list[index][1]) for index in  most_similar_indices]
            selected_docs_0 = []
            selected_docs_1 = []
            for x, y in docs:
                if y == 1:
                    selected_docs_1.append((x, y))
                    if len(selected_docs_1) == int(k/2):
                        break
            
            for x, y in docs:
                if y == 0:
                    selected_docs_0.append((x, y))
                    if len(selected_docs_0) == int(k/2):
                        break
            
            combined_docs = selected_docs_1 + selected_docs_0
            random.shuffle(combined_docs)
            return combined_docs
        else :
            return [(keys_list[index], values_list[index][1]) for index in  most_similar_indices]



def get_k_most_similar_texts_by_tfidf(target_text, texts, k=5):
    texts = []
    file_path = "data/train.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t", skiprows=1)
    for index, row in df.iterrows():
        texts.append((row[1], row[4]))

    # Initialize the vectorizer to include unigrams, bigrams, and trigrams
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    text_vectors = vectorizer.fit_transform([text[0] for text in texts] + [target_text])

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(text_vectors[-1], text_vectors[:-1])
    cosine_similarities = cosine_similarities[0]  # Extract the first row from the 2D array

    # Get indices of top k similar texts
    top_indices = cosine_similarities.argsort()[::-1][:k]

    # Return the top k similar texts and their similarities
    results = [(texts[i][0], texts[i][1], cosine_similarities[i]) for i in top_indices]
    return results


def get_k_most_similar_texts_randomly(target_text, texts, k=5):
    texts = []
    file_path = "data/train.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t", skiprows=1)
    for index, row in df.iterrows():
        texts.append((row[1], row[4]))
    indices = random.sample(range(0, len(df)), k)
    results = [(texts[i][0], texts[i][1]) for i in indices]
    return results

# Example usage:
# target_text = "Your target text goes here."
# texts = [
#     "First Persian text.",
#     "Second Persian text.",
#     "Third Persian text.",
#     # Add more texts as needed
# ]

# k = 5
# similar_texts = get_k_most_similar_texts(target_text, texts, k)
# for text, similarity in similar_texts:
#     print(f"Similarity: {similarity:.2f}\n{text}\n")

if __name__ == '__main__':
    sbert = SBERT()
    file_paths = {
        "data/test.csv":
            'data/sbert/{}_test_fa_embeddings.pickle'.format(sbert.model_name.replace('/', '-')),
        "data/train.csv":
            'data/sbert/{}_train_fa_embeddings.pickle'.format(sbert.model_name.replace('/', '-')),
    }
    # for x, y in file_paths.items():
    #     df = pd.read_csv(x, on_bad_lines='skip', delimiter="\t")
    #     sbert.encode_docs_to_pickle(list(zip(df['title'], df['tag'])), y)
    res = sbert.get_similarity('مهران مدیری', k=5)
    print(res)
    # from sentence_transformers import SentenceTransformer

    # Load the model (replace 'E5' with the actual model name if it's different)
    # from sentence_transformers import SentenceTransformer
    # sentences = ["This is an example sentence", "Each sentence is converted"]

    # model = SentenceTransformer('')
    # embeddings = model.encode(sentences)
    # print(embeddings)
