import pandas as pd
from hazm import Normalizer, stopwords_list, word_tokenize

def preprocess_text(text, normalizer, stopwords):
    """Normalize the text and remove stopwords using Hazm."""
    normalized_text = normalizer.normalize(text)
    tokens = word_tokenize(normalized_text)
    tokens = [word for word in tokens if word not in stopwords]
    return ' '.join(tokens)

def process_csv(input_filepath, output_filepath):
    # Load data
    df = pd.read_csv(input_filepath, on_bad_lines='skip', delimiter="\t")

    # Initialize the Hazm Normalizer and stopwords
    normalizer = Normalizer()
    persian_stopwords = set(stopwords_list())

    # Preprocess the 'title' and 'text' columns
    df['pre_title'] = df['title'].apply(lambda x: preprocess_text(x, normalizer, persian_stopwords))
    df['pre_text'] = df['text'].apply(lambda x: preprocess_text(x, normalizer, persian_stopwords))

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_filepath, index=False, sep='\t')
    print(f"Processed data saved to {output_filepath}")

# Example usage
input_csv = 'data/train.csv'
output_csv = 'data/train_pre.csv'
process_csv(input_csv, output_csv)
