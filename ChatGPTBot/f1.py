import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.metrics import f1_score
import random


def cacl_f1(label, num_of_data, df, num_experiments_for_random_classifier):
    fs = []
    print(label)
    for i in range(num_experiments_for_random_classifier if label=='random_tag' else 1):
        if label == "random_tag":
            for i in range(num_of_data):
                k = random.randint(0, 1)
                df['random_tag'][i] = '۱' if k == 1 else '۰'
        df[label] = df[label].apply(lambda x: 1 if str(x) in ["1.0", '1', '۱', 'مثبت'] else 0)
        df.dropna(subset=['tag'], inplace=True)
        # print(df[label])
        # print(df["tag"])
        f1_macro = f1_score(df['tag'], df[label], average='macro')
        # f1_micro = f1_score(df['tag'], df[label], average='micro')
        # print("F1 Score:", f1)
        fs.append(f1_macro)
    print("average f1:" if label == 'random_tag' else "f1:", round(sum(fs)/len(fs), 4))
    if label == 'random_tag':
        print("best f1:", round(max(fs), 4))
        print("min f1:", round(min(fs), 4))
    # print(
    #     '1 to all ratio:',
    #         round(df[label].value_counts()[1] /
    #         (df[label].value_counts()[0] + df[label].value_counts()[1]), 4)
    #     )

if __name__ == "__main__":

    df = pd.read_csv("data/test.csv", on_bad_lines='skip', delimiter="\t")
    df = df.drop('text', axis=1)
    df = df.assign(random_tag=None)
    num_experiments_for_random_classifier = 1000
    num_of_data = 265
    num_of_data = num_of_data if num_of_data < len(df) else len(df) 
    labels = [
        'chatgpt_prompt4_tag',
        'chatgpt_prompt7_tag',
        # 'chatgpt_prompt6_tag',
        'prompt_fa_kshot_all_mpnet_base_v2',
    ]
    print("num_of_data", num_of_data)

    df = df[:num_of_data]
    for label in labels:
        cacl_f1(label, num_of_data, df, num_experiments_for_random_classifier)  