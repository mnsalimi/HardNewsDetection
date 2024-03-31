import warnings
warnings.filterwarnings('ignore')
import pandas as pd

from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util

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
        self.model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    def encode_docs_to_pickle(self, docs):
        pass

    def get_similarity(self, setences=None, target=None):
        pass
        # Our sentences to encode
        sentences = [
            'مهران مدیری بازیگر ایرانی است که در اخرین فیبلمش نقش معتاد دارد',
            'مهران مدیری یک گاو است',
            'سلام',
        ]
        target_embedding = self.model.encode(target)

        # Encode input sentences
        sentence_embeddings = self.model.encode(sentences)

        # Compute cosine similarity between target and input sentences
        similarity_scores = util.cos_sim(target_embedding, sentence_embeddings)

        # Find the index of the most similar sentence
        most_similar_index = similarity_scores.argmax()

        # Print the most similar sentence and its cosine similarity score
        print("Target text:", target)
        print("Most similar sentence:", sentences[most_similar_index])
        print("Cosine similarity:", similarity_scores[most_similar_index])

# sbert = SBERT()
# sbert.get_similarity()
        
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_k_most_similar_texts(target_text, texts, k=5):
    texts = []
    file_path = "train.csv"
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
