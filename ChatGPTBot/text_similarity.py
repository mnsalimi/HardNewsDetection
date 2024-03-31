import warnings
warnings.filterwarnings('ignore')
import pandas as pd

from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer

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
        pass
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    def encode_docs_to_pickle(self, docs):
        pass

    def get_similarity(self, setences, target):
        pass
        # Our sentences to encode
        sentences = [
            "This framework generates embeddings for each input sentence",
            "Sentences are passed as a list of string.",
            "The quick brown fox jumps over the lazy dog."
        ]

        # Sentences are encoded by calling model.encode()
        embeddings = self.model.encode(sentences)

        # Print the embeddings
        for sentence, embedding in zip(sentences, embeddings):
            print("Sentence:", sentence)
            print("Embedding:", embedding)
            print("")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_k_similar(input_doc, doc_set, k=5):
    # Create TfidfVectorizer object
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the input documents
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(doc_set)

    # Transform the input document
    input_doc_tfidf = tfidf_vectorizer.transform([input_doc])

    # Compute cosine similarity between input document and documents in the set
    similarities = cosine_similarity(input_doc_tfidf, tfidf_matrix_train)

    # Get indices of top k most similar documents
    top_indices = similarities.argsort()[0][-k:][::-1]

    return top_indices

# Example usage:
# input_doc = """
# واکنش کنسولگری ایران در استانبول به ریجکت شدن تتلو!

# """
# file_path = "train.csv"
# doc_set = df = [row[1] for index, row in pd.read_csv(file_path, on_bad_lines='skip', delimiter=",", skiprows=1).iterrows()]
# similarities = get_top_k_similar(input_doc, doc_set, 5)
# print(similarities)
# for idx, sim in enumerate(similarities):
#     print(f"Similarity with document {doc_set[idx+1]}: {sim}")
#     print()
    # print()
