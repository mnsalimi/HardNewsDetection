from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


########### hyperparameters ############
sleep_time = 60
sleep_time2 = 70
words_limit = 3000
page_flag = True
page_c = 2
total_pages = 39830
start_row = 0

################# log in to ChatGPT #################
chat_bot = ChatGPTAutomation(
    chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
    chrome_driver_path="C:/Users/marya/Downloads/chromedriver-win64/chromedriver.exe",
    username="<your email address to log in to Chatgpt>", # Optional
    password="<password>"  # Optional
)


################### translating content from pages of the dataset ##################
while(page_flag):
    file_path = "D:/dotin/test/" + "page"+str(page_c)+"_trn.xlsx"
    file = pd.read_excel(file_path)
    translated_cnt = []

    for i in range(start_row, int(len(file["repo"]))):
        print("Page: ", page_c, " row: ", i+1)
        cnt = file["modify_content"][i]
        split_cnt = cnt.split()
        if len(cnt)>words_limit:
            trn_text=""
            num_tran = len(cnt)//words_limit
            rem = len(cnt)%words_limit
            num_words = len(split_cnt)//num_tran
            rem_words = len(split_cnt)%num_tran
            print("len word: ", len(split_cnt), num_words)

            for j in range(num_tran):
                prompt = " ".join(split_cnt[j*num_words:(j+1)*num_words])
                chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+prompt)
                # chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+cnt[j*num_words:(j+1)*num_words])
                time.sleep(sleep_time)
                chat_bot.check_continue_generating()
                time.sleep(sleep_time2)
                trn_text = trn_text + chat_bot.return_last_response()
                print(i + 1, (j+1)*num_words)
            if rem_words!=0:
                print(i + 1, (num_tran)*num_words)
                prompt = " ".join(split_cnt[(num_tran)*num_words:])
                chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+prompt)
                # chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+cnt[(num_tran)*num_words:])
                time.sleep(sleep_time)
                chat_bot.check_continue_generating()
                time.sleep(sleep_time2)
                trn_text = trn_text + chat_bot.return_last_response()
        else:
            chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+ cnt)
            # chat_bot.send_prompt_to_chatgpt("translate this text to persian: "+ cnt)
            time.sleep(sleep_time)
            chat_bot.check_continue_generating()
            time.sleep(sleep_time2)
            # print(i+1)
            trn_text = chat_bot.return_last_response()
        translated_cnt.append(trn_text)
        file["persain_content"][start_row:i+1] = translated_cnt
        file.to_excel("page" + str(page_c) + "_trn.xlsx")

    if page_c > total_pages:
        page_flag = False
    else:
        page_c += 1

