from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from random import randint
from selenium.webdriver import ActionChains
import pandas as pd
import os
from datetime import datetime

def logging(func):                                               #Decorator
    def wrapper(*args, **kwargs):
        user_func = func
        orig = func(*args, **kwargs)
        user_func_name = str(user_func.__name__)
        user_name = os.getlogin()
        time_act = str(datetime.now().time())
        day_act =  str(datetime.now().date())
        logs = 'logs.csv'
        if os.path.isfile(logs):                                                                                          #If csv file exists
            file_df = pd.read_csv(logs)
            data = {'': [len(file_df)], 'User': [user_name], 'Func': [user_func_name], 'Time':[time_act], 'Date':[day_act]}
            df = pd.DataFrame(data)
            df.to_csv('logs.csv',header=False, index=False, mode='a')
        else:                                                                                                             #If csv file doesn't exist
            data = {'User': [user_name], 'Func': [user_func_name], 'Time':[time_act], 'Date':[day_act]}
            df = pd.DataFrame(data)
            df.to_csv('logs.csv')
        return orig
    return wrapper

@logging
def calculating_elements(driver):
    elements = driver.find_elements(By.CLASS_NAME, value='b')
    games = []
    for element in elements:
        element.get_attribute('textContent')
        games.append(element)
    return games

@logging
def parsing(driver):
    games = calculating_elements(driver)
    column = ['Game', 'Current online', 'Last day online', 'Peak online']
    df = pd.DataFrame(columns = column)
    iter = 1
    for m in range(0, 4):
        for i in range(1, len(games)+1):
            try:
                game_name = driver.find_element(By.XPATH, value = f'/html/body/div[4]/div/div[2]/div[5]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[3]/a').get_attribute('textContent')
                print(game_name)
            except:
                game_name = None
            try:
                current_online = driver.find_element(By.XPATH, value = f'/html/body/div[4]/div/div[2]/div[5]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[4]').get_attribute('textContent')
            except:
                current_online = None
            try:
                last_day_online = driver.find_element(By.XPATH, value = f'/html/body/div[4]/div/div[2]/div[5]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[5]').get_attribute('textContent')
            except:
                last_day_online = None
            try:
                peak_online = driver.find_element(By.XPATH, value = f'/html/body/div[4]/div/div[2]/div[5]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[6]').get_attribute('textContent')
            except:
                peak_online = None    
            df.loc[iter] = [game_name, current_online, last_day_online, peak_online]
            iter += 1
        clickable_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[5]/div[3]/div[3]/div[2]/div/nav/button[8]'))
        )
        clickable_element.click()
    return df

@logging
def main():
    driver = webdriver.Chrome()
    chrome_version = randint(110, 140)
    windows_version = randint(10, 11)
    opts = Options()
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {windows_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36")
    driver.get("https://www.imdb.com/chart/top/?ref_=hm_nv_menu ")
    df = parsing(driver)
    df.to_csv('steamdb_info.csv')

if __name__ == '__main__':
    main()