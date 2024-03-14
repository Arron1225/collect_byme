import pandas as pd
from googletrans import Translator
from tqdm import tqdm
import time
df = pd.read_excel('ttt.xlsx')
translator = Translator()
errors = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Translating subjects"):
    try:
     
        translated_subject = translator.translate(row['subject'], dest="English").text
        # 新增翻譯後的結果到 DataFrame
        df.at[index, 'translated_subject'] = translated_subject
        time.sleep(1)
    except Exception as e:
        error_message = f"Error translating subject at index {index}: {e}"
        errors.append(error_message)
        print(error_message)
        df.at[index, 'translated_subject'] = row['subject']


print(df.head())

stop_words = ["_x000d"]  # 你的停用詞列表

def remove_stop_words(sentence, stop_words):
    # 替換 _x000d 為空字符串
    sentence = sentence.lower().replace('_x000d', '')
    
    words = sentence.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)


df['translated_subject'] = df['translated_subject'].apply(lambda x: remove_stop_words(x, stop_words))


print("DataFrame after removing stop words and handling _x000d:")
print(df[['translated_subject']])
df.to_excel('result_google_translate_v7_22.xlsx', index=False)
