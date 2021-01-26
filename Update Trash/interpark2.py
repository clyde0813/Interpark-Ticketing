from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tkinter import *
import time
from datetime import datetime
import numpy
import re
import cv2 as cv
from pytesseract import image_to_string
import getpass
import threading

dp = Tk()
main_frame = Frame(dp)
dp.geometry('500x500')
dp.title("인터파크 티켓팅 프로그램")
main_frame.pack()

driver = webdriver.Chrome("./es/chromedriver.exe")
driver2 = webdriver.Chrome("./es/chromedriver.exe")
wait = WebDriverWait(driver, 10)
wait2 = WebDriverWait(driver2, 10)
url = "https://ticket.interpark.com/Gate/TPLogin.asp"

def url1():
    driver.get(url)

def url2():
    driver2.get(url)

def url_all():
    threading.Thread(target=url1).start()
    threading.Thread(target=url2).start()
url_all()

id_label = Label(main_frame, text = "첫번째 아이디")
id_label.grid(row = 1, column = 0)
id_entry = Entry(main_frame)
id_entry.grid(row = 1, column = 1)

pw_label = Label(main_frame, text = "첫번째 비밀번호")
pw_label.grid(row = 2, column = 0)
pw_entry = Entry(main_frame)
pw_entry.grid(row = 2, column =1)

id_label2 = Label(main_frame, text = "두번째 아이디")
id_label2.grid(row = 3, column = 0)
id_entry2 = Entry(main_frame)
id_entry2.grid(row = 3, column = 1)

pw_label2 = Label(main_frame, text = "두번째 비밀번호")
pw_label2.grid(row = 4, column = 0)
pw_entry2 = Entry(main_frame)
pw_entry2.grid(row = 4, column =1)

showcode_label = Label(main_frame, text = "공연번호")
showcode_label.grid(row=6, column = 0)
showcode_entry = Entry(main_frame)
showcode_entry.grid(row=6, column = 1)

date_label = Label(main_frame, text = "첫번째 날짜")
date_label.grid(row=7, column = 0)
date_entry = Entry(main_frame)
date_entry.grid(row=7, column = 1)

date_label2 = Label(main_frame, text = "두번째 날짜")
date_label2.grid(row=7, column = 2)
date_entry2 = Entry(main_frame)
date_entry2.grid(row=7, column = 3)

round_label = Label(main_frame, text = "첫번째 회차")
round_label.grid(row = 8, column = 0)
round_entry = Entry(main_frame)
round_entry.grid(row=8, column = 1)

round_label2 = Label(main_frame, text = "두번째 회차")
round_label2.grid(row = 8, column = 2)
round_entry2 = Entry(main_frame)
round_entry2.grid(row=8, column = 3)

ticket_label = Label(main_frame, text = "티켓 수")
ticket_label.grid(row = 9, column = 0)
ticket_entry = Entry(main_frame)
ticket_entry.grid(row=9, column = 1)

code_time = Entry(main_frame)
code_time.grid(row=14, column = 1)
code_time2 = Entry(main_frame)
code_time2.grid(row=15, column = 1)

def login_go():
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys(id_entry.get())
    driver.find_element_by_id('userPwd').send_keys(pw_entry.get())
    driver.find_element_by_id('btn_login').click()

def login_go2():
    driver2.switch_to_frame(driver2.find_element_by_tag_name('iframe'))
    driver2.find_element_by_name('userId').send_keys(id_entry2.get())
    driver2.find_element_by_id('userPwd').send_keys(pw_entry2.get())
    driver2.find_element_by_id('btn_login').click()

def login_go3():
    threading.Thread(target=login_go).start()
    threading.Thread(target=login_go2).start()

def link_go():
    try:
        driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())
    except:
        driver.refresh()
def link_go2():    
    try:        
        driver2.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())
    except:
        driver2.refresh()
def link_all():
    threading.Thread(target=link_go).start()
    threading.Thread(target=link_go2).start()

def seat_macro():
    driver.switch_to_default_content()
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    seat2_frame = driver.find_element_by_name("ifrmSeatDetail")
    driver.switch_to_frame(seat2_frame)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stySeat')))
    len_seatn = len(driver.find_elements_by_class_name('stySeat'))
    print(len_seatn)
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

def seat_macro1_1():
    driver2.switch_to.default_content()
    seat3_frame = driver2.find_element_by_name("ifrmSeat")
    driver2.switch_to_frame(seat3_frame)
    seat4_frame = driver2.find_element_by_name("ifrmSeatDetail")
    driver2.switch_to_frame(seat4_frame)
    wait2.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stySeat')))
    len_seatn2 = len(driver2.find_elements_by_class_name('stySeat'))
    print(len_seatn2)
    shot2 = 0
    VIP2 = driver2.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
    R2 = driver2.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/2_90.gif"]')
    S2 = driver2.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/3_90.gif"]')
    A2 = driver2.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/4_90.gif"]')
    for x in range(0 , len_seatn2):
        try:
            VIP2[x].click()
            shot2 = shot2 + 1
        except:
            try:
                R2[x].click()
                shot2 = shot2 + 1
            except:
                try:
                    S2[x].click()
                    shot2 = shot2 + 1
                except:
                    try:
                        A2[x].click()
                        shot2 = shot2 + 1
                    except:
                        break
        if shot2 == int(ticket_entry.get()):
            break  

def seat_macro2():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    seat2_frame = driver.find_element_by_name("ifrmSeatDetail")
    driver.switch_to_frame(seat2_frame)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stySeat')))
    len_seatn = len(driver.find_elements_by_class_name('stySeat'))
    print(len_seatn)
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
    driver.switch_to_default_content()
    seat1_frame = driver.find_element_by_id("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    image = driver.find_element_by_id('imgCaptcha')
    image = image.screenshot_as_png
    with open("captcha.png", "wb") as file:
            file.write(image)
    image = cv.imread("captcha.png")
    #Set a threshold value for the image, and save		
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 85, 1)
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
    filtered_text = re.sub('[a-z]', '',captcha_text).replace(" ", "")
    filtered2_text = re.sub('[-,!@#$%^&*()[]{};:,./<>?\|`~-=_+]', '',filtered_text)
    print(captcha_text)
    driver.switch_to_default_content()
    driver.switch_to_frame(seat1_frame)
    driver.find_element_by_class_name('validationTxt').click()
    driver.find_element_by_id('txtCaptcha').send_keys(filtered2_text)
    print(filtered2_text)
    time.sleep(0.05)
    while 1:
            if driver.find_element_by_class_name('alertNotice').is_displayed():
                driver.find_element_by_class_name('refreshBtn').click()
                captcha()
            else:
                break

def captcha2():
    driver2.switch_to_default_content()
    seat3_frame = driver2.find_element_by_id("ifrmSeat")
    driver2.switch_to_frame(seat3_frame)
    image2 = driver2.find_element_by_id('imgCaptcha')
    image2 = image2.screenshot_as_png
    with open("captcha2.png", "wb") as file:
            file.write(image2)
    image2 = cv.imread("captcha2.png")
    #Set a threshold value for the image, and save		
    image2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)
    image2 = cv.adaptiveThreshold(image2, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 45, 1)
    kerne2 = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    image2 = cv.morphologyEx(image2, cv.MORPH_OPEN, kerne2, iterations=1)

    cnts2 = cv.findContours(image2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts2 = cnts2[0] if len(cnts2) == 2 else cnts2[1]
    for c in cnts2:
        area2 = cv.contourArea(c)
        if area2 < 50:
            cv.drawContours(image2, [c], -1, (0,0,0), -1)
    kernel3 = numpy.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    image2 = cv.filter2D(image2,-1,kernel3)
    result2 = 255 - image2
    captcha_text2 = image_to_string(result2)
    filtered_text2 = re.sub('[a-z]', '',captcha_text2).replace(" ", "")
    filtered2_text2 = re.sub('[-,!@#$%^&*()[]{};:,./<>?\|`~-=_+]', '',filtered_text2)
    print(captcha_text2)
    driver2.switch_to_default_content()
    driver2.switch_to_frame(seat3_frame)
    driver2.find_element_by_class_name('validationTxt').click()
    driver2.find_element_by_id('txtCaptcha').send_keys(filtered2_text2)
    print(filtered2_text2)
    time.sleep(0.05)
    while 1:
            if driver2.find_element_by_class_name('alertNotice').is_displayed():
                driver2.find_element_by_class_name('refreshBtn').click()
                captcha2()
            else:
                break

def date_select():
    first_frame = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to_frame(first_frame)
    #날짜
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="CellPlayDate"])' + "[" + date_entry.get() + "]"))).click()
    #회차
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry.get() + ']/a'))).click()
    driver.switch_to_default_content()
    wait.until(EC.element_to_be_clickable((By.ID, 'LargeNextBtnImage'))).click()
    #다음
    try:
        driver.switch_to.alert().accept()
        driver.switch_to_default_content()
        wait.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))
    except:
        driver.switch_to_default_content()
        wait.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))
         
def date_select2():
    first_frame2 = driver2.find_element_by_id('ifrmBookStep')
    driver2.switch_to_frame(first_frame2)
    #날짜
    wait2.until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="CellPlayDate"])' + "[" + date_entry2.get() + "]"))).click()
    #회차
    wait2.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry2.get() + ']/a'))).click()
    driver2.switch_to_default_content()
    wait2.until(EC.element_to_be_clickable((By.ID, 'LargeNextBtnImage'))).click()
    #다음
    try:
        driver2.switch_to.alert().accept()
        driver2.switch_to_default_content()
        wait2.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))
    except:
        driver2.switch_to_default_content()
        wait2.until(EC.presence_of_all_elements_located((By.ID, 'ifrmSeat')))

def go2():
    driver.switch_to_default_content()
    seat1_frame = driver.find_element_by_id("ifrmSeat")
    seat_macro()
    try:
        driver.switch_to_default_content()
        driver.switch_to_frame(seat1_frame)
        driver.find_element_by_id('NextStepImage').click()
        driver.switch_to_default_content()
        driver.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
        driver.find_element_by_name('SeatCount')
    except:
        try:
            driver.switch_to_default_content()
            driver.switch_to.alert().accept()
            driver.switch_to.default_content()
            driver.switch_to_frame(seat1_frame)
            driver.find_element_by_class_name('f1_r').click()
            seat_macro()
            driver.switch_to_default_content()
            driver.switch_to_frame(seat1_frame)
            driver.find_element_by_id('NextStepImage').click()
        except:
            try:
                seat_macro()
                driver.switch_to_default_content()
                driver.switch_to_frame(seat1_frame)
                driver.find_element_by_id('NextStepImage').click()
            except:
                try:
                    driver.switch_to_default_content()
                    driver.switch_to_frame(seat1_frame)
                    driver.find_element_by_id('NextStepImage').click()
                    driver.switch_to_default_content()
                    driver.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
                    driver.find_element_by_name('SeatCount')
                except:
                    try:
                        seat_macro()
                        driver.switch_to_default_content()
                        driver.switch_to_frame(seat1_frame)
                        driver.find_element_by_id('NextStepImage').click()
                    except:
                        try:
                            driver.switch_to_default_content()
                            driver.switch_to_frame(seat1_frame)
                            driver.find_element_by_id('NextStepImage').click()
                            driver.switch_to_default_content()
                            driver.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
                            driver.find_element_by_name('SeatCount')
                        except:
                            pass

def go3():
    driver2.switch_to_default_content()
    seat3_frame = driver2.find_element_by_id("ifrmSeat")
    seat_macro1_1()
    try:
        driver2.switch_to_default_content()
        driver2.switch_to_frame(seat3_frame)
        driver2.find_element_by_id('NextStepImage').click()
        driver2.switch_to_default_content()
        driver2.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
        driver2.find_element_by_name('SeatCount')
    except:
        try:
            driver2.switch_to_default_content()
            driver2.switch_to.alert().accept()
            driver2.switch_to.default_content()
            driver2.switch_to_frame(seat3_frame)
            driver2.find_element_by_class_name('f1_r').click()
            seat_macro1_1()
            driver2.switch_to_default_content()
            driver2.switch_to_frame(seat3_frame)
            driver2.find_element_by_id('NextStepImage').click()
        except:
            try:
                seat_macro1_1()
                driver2.switch_to_default_content()
                driver2.switch_to_frame(seat3_frame)
                driver2.find_element_by_id('NextStepImage').click()
            except:
                try:
                    driver2.switch_to_default_content()
                    driver2.switch_to_frame(seat3_frame)
                    driver2.find_element_by_id('NextStepImage').click()
                    driver2.switch_to_default_content()
                    driver2.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
                    driver2.find_element_by_name('SeatCount')
                except:
                    try:
                        seat_macro1_1()
                        driver2.switch_to_default_content()
                        driver2.switch_to_frame(seat3_frame)
                        driver2.find_element_by_id('NextStepImage').click()
                    except:
                        try:
                            driver2.switch_to_default_content()
                            driver2.switch_to_frame(seat3_frame)
                            driver2.find_element_by_id('NextStepImage').click()
                            driver2.switch_to_default_content()
                            driver2.switch_to_frame(driver.find_element_by_id('ifrmBookStep'))
                            driver2.find_element_by_name('SeatCount')
                        except:
                            pass

def go():
    code_time2.delete(0, END)
    start_time = time.time()
    try:
        driver.find_element_by_class_name('closeBtn').click()
        date_select()
        try:
            captcha()  
            go2()
        except:
            go2()
    except:
        try:
            date_select()
            captcha()
            go2()
        except:
            go2()
    finally:
        code_time.insert(0 ,"%s 초" % (time.time() - start_time) )

def go1_1():
    code_time2.delete(0, END)
    start_time2 = time.time()
    try:
        driver2.find_element_by_class_name('closeBtn').click()
        date_select2()
        try:
            captcha2()  
            go3()
        except:
            go3()
    except:
        try:
            date_select2()
            captcha2()
            go3()
        except:
            go3()
    finally:
        code_time2.insert(0 ,"%s 초" % (time.time() - start_time2) )

def go_all():
    threading.Thread(target=go).start()
    threading.Thread(target=go1_1).start()

def clock_time():
    clock = datetime.now().strftime('%H:%M:%S:%f')
    time_label.config(text = clock)
    time_label.after(1, clock_time)

login_button = Button(main_frame, text = "로그인", command = login_go3, height = 2)
login_button.grid(row=4, column = 3)
link_button = Button(main_frame, text = "직링", command = link_all, height = 2)
link_button.grid(row=5, column = 1)
start_button = Button(main_frame, text = "시작", command = go_all, height = 2)
start_button.grid(row=10, column = 1)
chair_button = Button(main_frame, text = "ERROR", command = go2, height = 2)
chair_button.grid(row=11, column = 1)
captcha_button = Button(main_frame, text = 'Captcha', command = captcha, height = 2)
captcha_button.grid(row=12, column = 1)
time_label = Label(main_frame, font = ("Calibri", 15) ,height = 2)
time_label.grid(row=13, column = 1)
clock_time()


dp.mainloop()

