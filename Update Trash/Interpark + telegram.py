from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tkinter import *
from datetime import datetime
import numpy, re, pyotp, sys, time, tkinter.ttk, pytesseract, tkinter.font
import cv2 as cv
from pytesseract import image_to_string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, Update, Bot
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Updater, Filters
import threading

dp = Tk()
main_frame = Frame(dp)
dp.geometry('500x500')
dp.title("인터파크 티켓팅 프로그램")
main_frame.pack()

driver = webdriver.Chrome("es/chromedriver")
wait = WebDriverWait(driver, 20)
url = "https://ticket.interpark.com/Gate/TPLogin.asp"
driver.get(url)

id_label = Label(main_frame, text = "아이디")
id_label.grid(row = 1, column = 0)
id_entry = Entry(main_frame)
id_entry.grid(row = 1, column = 1)

pw_label = Label(main_frame, text = "비밀번호")
pw_label.grid(row = 2, column = 0)
pw_entry = Entry(main_frame, show = '*')
pw_entry.grid(row = 2, column =1)

showcode_label = Label(main_frame, text = "공연번호")
showcode_label.grid(row=4, column = 0)
showcode_entry = Entry(main_frame)
showcode_entry.grid(row=4, column = 1)

date_label = Label(main_frame, text = "날짜")
date_label.grid(row=5, column = 0)
date_entry = Entry(main_frame)
date_entry.grid(row=5, column = 1)

round_label = Label(main_frame, text = "회차")
round_label.grid(row = 6, column = 0)
round_entry = Entry(main_frame)
round_entry.grid(row=6, column = 1)

ticket_label = Label(main_frame, text = "티켓 수")
ticket_label.grid(row = 7, column = 0)
ticket_entry = Entry(main_frame)
ticket_entry.grid(row=7, column = 1)

code_time = Entry(main_frame)
code_time.grid(row=12, column = 1)

def login_go():
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys(id_entry.get())
    driver.find_element_by_id('userPwd').send_keys(pw_entry.get())
    driver.find_element_by_id('btn_login').click()

def link_go():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())

def seat_macro():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    seat2_frame = driver.find_element_by_name("ifrmSeatDetail")
    driver.switch_to_frame(seat2_frame)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stySeat')))
    len_seatn = len(driver.find_elements_by_class_name('stySeat'))
    print(len_seatn)
    len_VIP = len(driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]'))
    print(len_VIP)
    shot = 0
    VIP = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
    R = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/2_90.gif"]')
    S = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/3_90.gif"]')
    A = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/4_90.gif"]')
    for x in range(0 , len_seatn):
        try:
            VIP[x].click()
            shot = shot + 1
        except:
            try:
                R[x].click()
                shot = shot + 1
            except:
                try:
                    S[x].click()
                    shot = shot + 1
                except:
                    try:
                        A[x].click()
                        shot = shot + 1
                    except:
                        break
        if shot == int(ticket_entry.get()):
            break  

def captcha():
        driver.switch_to.default_content()
        seat1_frame = driver.find_element_by_id("ifrmSeat")
        driver.switch_to_frame(seat1_frame)
        image = driver.find_element_by_id('imgCaptcha')
        image = image.screenshot_as_png
        with open("captcha.png", "wb") as file:
                file.write(image)
        image = cv.imread("captcha.png")
        #Set a threshold value for the image, and save		
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 71, 1)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=1)

        cnts = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv.contourArea(c)
            if area < 50:
                cv.drawContours(image, [c], -1, (0,0,0), -1)
        kernel2 = numpy.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
        image = cv.filter2D(image,-1,kernel2)
        result = 255 - image
        captcha_text = image_to_string(result)
        print(captcha_text)
        driver.switch_to.default_content()
        driver.switch_to_frame(seat1_frame)
        driver.find_element_by_class_name('validationTxt').click()
        driver.find_element_by_id('txtCaptcha').send_keys(captcha_text)
        while 1:
                if driver.find_element_by_class_name('capchaInner').is_displayed():
                    driver.find_element_by_class_name('refreshBtn').click()
                    captcha()
                else:
                    break

def date_select():
        first_frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to_frame(first_frame)
        #날짜
        driver.find_element_by_xpath('(//*[@id="CellPlayDate"])' + "[" + date_entry.get() + "]").click()
        #회차
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry.get() + ']/a'))).click()
        driver.switch_to.default_content()
        wait.until(EC.element_to_be_clickable((By.ID, 'LargeNextBtnImage'))).click()
        #다음
        try:
            driver.switch_to.alert().accept()
            driver.switch_to.default_content()
            wait.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))
        except:
            driver.switch_to.default_content()
            wait.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))

def go2():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_id("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    seat2_frame = driver.find_element_by_id("ifrmSeatDetail")
    driver.switch_to_frame(seat2_frame)
    seat_macro()
    try:
        driver.switch_to.alert().accept()
        driver.switch_to.default_content()
        driver.switch_to_frame(seat1_frame)
        driver.find_element_by_id('NextStepImage').click()
        driver.switch_to.alert().accept()
    except:
        driver.switch_to.default_content()
        driver.switch_to_frame(seat1_frame)
        driver.find_element_by_id('NextStepImage').click()

def go():
    code_time.delete(0, END)
    start_time = time.time()
    try:
        driver.find_element_by_class_name('closeBtn').click()
        date_select()
        try:
            captcha()  
            go2()
            pass
        except:
            go2()
            pass
    except:
        date_select()
        try:
            captcha()
            go2()
            pass
        except:
            go2()
            pass
    finally:
        code_time.insert(0 ,"%s 초" % round((time.time() - start_time),3) )

def clock_time():
    clock = datetime.now().strftime('%H:%M:%S:%f')
    time_label.config(text = clock)
    time_label.after(1, clock_time)

BOT_TOKEN = '1289747693:AAEBosjOS2ui3ROkGrPOwmDq04JRrLPOL_U'
updater = Updater(token=BOT_TOKEN)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def get_command(update, context):
    show_list = []
    show_list.append(InlineKeyboardButton("시작", callback_data='1'))
    show_list.append(InlineKeyboardButton("직링", callback_data='2'))
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1))
    update.message.reply_text("선택하세요.", reply_markup = show_markup)
    if update.callback_data == '1':
        go()
    elif update.callback_data == '2':
        link_go()

get_handler = CommandHandler('task', get_command)
updater.dispatcher.add_handler(get_handler)


login_button = Button(main_frame, text = "로그인", command = login_go, height = 2)
login_button.grid(row=2, column = 3)
link_button = Button(main_frame, text = "직링", command = link_go, height = 2)
link_button.grid(row=3, column = 1)
start_button = Button(main_frame, text = "시작", command = go, height = 2)
start_button.grid(row=8, column = 1)
chair_button = Button(main_frame, text = "좌석", command = go2, height = 2)
chair_button.grid(row=9, column = 1)
captcha_button = Button(main_frame, text = '캡챠', command = captcha, height = 2)
captcha_button.grid(row=10, column = 1)
time_label = Label(main_frame, height = 2)
time_label.grid(row=11, column = 1)
clock_time()

def updater2():
    updater.start_polling()
    updater.idle()

def mainup():
    threading.Thread(target=updater2).start()
    threading.Thread(dp.mainloop()).start()
mainup()

