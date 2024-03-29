from chatgpt_automation.chatgpt_automation import ChatGPTAutomation
import time, datetime
import pandas as pd
import random
import ast
import re
class ChatGPTBot:
    def __init__(self):
        self.sleep_time =  180
        self.sleep_time2 = 180
        self.sleep_time3 =  30
        self.sleep_time4 = 15
        self.words_limit = 900
        self.page_flag = True
        self.page_c = 1
        self.total_pages = 39830
        self.start_row = 640
        ################# log in to ChatGPT #################
        self.chat_bot = ChatGPTAutomation(
            
            # chrome_path="/opt/google/chrome/chrome",
            # chrome_driver_path="/opt/chromedriver_linux64/chromedriver",
            username="sartakhti.salimi@gmail.com", # Optional
            # password="Help@Me2day"  # Optional
        )


    def send_prompt_get_transaltion(self, sleep_time, sleep_time2, cnt):
        remain_flag = False
        if len(cnt.split(" ")) > self.words_limit:
            print('exceed token limit: ', len(cnt.split(" ")))
            split_cnt = cnt.split(" ")
            cnt = ' '.join(split_cnt[:self.words_limit])
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(sleep_time)
            self.chat_bot.check_continue_generating()
            time.sleep(sleep_time2)
            trn_text = self.chat_bot.return_last_response()
            if remain_flag:
                prompt = prompt + " ".join(split_cnt[pre_id:])
                self.chat_bot.check_response_status2(self.chat_bot, prompt)
                time.sleep(self.sleep_time3)
                self.chat_bot.check_continue_generating()
                time.sleep(self.sleep_time4)
                trn_text = trn_text + self.chat_bot.return_last_response()
                prompt = " "
                pre_id = 0
                remain_flag = False

        else:
            self.chat_bot.check_response_status2(self.chat_bot, cnt)
            time.sleep(sleep_time)
            self.chat_bot.check_continue_generating()
            time.sleep(sleep_time2)
            trn_text = self.chat_bot.return_last_response()
        return trn_text

    def call_spgt_function(self, sleep_time, sleep_time2, cnt):
        translation_flag = False
        while not translation_flag:
            trn_text = self.send_prompt_get_transaltion(sleep_time, sleep_time2, cnt)
            if len(trn_text) <= 1:
                translation_flag = False
            else:
                translation_flag = True
        return trn_text

    def start_gpt(self, sleep1, sleep2, prompt):
        while True:
            response = self.call_spgt_function(sleep1, sleep2, prompt).\
                replace('ChatGPT\n', "").replace("1 / 2", "").\
                strip()
            if "limit of messages" in response:
                print('Sleeping 100 Seconds')
                time.sleep(100)
            elif 'Response' in response:
                print('Two Responses from ChatGPT! Sleep 5 Seconds')
                time.sleep(5)
            else:
                #     print("length response error. Content:", response)
                #     print("end of message and exiting")
                #     exit()
                #     else:
                break
        return response
        
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
        file_path = "test.csv"
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
        start_row = df.index[df['title_tr'].isnull() | (df['title_tr'] == '')].tolist()[0]
        print(start_row)
        for i in range(start_row, int(len(df))):
            print(f"----------- starting row {i} -----------")
            sleep1 = random.randint(4, 16)
            sleep2 = random.randint(4, 11)
            prmpt = prompt1_body.replace("body", df["title"][i]) 
            title = self.start_gpt(sleep1, sleep2, prmpt).\
                replace('ChatGPT\n', "").replace("1 / 2", "")
            prmpt = prompt1_body.replace("body", df["text"][i]) 
            text = self.start_gpt(sleep1, sleep2, prmpt).\
                replace('ChatGPT\n', "").replace("1 / 2", "")
            prmpt = prompt1_tag.replace('body', '، '.join(ast.literal_eval(df["tags"][i])))
            tags = self.start_gpt(sleep1, sleep2, prmpt).\
                replace('ChatGPT\n', "").replace("1 / 2", "")
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


    def importance_detection(self,):
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
        prompt4 = """

    هدف، داشتن یک دسته‌بند دودویی است که با گرفتن هر متن ورودی، کلاس آن را در خروجی مشخص می‌کند. کلاس‌ها شامل دو دسته‌ی 1 یا 0 هستند. 1 یعنی خبر مهم است و 0 یعنی خبر مهم نیست.

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
    فقط اخبار مربوط به تیم‌های معروف و پرطرفدار ایرانی و همین‌طور اروپایی مهم است
    حالا، برای متن زیر به صورت جداگانه و مستقل و تنها در یک واژه پاسخ بده که باتوجه به مفاهیمی که در بالا مطرح شد و قدرت استنتاجی که خودت داری، آیا متن 
    مهم (تاثیرگذاری) حساب می‌شود یا خیر. (1 یا 0):
    '''
    ^^body^^
    '''
    همچنین در نظر داشته باش که بیش‌تر خبرها مهم نیستند و خبرهای مهم در اقلیت هستند. بنابراین برای اینکه اعلام کنی خبری مهم هست یا نه، باید وسواس زیادی داشته باشی و باید حتما یکی از معیارهایی که در بالاتر توضیح داده شد را داشته باشد. حال با توجه به توضیحاتی که در بالا داده شد، این خبر مهم است و یا نه؟ (1 یا 0)؟ تنها در یک کلمه پاسخ بده

    """
        file_path = "test.csv"
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter="\t")
        print(df)
        target_col = 'chatgpt_prompt4_tag'
        if target_col not in df:
            df = df.assign(chatgpt_prompt4_tag=None)
        start_row = df.index[df[target_col].isnull() | (df[target_col] == '') | (df[target_col] == '--')].tolist()[0]
        for i in range(start_row, int(len(df))):
            print(f"----------- starting row {i} -----------")
            # prmpt = prompt2 + "\n" + df["title"][i]  + "\n" + df["text"][i]
            prmpt = prompt4.replace("^^body^^", df["title"][i]  + "\n" + df["text"][i])
            sleep1 = random.randint(4, 9)
            sleep2 = random.randint(4, 7)
            while True:
                trn_text1 = self.call_spgt_function(self.chat_bot, sleep1, sleep2, prmpt).\
                    replace('ChatGPT\n', "").replace("1 / 2", "").lstrip().rstrip().\
                    strip()
                if len(trn_text1) >= 5:
                    if "limit of messages per hour" in trn_text1:
                        print('Sleeping 100 Seconds')
                        time.sleep(100)
                    elif 'Response' in trn_text1:
                        print('Two Responses from ChatGPT! Sleep 5 Seconds')
                        time.sleep(5)
                    else:
                        print("length response error. Content:", trn_text1)
                        print("end of message")
                        exit()
                else:
                    break
            print(trn_text1)
            df.loc[df.index[i], target_col] = trn_text1
            df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)
            print('saved at ' + str(datetime.datetime.now()))
            print("   * ----------------- row: ", i , " is translated -----------------\n")
        df.to_csv(file_path, sep='\t', encoding='utf-8', index=False)


if __name__ == "__main__":
    # importance_detection()
    chat_gpt_bot = ChatGPTBot()
    chat_gpt_bot.translate()