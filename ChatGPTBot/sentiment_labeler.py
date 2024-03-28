from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv


########### hyperparameters ############
sleep_time =  10
sleep_time2 = 10
num_prompts = 5
start_row = 0
errors_path = "/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/common_errors.csv"
errors = pd.read_csv(errors_path)
err1, err2 = errors["error1"][0], errors["error2"][0]
# print(err1, err2)
################# log in to ChatGPT #################
chat_bot = ChatGPTAutomation(
    chrome_path="/opt/chrome-linux64/chrome",
    chrome_driver_path="/opt/chrome-driver/chromedriver",
    username="<myalsava@uwaterloo.ca>", # Optional
    password="<...>"  # Optional
)


def send_prompt_get_transaltion(chat_bot, sleep_time, sleep_time2, cnt):
    chat_bot.check_response_status3(chat_bot, cnt)
    time.sleep(sleep_time)
    trn_text = chat_bot.return_last_response()
    return trn_text

def call_spgt_function(chat_bot, sleep_time, sleep_time2, cnt):
    translation_flag = False
    while not translation_flag:
        trn_text = send_prompt_get_transaltion(chat_bot, sleep_time, sleep_time2, cnt)
        if len(trn_text) <= 1:
            translation_flag = False
        elif err1 in trn_text:
            translation_flag = False
        elif err2 in trn_text:
            translation_flag = False
        else:
            translation_flag = True
    return trn_text


################### translating content from pages of the dataset ##################

file_path = "/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/chunk_1.csv"
output_file = "/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/chunk_1_labeled.csv"
file = pd.read_csv(file_path)
file = file.assign(bot_label=None)




with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
    fieldnames = ["comment", "bot_label"]
    writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
    
    writer.writeheader()  # Write header row

    title_cnt, body_cnt, answer_cnt = [], [], []
    k = 1
    title_prompt = ""
    for i in range(start_row, int(len(file))):
        # print(f"----------- starting row {i+1} -----------")
        title_prompt = "\n"+title_prompt  + str(k) + ". " + file["comment"][i] + "\n"
        k = k +1
        if i%num_prompts==0 and i!=0:
            k = 1
            trn_text1 = call_spgt_function(chat_bot, 15, 15, title_prompt)
            trn_text1 = trn_text1.replace("ChatGPT\n", "")
            trn_text1 = trn_text1.replace("\n", ",")
            labels = trn_text1.split(",")
            label = []
            for elm in labels:
                label.append(elm)
            title_prompt = "\n"
            for j in range(len(label)):
                # print(i, j, i-len(label)+1+j)
                row = {
                    "comment": file["comment"][i-len(label)+1+j],
                    "bot_label": label[j],
                }

                writer.writerow(row)
                print("   * ----------------- row: ", str(i-len(label)+1+j) , " is translated -----------------")


# # with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
# fieldnames = ["comment", "bot_label"]
# writer = pd.read_csv("/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/chunk_1_labeled.csv")


# title_cnt, body_cnt, answer_cnt = [], [], []
# label = list(writer["bot_label"][0:start_row])
# print(len(label))
# k = 1
# title_prompt = ""
# for i in range(start_row, int(len(file))):

#     title_prompt = "\n"+title_prompt  + str(k) + ". " + file["comment"][i] + "\n"
#     k = k +1
#     if i%num_prompts==0 and i!=0:
#         k = 1
#         trn_text1 = call_spgt_function(chat_bot, 15, 15, title_prompt)
#         trn_text1 = trn_text1.replace("ChatGPT\n", "")
#         trn_text1 = trn_text1.replace("\n", ",")

#         labels = trn_text1.split(",")
#         for elm in labels:
#             label.append(elm)
#         # print(len(label))
#         title_prompt = "\n"
    
#         row = {
#             "comment": file["comment"][0:i+1] ,
#             "bot_label": label,
#         }
#         df = pd.DataFrame(row)
#         df.to_csv(output_file)
#         #     writer.writerow(row)
#         print("   * -----------------up to row: ", i+1 , " is labeled -----------------")
#     # print(label)
