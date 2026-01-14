# Top 250 movies

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

def logging(func):                                               
    def wrapper(*args, **kwargs):
        user_func = func
        orig = func(*args, **kwargs)
        user_func_name = str(user_func.__name__)
        user_name = os.getlogin()
        time_act = str(datetime.now().time())
        day_act =  str(datetime.now().date())
        logs = 'logs.csv'
        if os.path.isfile(logs):                                                                                          
            file_df = pd.read_csv(logs)
            data = {'': [len(file_df)], 'User': [user_name], 'Func': [user_func_name], 'Time':[time_act], 'Date':[day_act]}
            df = pd.DataFrame(data)
            df.to_csv('logs.csv',header=False, index=False, mode='a')
        else:                                                                                                             
            data = {'User': [user_name], 'Func': [user_func_name], 'Time':[time_act], 'Date':[day_act]}
            df = pd.DataFrame(data)
            df.to_csv('logs.csv')
        return orig
    return wrapper


@logging
def parsing(driver):
    column = ['Movie name', 'Release Year', 'Duration', 'Age Limit', 'Rating']
    df = pd.DataFrame(columns = column)
    iter = 1
    for i in range(1, 251):
        try:
            movie_name = driver.find_element(By.XPATH, value = f'/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[2]/a/h3').get_attribute('textContent')
            print(movie_name)
        except:
            movie_name = None
        try:
            release_year = driver.find_element(By.XPATH, value = f'/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[3]/span[1]').get_attribute('textContent')
        except:
            release_year = None
        try:
            duration = driver.find_element(By.XPATH, value = f'/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[3]/span[2]').get_attribute('textContent')
        except:
            duration = None
        try:
            age_limit = driver.find_element(By.XPATH, value = f'/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[3]/span[3]').get_attribute('textContent')
        except:
            age_limit = None    
        try:
            rating = driver.find_element(By.XPATH, value = f'/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/span/div/span/span[1]').get_attribute('textContent')
        except:
            rating = None    
        df.loc[iter] = [movie_name, release_year, duration, age_limit, rating]
        iter += 1
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
    df.to_csv('IMDb_info.csv')

if __name__ == '__main__':
    main()