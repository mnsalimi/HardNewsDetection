from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
import time, datetime
import pandas as pd
import random
import ast
import re

########### hyperparameters ############
sleep_time =  180
sleep_time2 = 180
sleep_time3 =  30
sleep_time4 = 15
words_limit = 900
page_flag = True
page_c = 1
total_pages = 39830
start_row = 640
################# log in to ChatGPT #################
chat_bot = ChatGPTAutomation(
    
    # chrome_path="/opt/google/chrome/chrome",
    # chrome_driver_path="/opt/chromedriver_linux64/chromedriver",
    username="sartakhti.salimi@gmail.com", # Optional
    # password="Help@Me2day"  # Optional
)


def send_prompt_get_transaltion(chat_bot, sleep_time, sleep_time2, cnt):
    remain_flag = False
    if len(cnt.split(" ")) > words_limit:
        print('exceed token limit: ', len(cnt.split(" ")))
        split_cnt = cnt.split(" ")
        cnt = ' '.join(split_cnt[:words_limit])
        chat_bot.check_response_status2(chat_bot, cnt)
        time.sleep(sleep_time)
        chat_bot.check_continue_generating()
        time.sleep(sleep_time2)
        trn_text = chat_bot.return_last_response()
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

def call_spgt_function(chat_bot, sleep_time, sleep_time2, cnt):
    translation_flag = False
    while not translation_flag:
        trn_text = send_prompt_get_transaltion(chat_bot, sleep_time, sleep_time2, cnt)
        if len(trn_text) <= 1:
            translation_flag = False
        else:
            translation_flag = True
    return trn_text


def translate():
    prompt1 = """
متن زیر را به انگلیسی ترجمه کن. 
"""
    file_path = "test.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
    start_row = df.index[df['title_tr'].isnull() | (df['title_tr'] == '')].tolist()[0]
    print(start_row)
    for i in range(start_row, int(len(df))):
        print(f"----------- starting row {i} -----------")
        prmpt = prompt1 + "عنوان متن:\n" + df["title"][i]  + ".\n\n" + "متن:\n" + df["text"][i]
            # ".\n\n" + "کلمات کلیدی:\n" + '، '.join(ast.literal_eval(df["tags"][i]))
        # answer_prompt = file["answer"][i]
        sleep1 = random.randint(4, 9)
        sleep2 = random.randint(4, 7)
        trn_text = call_spgt_function(chat_bot, sleep1, sleep2, prmpt).\
            replace('ChatGPT\n', "").replace("1 / 2", "")
        print('trn_text', trn_text)
        prompt_tr = re.findall(r'(Title:\n*)((?s).*)(Text:\n*)((?s).*)', trn_text)[0]
        tags_tr = [
            tag.strip()
            for tag in
            ', '.join(prompt_tr[5: ]).rstrip().lstrip().strip().split(',')
        ]
        title_tr = prompt_tr[1].rstrip().lstrip().strip()
        text_tr = prompt_tr[3].rstrip().lstrip().strip()
        prmpt = prompt1 + "کلمات کلیدی:\n" + '، '.join(ast.literal_eval(df["tags"][i]))
        trn_text = call_spgt_function(chat_bot, sleep1, sleep2, prmpt).\
            replace('ChatGPT\n', "").replace("1 / 2", "")
        tags = trn_text.replace('keywords:\n', '')
        print('tags', tags)
        tags = [tag.strip() for tag in tags.split(",")]
        print('tags', tags)
        # print('text_tr', text_tr)
        # print('tags_tr', tags_tr)
        df.loc[df.index[i], "title_tr"] = title_tr
        df.loc[df.index[i], "text_tr"] = text_tr
        df.loc[df.index[i], "tags_tr"] = str(tags_tr)
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
        print('saved at ' + str(datetime.datetime.now()))
        print("   * ----------------- row: ", i , " is translated -----------------\n")
    df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)

def importance_detection():
    prompt1 = """"
    هدف، داشتن یک دسته‌بند دودویی است که با گرفتن هر متن ورودی، کلاس آن را در خروجی مشخص می‌کند. کلاس‌ها شامل دو دسته‌ی مثبت یا منفی هستند. 

شرح تسک:
متن یا خبری را مهم یا تاثیرگذار می‌گوییم اگر که برای بیش‌تر کاربران فارسی‌زبان اهمیت بالایی داشته باشد. یا به عبارت دیگر، جمعیت بزرگی از ایرانیان مایل باشند که آن متن یا خبر را بخوانند و یا برای یکدیگر بفرستند.
در صورتی که متن ورودی مهم باشد، کلاس مثبت خواهد بود و در صورتی که مهم نباشد، کلاس منفی خواهد بود

برای متن زیر به صورت جداگانه و مستقل و تنها در یک واژه پاسخ بده که آیا متن 
مهم (تاثیرگذاری) حساب می‌شود یا خیر. (مثبت یا منفی):
    """
    
    
    prompt2 = """
    هدف، داشتن یک دسته‌بند دودویی است که با گرفتن هر متن ورودی، کلاس آن را در خروجی مشخص می‌کند. کلاس‌ها شامل دو دسته‌ی مثبت یا منفی هستند. 

شرح تسک:
متن یا خبری را مهم یا تاثیرگذار می‌گوییم اگر که برای بیش‌تر کاربران فارسی‌زبان اهمیت بالایی داشته باشد. یا به عبارت دیگر، جمعیت بزرگی از ایرانیان مایل باشند که آن متن یا خبر را بخوانند و یا برای یکدیگر بفرستند.
در صورتی که متن ورودی مهم باشد، کلاس مثبت خواهد بود و در صورتی که مهم نباشد، کلاس منفی خواهد بود
برخی از مفاهیم مهم عبارت‌اند از:
یارانه و سهام و مواردی که قرار است پول به مردم برسد مهم هستند
ثبت نام خونه و وام و... 
ثبت نام خودرو
افزایش و کاهش های شدید قیمت ارز یا تورم 

فرهنگی:
قانون های مهم برای همه مردم، مهم هستند

سیاسی:
اخبار جنگ، برجام، توافق های ایران، 
تحریم های ایران، 
خبرها جنگ منطقه‌ای مهم. 
عزل و نصب مقامات مهم. 
این‌ها همگی مهم هستند

حالا، برای متن زیر به صورت جداگانه و مستقل و تنها در یک واژه پاسخ بده که باتوجه به مفاهیمی که در بالا مطرح شد و قدرت استنتاجی که خودت داری، آیا متن 
مهم (تاثیرگذاری) حساب می‌شود یا خیر. (مثبت یا منفی):
    """
    
    prompt3 = """هدف، داشتن یک دسته‌بند دودویی است که با گرفتن هر متن ورودی، کلاس آن را در خروجی مشخص می‌کند. کلاس‌ها شامل دو دسته‌ی 1 یا 0 هستند. 1 یعنی خبر مهم است و 0 یعنی خبر مهم نیست.

شرح تسک:
متن یا خبری را مهم یا تاثیرگذار می‌گوییم اگر که برای بیش‌تر کاربران فارسی‌زبان اهمیت بالایی داشته باشد. یا به عبارت دیگر، جمعیت زیاد و بزرگی از ایرانیان مایل باشند که آن متن یا خبر را بخوانند و یا برای یکدیگر بفرستند. اگر خبری مربوط به یک قشر کوچک یا جامعه‌ی خاصی از کاربران باشد، آن خبر مهم نیست.
در صورتی که متن ورودی مهم باشد، کلاس 1 خواهد بود و در صورتی که مهم نباشد، کلاس 0 خواهد بود
برخی از مفاهیم مهم عبارت‌اند از:
یارانه و سهام و مواردی که قرار است پول به مردم برسد مهم هستند
ثبت نام مسکن و خانه و اخبار مربوط به وام‌ها و... 
ثبت نام خودرو
افزایش و کاهش های شدید و زیاد قیمت ارز یا طلا و سکه و یا تورم 

سیاسی:
اخبار جنگ، برجام، توافق های ایران، 
تحریم های ایران، 
خبرهای جنگ‌های بزرگ منطقه‌ای،
عزل و نصب مقامات بلندپایه ایرانی،
این‌ها همگی مهم هستند

ورزشی:
اخبار مربوط به تیم‌های معروف و پرطرفدار ایرانی و همین‌طور اروپایی مهم است

حالا، برای متن زیر به صورت جداگانه و مستقل و تنها در یک واژه پاسخ بده که باتوجه به مفاهیمی که در بالا مطرح شد و قدرت استنتاجی که خودت داری، آیا متن 
مهم (تاثیرگذاری) حساب می‌شود یا خیر. (1 یا 0):
'''
^^body^^
'''
با توجه به توضیحاتی که در بالا داده شد، این خبر مهم است و یا نه؟ (1 یا 0)؟ تنها در یک کلمه پاسخ بده
"""
    file_path = "test.csv"
    df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
    print(df)
    target_col = 'chatgpt_prompt3_tag'
    start_row = df.index[df[target_col].isnull() | (df[target_col] == '') | (df[target_col] == '--')].tolist()[0]
    for i in range(start_row, int(len(df))):
        print(f"----------- starting row {i} -----------")
        # prmpt = prompt2 + "\n" + df["title"][i]  + "\n" + df["text"][i]
        prmpt = prompt3.replace("^^body^^", df["title"][i]  + "\n" + df["text"][i])
        sleep1 = random.randint(4, 9)
        sleep2 = random.randint(4, 7)
        trn_text1 = call_spgt_function(chat_bot, sleep1, sleep2, prmpt).\
            replace('ChatGPT\n', "").replace("1 / 2", "").lstrip().rstrip().\
            strip()
        if len(trn_text1) >= 5:
            print("length response error. Content:", trn_text1)
            exit()
        print(trn_text1)
        df.loc[df.index[i], target_col] = trn_text1
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
        print('saved at ' + str(datetime.datetime.now()))
        print("   * ----------------- row: ", i , " is translated -----------------\n")
    df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)


if __name__ == "__main__":
    importance_detection()
    # translate()