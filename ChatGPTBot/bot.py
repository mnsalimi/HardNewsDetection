from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
import time, datetime
import pandas as pd
import random
import ast
import re
from text_similarity import get_k_most_similar_texts
from text_similarity import SBERT
from f1 import cacl_f1
import prompts

class ChatGPTBot:
    def __init__(self):
        self.sbert = SBERT()
        self.labels = [
            # 'chatgpt_prompt1_tag',
            # 'chatgpt_prompt2_tag',
            'chatgpt_prompt4_tag',
            # 'chatgpt_prompt6_tag',
            'chatgpt_prompt7_tag',
            'prompt_fa_kshot_tfidf',
            'prompt_fa_kshot_all_mpnet_base_v2',
            'prompt_fa_8shot_invserse_sample_with_tag_All_mpnet_base_v2',
            # 'random_tag'
        ]
        self.sleep_time1 = random.randint(1, 2)
        self.sleep_time2 = random.randint(1, 2)
        self.words_limit = 900
        self.page_flag = True
        self.page_c = 1
        self.total_pages = 39830
        self.start_row = 640
        ################# log in to ChatGPT #################
        self.chat_bot = ChatGPTAutomation(
            
            # chrome_path="/opt/google/chrome/chrome",
            # chrome_driver_path="/opt/chromedriver_linux64/chromedriver",
            # username="sartakhti.salimi@gmail.com", # Optional
            # password="Help@Me2day"  # Optional
        )


    def send_prompt_get_transaltion(self, cnt):
        remain_flag = False
        if len(cnt.split(" ")) > self.words_limit:
            print('exceed token limit: ', len(cnt.split(" ")))
            split_cnt = cnt.split(" ")
            cnt = ' '.join(split_cnt[:self.words_limit])
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(self.sleep_time1)
            self.chat_bot.check_continue_generating()
            time.sleep(self.sleep_time2)
            trn_text = self.chat_bot.return_last_response()
            if remain_flag:
                prompt = prompt + " ".join(split_cnt[pre_id:])
                self.chat_bot.check_response_status2(self.chat_bot, prompt)
                time.sleep(self.sleep_time1)
                self.chat_bot.check_continue_generating()
                time.sleep(self.sleep_time2)
                trn_text = trn_text + self.chat_bot.return_last_response()
                prompt = " "
                pre_id = 0
                remain_flag = False

        else:
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(self.sleep_time1)
            self.chat_bot.check_continue_generating()
            time.sleep(self.sleep_time2)
            trn_text = self.chat_bot.return_last_response()
        return trn_text

    def call_spgt_function(self, cnt):
        translation_flag = False
        while not translation_flag:
            trn_text = self.send_prompt_get_transaltion(cnt)
            if len(trn_text) <= 1:
                translation_flag = False
            else:
                translation_flag = True
        return trn_text

    def start_gpt(self, prompt, task='classification'):
        while True:
            try:

                while True:
                    response = self.call_spgt_function(prompt).\
                        replace('ChatGPT\n', "").replace("1 / 2", "")
                    if task == 'classification':
                        response = response.replace('برچسب: ', '').strip()
                    response = response.strip()
                    # if "You've reached our limit of messages per 24 hours. Please try again later" in response:
                    if "limit of messages" in response:
                        print('limitation... Sleeping 100 Seconds')
                        # print('24 H limitation... Sleeping 100 Seconds')
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
                        #     print("length response error. Content:", response)
                        #     print("end of message and exiting")
                        #     exit()
                        #     else:
                        break
                break
            except:
                print('Error in try except...')
                time.sleep(5)

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
        file_path = "train.csv"
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


    def importance_detection(self, lang="en"):
        kshot = 8
        file_path = "data/test.csv"
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
        print(df)
        target_col = 'prompt_fa_{}shot_invserse_sample_with_tag_All_mpnet_base_v2'.format(kshot)
        if target_col not in df:
            df = df.assign(label=lambda x: target_col)
        start_row = df.index[df[target_col].isnull() | (df[target_col] == '') | (df[target_col] == '--')].tolist()[0]
        for i in range(start_row, int(len(df))):
            print(f"----------- starting row {i} -----------")
            new_prmpt = prompts.prompt_fa_kshot.replace(
                "^^body^^",  df["title"][i]  if lang == 'fa' else df["title_tr"][i]
            )
            print(df["title"][i])
            texts = self.sbert.get_similarity(df["title"][i], 10)
            # texts = get_k_most_similar_texts(k=10, target_text=df["title"][i], texts=None)
            print("res", texts)
            if 'SAMPLES_HERE':
                sample_str = ''
                for _ in range(8):
                    sample_str += 'متن: {}\n' +\
                    'خروجی : {}\n'
                new_prmpt = new_prmpt.replace('SAMPLES_HERE', sample_str)
            samples = []
            for text in texts:
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
            df.loc[df.index[i], target_col] = trn_text1
            df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
            [
                cacl_f1(label, i, df.copy()[:i], 1000)
                for label in self.labels
            ]
            # print('f1-macro:', f1)
            print("   * ----------------- row: ", i , 'saved at ' + str(datetime.datetime.now()) +"\n")
            print()
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)


if __name__ == "__main__":
    chat_gpt_bot = ChatGPTBot()
    # chat_gpt_bot.translate()
    chat_gpt_bot.importance_detection('fa')