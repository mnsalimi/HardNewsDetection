import pandas as pd

file1 = pd.read_csv("/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/common_errors.csv")
print(file1)
# file1[0:100].to_csv("sub_data.csv")
# file1 = pd.read_csv("/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/data_1.csv")
# t, b, a = [], [], []
# for i in range(len(file1)):
#     t.append(len(file1["tilte"][i])) 
#     a.append(len(file1["answer"][i]))
#     b.append(len(file1["body"][i]))
# print(max(t), " ", max(a), " ", max(b))
#     # title = file1["tilte"][0:5]
#     # body = file1["tilte"][0:5]
#     # answer = file1["answer"][0:5]
# dic = {"title": title, "body": body, "answer": answer}
# df = pd.DataFrame(dic)
# df.to_csv("/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/sub_data.csv")
# print(file1["tilte"][0:5])
# print(file1["body"][0])
# print(file1["answer"][0:5])

# ########### hyperparameters ############
# sleep_time = 60
# sleep_time2 = 70
# words_limit = 3000
# page_flag = True
# page_c = 3
# total_pages = 1
# start_row = 0


# ################### translating content from pages of the dataset ##################
# while(page_flag):
#     file_path = "/home/maryam/ChatGPTAutomation-master/ChatGPTAutomation-master/data_1.csv"
#     file = pd.read_csv(file_path)
#     translated_cnt = []
#     print("num rows: ", int(len(file)))
#     for i in range(start_row, 700):
#         print("Page: ", page_c, " row: ", i+1)
#         cnt = file["body"][i]
#         remain_flag = False

#         if len(cnt)>words_limit:
#             split_cnt = cnt.split()
#             idx = [i for i, s in enumerate(split_cnt) if "<p>" in s]
#             print("idx is: ", idx)
#             prompt = ""
#             pre_id = 0
#             for id in idx:
#                 print(id)
#                 nxt_prm = prompt + " ".join(split_cnt[pre_id:id + 1])
#                 if len(nxt_prm)<words_limit:
#                     if id==idx[-1]:
#                         prompt = prompt + " ".join(split_cnt[pre_id:])
#                         print("len last prm: ",len(prompt))
#                         print("send prompt last ", prompt )
#                         prompt = " "
#                         pre_id = 0

#                     else:
#                         prompt = prompt + " ".join(split_cnt[pre_id:id + 1])
#                         pre_id = id + 1
#                         print("len prm1: ", len(prompt))
#                 else:
#                     if id==idx[-1]:
#                         remain_flag = True
#                     if len(idx)!=1:
#                         print("prm len: ", len(prompt))
#                         print("send prompt ", prompt)
#                         print(pre_id , id + 1)
#                         prompt = "" + " ".join(split_cnt[pre_id :id + 1])
#                         pre_id = id + 1

#             if remain_flag:
#                 prompt = prompt + " ".join(split_cnt[pre_id:])
#                 print("len last prm: ", len(prompt))
#                 print("send prompt last ", prompt)
#                 prompt = " "
#                 pre_id = 0
#                 remain_flag = False

#         else:
#             print("send prompt ", len(cnt))

#     if page_c >= total_pages:
#         page_flag = False
#     else:
#         page_c += 1

