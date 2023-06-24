from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import config
import telebot

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def is_time_to_stop(curr_time, stop_time):
    curr_time_ls = [curr_time.hour, curr_time.minute, curr_time.second]
    stop_time_ls = [stop_time.hour, stop_time.minute, stop_time.second]
    cnt = 0
    while cnt < 3:
        if curr_time_ls[cnt] > stop_time_ls[cnt]:
            return True
        elif curr_time_ls[cnt] < stop_time_ls[cnt]:
            return False
        cnt += 1
    return False

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://moskovskoe.vremja.org")

# css selector: $(".table-price > .container > .desctop > .show-all__wrap > .show-all__table > .table2 > tbody > tr:first-child")

bot = telebot.TeleBot(config.tg_token)
import time
import datetime

print("OK")
stop_time = datetime.datetime.now() + datetime.timedelta(seconds=40)
while True:
    driver.refresh()
    print("begin")
    time.sleep(20)
    print("not now")
    res = driver.find_element(By.CSS_SELECTOR, '#Timer')
    curr_time = datetime.datetime.strptime(res.text, "%H:%M:%S")
    print("Time: ", curr_time.strftime('%H:%M:%S'),  stop_time.strftime("%H:%M:%S"), is_time_to_stop(curr_time, stop_time))
    if is_time_to_stop(curr_time, stop_time):
        bot.send_message(726502189, "Time's up")
        break

