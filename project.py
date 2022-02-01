import requests
import json
import sqlite3
from selenium import webdriver
import bs4
import time

# PATH = "C:/Users/GF75/chromedriver.exe"
# driver = webdriver.Chrome(PATH)
# driver.get("https://airtw.epa.gov.tw/")
# citys = driver.find_elements_by_xpath('//*[@id="ddl_county"]/option[position()<23]')
# for city in citys:
#     city.click()
#     time.sleep(4)
# time.sleep(5)

def defind_urls(localtime):
    keys = [str(i) for i in range(1, 94) if not(i in [77, 78, 79, 80, 81, 82, 83, 88, 89])]
    keys.append('96')
    keys.append('136')
    # print(keys)
    localtime = localtime[:-2] + str(int(localtime[-2:]) - 1)
    urls = [f"https://airtw.epa.gov.tw/json/airlist/airlist_{str(i)}_{localtime}.json"
            for i in keys]
    return urls
    # print(urls)

def catchdata(urls):
    count = 1
    all_data = []
    for url in urls:
        header ={
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }
        data_json = requests.get(url, headers=header)
        try:
            data = json.loads(data_json.text)
            # print(str(count))
            # print(data)
            # count += 1
        except:
            print("無法正確抓出所有json檔案，請確認時間是否正確")
        all_data.append(data)
    return all_data
        

def IN_database(all_data):
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    for data in all_data:
        try:
            sql = f"INSERT INTO airtw(date, county, sitename, sitetype, AQI,\
                                    AVPM25, PM25_FIX, AVPM10, PM10_FIX, AVO3,\
                                    O3_FIX, AVCO, CO_FIX, SO2_FIX,\
                                    NO2_FIX, POLLUTANT, AVSO2) VALUES\
                                    ('{data[0]['date']}', '{data[1]['county']}', '{data[2]['sitename']}', '{data[3]['sitetype']}', '{data[4]['AQI']}',\
                                    '{data[5]['AVPM25']}', '{data[6]['PM25_FIX']}', '{data[7]['AVPM10']}', '{data[8]['PM10_FIX']}', '{data[9]['AVO3']}',\
                                    '{data[10]['O3_FIX']}', '{data[11]['AVCO']}', '{data[12]['CO_FIX']}', '{data[13]['SO2_FIX']}',\
                                    '{data[14]['NO2_FIX']}', '{data[15]['POLLUTANT']}', '{data[16]['AVSO2']}')"
            cur.execute(sql)
        except:
            print("無法正確地將資料存入資料庫")
            return 
    print("成功將所有資料存入資料庫")
    conn.commit()

check = False
while True:
    accept = input("是否要取得最新資訊?(Y為是，N為手動輸入)：")
    if accept == 'Y':
        localtime = time.strftime('%Y%m%d%H', time.localtime())
        break
    elif accept == 'N':
        check = True
        break
    else:
        print("輸入錯誤請重新輸入")
while True:
    if check:
        localtime = input("輸入年月日時(ex:2021110414)：")
    if localtime.isdigit() and len(localtime) == 10:
        print("OK")
        urls = defind_urls(localtime)
        all_data = catchdata(urls)
        IN_database(all_data)
        break
    else:
        print("請重新確認時間")

# driver.quit()