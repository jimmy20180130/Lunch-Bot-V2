import json
import sys
import traceback

def load_lunch():
    with open('lunch_data.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)
    return user_data

def load_lunch_data():
    with open('lunch.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)
    return user_data
        
def save_lunch(data):
    with open('lunch_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
def load_settings():
    with open('settings.json', 'r', encoding='utf-8') as file:
        setting = json.load(file)
    return setting
        
def error_info(e):
    try:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        err_msg = f'發生了錯誤\n類型: {error_class}\n檔案名稱: {fileName}\n函數名稱: {funcName}\n行數: {lineNum}\n詳細原因: {detail}'
        return err_msg
    except Exception as e:
        print(e)