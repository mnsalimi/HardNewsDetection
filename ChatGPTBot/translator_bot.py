from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


########### hyperparameters ############
sleep_time =  70
sleep_time2 = 70
sleep_time3 =  300
sleep_time4 = 70
words_limit = 3000
page_flag = True
page_c = 2
total_pages = 39830
start_row = 0
errors_path = "/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/common_errors.xlsx"
errors = pd.read_excel(errors_path)
err1, err2 = errors["error1"][0], errors["error2"][0]


################# log in to ChatGPT #################
chat_bot = ChatGPTAutomation(
    chrome_path="/opt/chrome-linux64/chrome",
    chrome_driver_path="/opt/chrome-driver/chromedriver",
    username="<myalsava@uwaterloo.ca>", # Optional
    password="<...>"  # Optional
)


def send_prompt_get_transaltion(chat_bot, words_limit, emain_flag, sleep_time, sleep_time2, sleep_time3, sleep_time4, cnt):
    if len(cnt) > words_limit:
        split_cnt = cnt.split()
        idx = [i for i, s in enumerate(split_cnt) if '<issue_comment>' in s]
        print("idx is: ", idx)
        prompt = ""
        pre_id = 0
        trn_text = ""
        for id in idx:
            nxt_prm = prompt + " ".join(split_cnt[pre_id:id + 1])
            print()
            if len(nxt_prm) < words_limit:
                if id == idx[-1]:
                    prompt = prompt + " ".join(split_cnt[pre_id:])
                    chat_bot.check_response_status2(chat_bot, prompt)
                    time.sleep(sleep_time)
                    chat_bot.check_continue_generating()
                    time.sleep(sleep_time2)
                    trn_text = trn_text + chat_bot.return_last_response()
                    prompt = " "
                    pre_id = 0
                else:
                    prompt = prompt + " ".join(split_cnt[pre_id:id + 1])
                    pre_id = id + 1
            else:

                if id == idx[-1]:
                    remain_flag = True
                if len(idx) != 1:
                    chat_bot.check_response_status2(chat_bot, prompt)
                    time.sleep(sleep_time3)
                    chat_bot.check_continue_generating()
                    time.sleep(sleep_time4)
                    trn_text = trn_text + chat_bot.return_last_response()
                    prompt = "" + " ".join(split_cnt[pre_id:id + 1])
                    pre_id = id + 1

        if remain_flag:
            prompt = prompt + " ".join(split_cnt[pre_id:])
            chat_bot.check_response_status2(chat_bot, prompt)
            time.sleep(sleep_time3)
            chat_bot.check_continue_generating()
            time.sleep(sleep_time4)
            trn_text = trn_text + chat_bot.return_last_response()
            prompt = " "
            pre_id = 0
            remain_flag = False

    else:
        chat_bot.check_response_status2(chat_bot, cnt)
        time.sleep(sleep_time)
        chat_bot.check_continue_generating()
        time.sleep(sleep_time2)
        trn_text = chat_bot.return_last_response()
    return trn_text


################### translating content from pages of the dataset ##################
while(page_flag):
    file_path = "/home/maryam/get_data_from_huggingface/data/" + "page"+str(page_c)+"_trn.csv"
    file = pd.read_excel(file_path)
    translated_cnt = []

    for i in range(start_row, int(len(file["repo"]))):
        print("Page: ", page_c, " row: ", i+1)
        cnt = file["modify_content"][i]
        split_cnt = cnt.split()
        remain_flag = False
        translation_flag = False
        while not translation_flag:
            trn_text = send_prompt_get_transaltion(chat_bot, words_limit, remain_flag, sleep_time, sleep_time2,
                                               sleep_time3, sleep_time4, cnt)
            if len(trn_text)<=1:
                translation_flag = False
            elif err1 in trn_text:
                translation_flag = False
            elif err2 in trn_text:
                translation_flag = False
            else:
                translation_flag = True

        translated_cnt.append(trn_text)
        file["persain_content"][start_row:i+1] = translated_cnt
        file.to_csv("D:/dotin/ChatGPTAutomation-master/page" + str(page_c) + "_trn.csv", encoding = "utf-8")

    if page_c > total_pages:
        page_flag = False
    else:
        page_c += 1

