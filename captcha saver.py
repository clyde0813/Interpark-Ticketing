from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tkinter import *
from PIL import Image

dp = Tk()
main_frame = Frame(dp)
dp.geometry('500x500')
main_frame.pack()

driver = webdriver.Chrome("./es/chromedriver.exe")
wait = WebDriverWait(driver, 5)
wait2 = WebDriverWait(driver, 5)
url = "https://ticket.interpark.com/Gate/TPLogin.asp"
driver.get(url)


def login_go():
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys('eric3285')
    driver.find_element_by_id('userPwd').send_keys('Eric3371!')
    driver.find_element_by_id('btn_login').click()

def link_go():
    driver.switch_to_window(driver.window_handles[0])
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=20008287')
    driver.switch_to_window(driver.window_handles[-1])

def capture_start():
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to_frame(seat1_frame)
    image = driver.find_element_by_id('imgCaptcha')
    for i in range(1, 501):
        image2 = image.screenshot_as_png
        with open("%d.png" % i, "wb") as file:
            file.write(image2) 
        driver.find_element_by_class_name('refreshBtn').click()

login_button = Button(main_frame, text = "로그인", command = login_go)
login_button.grid(row=1)
link_button = Button(main_frame, text = "직링", command = link_go)
link_button.grid(row=2)
capture_button = Button(main_frame, text = "캡쳐", command = capture_start)
capture_button.grid(row=3)

dp.mainloop()
