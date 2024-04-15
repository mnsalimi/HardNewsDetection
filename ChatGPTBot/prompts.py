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
        
prompt_fa_kshot = """هدف، داشتن یک دسته‌بند دودویی است که با گرفتن هر متن ورودی، کلاس آن را در خروجی مشخص می‌کند. کلاس‌ها شامل دو دسته‌ی 1 یا 0 هستند. 1 یعنی خبر مهم است و 0 یعنی خبر مهم نیست.

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

    نمونه‌ها: چند نمونه پایین را ببین و باتوجه به آن‌ها به سوال پایین پاسخ بده
    SAMPLES_HERE
    از روی نمونه‌های بالایی یاد بگیر و خروجی را مشخص کن (فقط ۰ یا ۱).
    حال  با توجه به «نمونه‌های بالا»، برای متن زیر تنها در یک واژه پاسخ بده که باتوجه به مفاهیمی که در بالا مطرح شد و قدرت استنتاجی که خودت داری، آیا متن 
    مهم (تاثیرگذاری) حساب می‌شود یا خیر. (1 یا 0):
    '''
    ^^body^^
    '''
    در خروجی فقط مجاز هستی عدد ۱ یا عدد ۰ بنویسی. بدون هیچ توضیح اضافه‌ای.
    """
        
prompt_eng_zero_shot = """
The aim is to have a binary classifier that, given each input text, determines its class in the output. Classes include two categories: 1 or 0. 1 means the news is important, and 0 means it is not important.

Task Description:
We consider a text or news important or influential if it is of high importance to most Persian-speaking users. In other words, if a large and significant population of Iranians is willing to read or share that text or news with each other. If the news is related to a small segment or a specific community of users, it is not important. If the input text is important, the class will be 1, and if it is not important, the class will be 0.
Some important concepts include:

Subsidies, stocks, and matters concerning money reaching people are important.
Registration for housing and home, news related to loans, etc.
Car registration
Sharp increases and decreases in the price of currency, gold, coins, or inflation
Political:

News of wars, agreements such as the Iran Nuclear Deal, Iran sanctions,
News of major regional wars,
Impeachment and appointment of high-ranking Iranian officials,
All of these are important
Sports:

News related to famous and popular Iranian as well as European teams is important.

Now, separately and independently, answer in a single word whether the text is important (influential) or not (1 or 0):
'''
^^body^^
'''
According to the explanations provided above, is this news important or not? (1 or 0)? You "must" Respond in "only just one word" (1 or 0) without any extra words.
"""


prompt_eng_kshot = """
The aim is to have a binary classifier that, given each input text, determines its class in the output. Classes include two categories: 1 or 0. 1 means the news is important, and 0 means it is not important.

Task Description:
We consider a text or news important or influential if it is of high importance to most Persian-speaking users. In other words, if a large and significant population of Iranians is willing to read or share that text or news with each other. If the news is related to a small segment or a specific community of users, it is not important. If the input text is important, the class will be 1, and if it is not important, the class will be 0.
Some important concepts include:

Subsidies, stocks, and matters concerning money reaching people are important.
Registration for housing and home, news related to loans, etc.
Car registration
Sharp increases and decreases in the price of currency, gold, coins, or inflation
Political:

News of wars, agreements such as the Iran Nuclear Deal, Iran sanctions,
News of major regional wars,
Impeachment and appointment of high-ranking Iranian officials,
All of these are important
Sports:

News related to famous and popular Iranian as well as European teams is important.

Some Samples:
SAMPLES_HERE

Now, separately and independently, answer in a single word whether the text is important (influential) or not (1 or 0):
'''
^^body^^
'''
According to the explanations provided above, is this news important or not? (1 or 0)? You "must" Respond in "only just one word" (1 or 0) without any extra words.
"""
