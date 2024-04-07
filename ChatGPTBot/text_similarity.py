import pickle
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
        self.model_name = 'all-mpnet-base-v2'
        self.model = SentenceTransformer(self.model_name)
        with open('data/sbert/{}_test_fa_embeddings.pickle'.format(self.model_name), 'rb') as f:
            self.test_fa_embeddings = pickle.load(f)
        with open('data/sbert/{}_train_fa_embeddings.pickle'.format(self.model_name), 'rb') as f:
            self.train_fa_embeddings = pickle.load(f)

    def encode_docs_to_pickle(self, datas, path):
        new_sentnece_embeddings = {}
        try:
            with open(path, 'rb') as f:
                pickle_embeddings_dict = pickle.load(f)
        except:
            pickle_embeddings_dict = {}
            print('exept')
        for data in datas:
            if data[0] not in pickle_embeddings_dict:
                new_sentnece_embeddings[data[0]] =\
                    (self.model.encode(data[0]), data[1])
        pickle_embeddings_dict = {**pickle_embeddings_dict, **new_sentnece_embeddings}
        with open(path, 'wb') as f:
            pickle.dump(pickle_embeddings_dict, f)

    def get_similarity(self, target, k):
        if target not in self.test_fa_embeddings:
            print('target not in self.test_fa_embeddings')
            target_embedding = self.model.encode(target)
        else:
            target_embedding = self.test_fa_embeddings[target][0],
        # print(target)
        # print(type(target_embedding))
        # print(len([item[0] for item in list(self.train_fa_embeddings.values())]))
        # print(type([item[0] for item in list(self.train_fa_embeddings.values())]))
        similarity_scores = util.cos_sim(
            target_embedding,
            [item[0] for item in list(self.train_fa_embeddings.values())]
        )
        # for x, y in self.train_fa_embeddings.items():
        #     print(x, y)
        #     exit()
        similarity_scores_np = similarity_scores.numpy().flatten()

        most_similar_indices = similarity_scores_np.argsort()[-k:][::-1]
        keys_list = list(self.train_fa_embeddings.keys())
        values_list = list(self.train_fa_embeddings.values())
        return [(keys_list[index], values_list[index][1]) for index in  most_similar_indices]


def get_k_most_similar_texts(target_text, texts, k=5):
    texts = []
    file_path = "data/train.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter=",", skiprows=1)
    for index, row in df.iterrows():
        texts.append((row[1], row[-1]))

    vectorizer = TfidfVectorizer()
    text_vectors = vectorizer.fit_transform([text[0] for text in texts] + [target_text])
    
    # Calculate cosine similarity between target text and all other texts
    cosine_similarities = cosine_similarity(text_vectors[-1], text_vectors[:-1])
    cosine_similarities = cosine_similarities[0]  # cosine_similarities is a 2D array, we extract the first row
    
    # Get indices of top k similar texts
    top_indices = cosine_similarities.argsort()[::-1][:k]
    print(top_indices)
    # Return the top k similar texts and their similarities
    results = [(texts[i][0], texts[i][1], cosine_similarities[i]) for i in top_indices]
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
    file_path = "data/test.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
    path = 'data/sbert/{}_test_fa_embeddings.pickle'.format(sbert.model_name)
    # sbert.encode_docs_to_pickle(list(zip(df['title'], df['tag'])), path)
    res = sbert.get_similarity('مهران مدیری', k=5)
    print(res)