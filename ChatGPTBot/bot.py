import re
import ast
import random
import pandas as pd
import time, datetime
from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
from text_similarity import get_k_most_similar_texts_by_tfidf
from text_similarity import get_k_most_similar_texts_randomly
from text_similarity import SBERT
from f1 import cacl_f1
import prompts

class ChatGPTBot:
    def __init__(self):
        self.sbert = SBERT()
        self.sleep_time1 = random.randint(1, 1)
        self.sleep_time2 = random.randint(1, 1)
        self.words_limit = 900
        self.chat_bot = ChatGPTAutomation(
            # chrome_path="/opt/google/chrome/chrome",
            # chrome_driver_path="/opt/chromedriver_linux64/chromedriver",
            # username="sartakhti.salimi@gmail.com", # Optional
            # password="Help@Me2day"  # Optional
        )


    def call_prompt(self, cnt):
        if len(cnt.split(" ")) > self.words_limit:
            print('exceed token limit: ', len(cnt.split(" ")))
            split_cnt = cnt.split(" ")
            cnt = ' '.join(split_cnt[:self.words_limit])
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(self.sleep_time1)
            self.chat_bot.check_continue_generating()
            time.sleep(self.sleep_time2)
            trn_text = self.chat_bot.return_last_response()
        else:
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(self.sleep_time1)
            self.chat_bot.check_continue_generating()
            time.sleep(self.sleep_time2)
            trn_text = self.chat_bot.return_last_response()
        return trn_text

    def run_gpt(self, cnt):
        translation_flag = False
        while not translation_flag:
            trn_text = self.call_prompt(cnt)
            if len(trn_text) <= 1:
                translation_flag = False
            else:
                translation_flag = True
        return trn_text

    def start_gpt(self, prompt, task='classification'):
        while True:
            # try:

                while True:
                    response = self.run_gpt(prompt).\
                        replace('ChatGPT\n', "").replace("1 / 2", "")
                    if task == 'classification':
                        response = response.replace('برچسب: ', '').strip()
                    response = response.strip()
                    if "limit of messages" in response:
                        print('limitation... Sleeping 100 Seconds')
                        print('res,:', response)
                        time.sleep(100)
                        continue
                    elif 'Response' in response and len(response) <= 20:
                        print('Two Responses from ChatGPT! Sleep 5 Seconds')
                        time.sleep(5)
                        continue
                    else:
                        print('response:', response)
                        print()
                        break
                break
            # except:
            #     print('Error in try except...')
            #     time.sleep(5)

        return response
        
    def translate(self):
        prompt1_body = """
    متن زیر را به انگلیسی ترجمه کن:
    '''
    body
    '''
    """
        prompt1_tag = """
    کلمات کلیدی زیر را به انگلیسی ترجمه کن:
    '''
    body
    '''
    """
        file_path = "data/train.csv"
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
        start_row = df.index[df['title_tr'].isnull() | (df['title_tr'] == '')].tolist()[0]
        print(start_row)
        for i in range(start_row, int(len(df))):
            print(f"----------- starting row {i} -----------")
            prmpt = prompt1_body.replace("body", df["title"][i]) 
            title = self.start_gpt(prmpt)
            prmpt = prompt1_body.replace("body", df["text"][i]) 
            text = self.start_gpt(prmpt)
            prmpt = prompt1_tag.replace('body', '، '.join(ast.literal_eval(df["tags"][i])))
            tags = self.start_gpt(prmpt)
            tags = [tag.strip() for tag in tags.split(",")]
            print()
            print('title', title)
            print('text', text)
            print('tags', tags)
            print()
            # print('text_tr', text_tr)
            # print('tags_tr', tags_tr)
            df.loc[df.index[i], "title_tr"] = title
            df.loc[df.index[i], "text_tr"] = text
            df.loc[df.index[i], "tags_tr"] = str(tags)
            df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
            print('saved at ' + str(datetime.datetime.now()))
            print("   * ----------------- row: ", i , " is translated -----------------\n")
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)

    labels = [
            'chatgpt_prompt4_tag',
            'chatgpt_prompt7_tag',
            'prompt_fa_kshot_tfidf',
            'prompt_fa_kshot_all_mpnet_base_v2',
            'prompt_fa_10shot_invserse_sample_with_tag_All_mpnet_base_v2',
            'prompt_fa_10shot_invserse_sample_with_tag_multi-qa-mpnet-base-dot-v1',
            'prompt_fa_10shot_invserse_sample_with_tag_embaas-entence-transformers-e5-large-v2',
            # 'prompt_fa_10shcot_invserse_sample_with_tag_all-distilroberta-v1',
            # 'prompt_fa_10shot_invserse_sample_with_tag_All_mpnet_base_v2_titletext_similarity',
            'prompt_fa_10shot_invserse_sample_with_tfidf_123gram_titletext_similarity',
            'prompt_texttags_fa_10shot_invserse_sample_with_tag_All_mpnet_base_v2',
            'prompt_fa_20shot_invserse_sample_with_tag_All_mpnet_base_v2',
            
            # 'prompt_fa_10shot_invserse_samples_balance_with_tag_All_mpnet_base_v2',
            # 'fa_imbalance_imbalance_10shot_invserse_samples',
            # 'random_tag'
        ]
    def importance_detection(self, lang="en"):
        kshot = 20
        file_path = "data/test.csv"
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
        target_col = self.labels[-1]
        print('target label:', target_col)
        if target_col not in df:
            df = df.assign(**{target_col: None})
            df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)

        start_row = df.index[df[target_col].isnull() | (df[target_col] == '') | (df[target_col] == '--')].tolist()[0]
        for i in range(start_row, int(len(df))):
            print(f"----------- starting row {i} -----------")
            new_prmpt = prompts.prompt_fa_kshot.replace(
                # "^^body^^",  df["title"][i] + '\n' + 'کلمات کلیدی خبر: ' + df["tags"][i] if lang == 'fa' else df["title_tr"][i]
                "^^body^^",  df["title"][i] if lang == 'fa' else df["title_tr"][i]
            )
            print(df["title"][i])
            texts = self.sbert.get_similarity(df["title"][i], kshot, balance=False)
            # texts = get_k_most_similar_texts_by_tfidf(k=kshot, target_text=df["title"][i]+'\n'+df["text"][i], texts=None)
            # texts = get_k_most_similar_texts_randomly(k=kshot, target_text=df["title"][i], texts=None)
            
            print("res", texts)
            if 'SAMPLES_HERE':
                sample_str = ''
                for _ in range(kshot):
                    sample_str += 'متن: {}\n' +\
                    'خروجی : {}\n'
                new_prmpt = new_prmpt.replace('SAMPLES_HERE', sample_str)
            samples = []
            for text in texts:
                samples.append(text[0])
                samples.append(text[0])
                samples.append(text[1])
            new_prmpt = new_prmpt.format(*samples)
            count = 0
            while True:
                
                trn_text1 = self.start_gpt(new_prmpt).\
                    replace('ChatGPT\n', "").replace("1 / 2", "").lstrip().rstrip().\
                    replace('برچسب: ', '').strip()
                if len(trn_text1) <= 5:
                    break
                elif "You've reached our limit of messages per 24 hours. Please try again later." == trn_text1:
                    print("jim")
                elif "limit of messages" in trn_text1:
                        print('Sleeping 100 Seconds')
                        print(trn_text1)
                        time.sleep(100)
                elif 'Response' in trn_text1:
                    print('Two Responses from ChatGPT! Sleep 5 Seconds')
                    time.sleep(5)
                else:
                    print("length response error. Content:", trn_text1)
                    print("end of message")
                    time.sleep(5)

                count += 1
                if count >= 3:
                    count = 0
                    break
            # with open('log.txt', 'a', encoding='utf-8') as f:
            #     f.write(str(i)+": " + str(sum([t[1] for t in texts])) + "\n{}\n\n".format(trn_text1))
            df.loc[df.index[i], target_col] = trn_text1
            df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
            [
                cacl_f1(label, i, df.copy()[:i+1], 1000)
                for label in self.labels
            ]
            # print('f1-macro:', f1)
            print("   * ----------------- row: ", i , 'saved at ' + str(datetime.datetime.now()) +"\n")
            print()
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)


if __name__ == "__main__":
    chat_gpt_bot = ChatGPTBot()
    chat_gpt_bot.translate()
    # chat_gpt_bot.importance_detection('fa')