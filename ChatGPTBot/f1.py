import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.metrics import f1_score
import random


def cacl_f1(label, num_of_data, df, num_experiments_for_random_classifier):
    fs = []
    print("y_pred is:", label)
    for i in range(num_experiments_for_random_classifier if label=='random_tag' else 1):
        if label == "random_tag":
            for i in range(num_of_data):
                k = random.randint(0, 1)
                df['random_tag'][i] = '۱' if k == 1 else '۰'
        df[label] = df[label].apply(lambda x: 1 if x in ['۱', 'مثبت'] else 0)
        df.dropna(subset=['tag'], inplace=True)
        f1 = f1_score(df['tag'], df[label])
        # print("F1 Score:", f1)
        fs.append(f1)
    print("average f1:" if label == 'random_tag' else "f1:", sum(fs)/len(fs))
    if label == 'random_tag':
        print("best f1:", max(fs))
        print("min f1:", min(fs))
        print(
                df['tag'].value_counts()[1] /
                (df['tag'].value_counts()[0] + df['tag'].value_counts()[1])
            )
    print()


df = pd.read_csv("test.csv", on_bad_lines='skip', delimiter="\t")
df = df.drop('text', axis=1)
df = df.assign(random_tag=None)
num_experiments_for_random_classifier = 1000
num_of_data = 27
num_of_data = num_of_data if num_of_data < len(df) else len(df) 
labels = ['chatgpt_prompt1_tag', 'chatgpt_prompt2_tag', 'chatgpt_prompt3_tag', 'chatgpt_prompt4_tag', 'random_tag']
print("num_of_data", num_of_data)

df = df[:num_of_data]
for label in labels:
    cacl_f1(label, num_of_data, df, num_experiments_for_random_classifier)