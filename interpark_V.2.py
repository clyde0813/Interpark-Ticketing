from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException, UnexpectedAlertPresentException, \
    ElementClickInterceptedException, NoAlertPresentException, ElementNotInteractableException
from tkinter import *
import numpy
import time, datetime
import cv2 as cv
from pytesseract import image_to_string

opt = webdriver.ChromeOptions()
opt.add_argument('window-size=800,600')
driver = webdriver.Chrome(executable_path="D:\SynologyDrive\Python Projects\InterPark\es\chromedriver.exe", options=opt)
wait = WebDriverWait(driver, 10)
url = "https://ticket.interpark.com/Gate/TPLogin.asp"
driver.get(url)


def login_go():
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys(id_entry.get())
    driver.find_element_by_id('userPwd').send_keys(pw_entry.get())
    driver.find_element_by_id('btn_login').click()


def link_go():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())


def link_test():
    driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + showcode_entry.get())
    driver.switch_to.frame(driver.find_element_by_id('ifrmBookStep'))
    driver.execute_script("document.querySelectorAll('.calCont').forEach(function(a) {a.remove()})")


def seat_macro():
    driver.switch_to.default_content()
    seat1_frame = driver.find_element_by_name("ifrmSeat")
    driver.switch_to.frame(seat1_frame)
    seat2_frame = driver.find_element_by_name("ifrmSeatDetail")
    driver.switch_to.frame(seat2_frame)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'stySeat')))
    len_seatn = len(driver.find_elements_by_class_name('stySeat'))
    print(len_seatn)
    len_VIP = len(
        driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]'))
    print(len_VIP)
    shot = 0
    VIP = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
    R = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/2_90.gif"]')
    S = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/3_90.gif"]')
    A = driver.find_elements_by_css_selector('img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/4_90.gif"]')
    for x in range(0, len_seatn):
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
    driver.switch_to.frame(seat1_frame)
    image = driver.find_element_by_id('imgCaptcha')
    image = image.screenshot_as_png
    with open("D:\SynologyDrive\Python Projects\InterPark\captcha.png", "wb") as file:
        file.write(image)
    image = cv.imread("D:\SynologyDrive\Python Projects\InterPark\captcha.png")
    # Set a threshold value for the image, and save
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 85, 1)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=1)

    cnts = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 50:
            cv.drawContours(image, [c], -1, (0, 0, 0), -1)
    kernel2 = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv.filter2D(image, -1, kernel2)
    result = 255 - image
    captcha_text = image_to_string(result)
    print(captcha_text)
    driver.switch_to.default_content()
    driver.switch_to.frame(seat1_frame)
    driver.find_element_by_class_name('validationTxt').click()
    driver.find_element_by_id('txtCaptcha').send_keys(captcha_text)
    while 1:
        try:
            driver.find_element_by_class_name('refreshBtn').click()
            captcha()
        except (ElementClickInterceptedException, WebDriverException, NoSuchElementException):
            return


def date_select():
    # 날짜
    while True:
        driver.switch_to.frame(driver.find_element_by_id('ifrmBookStep'))
        if int(calender_entry.get()) == 0:
            pass
        elif int(calender_entry.get()) >= 1:
            for i in range(1, int(calender_entry.get()) + 1):
                driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
        try:
            driver.find_element_by_xpath('(//*[@id="CellPlayDate"])' + "[" + date_entry.get() + "]").click()
            break
        except NoSuchElementException:
            link_go()
            go()
            break
        except NoSuchElementException:
            link_go()
            go()
            break
    # 회차
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + round_entry.get() + ']/a'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_id('LargeNextBtnImage').click()


def seat_again():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.execute_script('$("ifrmSeatDetail").contentWindow.location.reload();')
    driver.execute_script('fnInitSeat();')
    driver.switch_to.default_content()
    seat_macro()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.find_element_by_id('NextStepImage').click()


def go2():
    driver.switch_to.default_content()
    seat_macro()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("ifrmSeat"))
    driver.find_element_by_id('NextStepImage').click()
    while 1:
        try:
            seat_again()
            pass
        except UnexpectedAlertPresentException:
            pass


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
        except NoSuchElementException:
            go2()
            pass
    except NoSuchElementException:
        date_select()
        try:
            captcha()
            go2()
            pass
        except NoSuchElementException:
            go2()
            pass
    except UnexpectedAlertPresentException:
        all_go()
    finally:
        code_time.insert(0, "%s 초" % round((time.time() - start_time), 3))


def all_go():
    while 1:
        try:
            link_go()
            go()
            return
        except UnexpectedAlertPresentException:
            driver.switch_to.alert.accept()
            link_go()
            go()
            return
        except NoSuchElementException:
            link_go()
            go()
            return


def credit():
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="YYMMDD"]'))).send_keys(birth_entry.get())
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    bank2 = bank_var.get()
    kakao2 = kakao_var.get()
    if bank2 == 1:
        bank()
    elif kakao2 == 1:
        kakao()


def bank():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[7]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def kakao():
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22084"]/td/input'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()


def clock_time():
    clock = time.strftime('%X')
    time_label.config(text=clock)
    time_label.after(1, clock_time)


def full_auto():
    while True:
        time1 = time.strftime('%X')
        print(time1)
        if time1 == full_entry.get():
            all_go()


dp = Tk()
main_frame = Frame(dp)
dp.geometry('300x450')
dp.title("인터파크 티켓팅 프로그램")
main_frame.pack()

id_label = Label(main_frame, text="아이디")
id_label.grid(row=1, column=0)

id_entry = Entry(main_frame)
id_entry.grid(row=1, column=1)

pw_label = Label(main_frame, text="비밀번호")
pw_label.grid(row=2, column=0)

pw_entry = Entry(main_frame)
pw_entry.grid(row=2, column=1)

login_button = Button(main_frame, text="로그인", command=login_go, height=2)
login_button.grid(row=3, column=1)

showcode_label = Label(main_frame, text="공연번호")
showcode_label.grid(row=4, column=0)

showcode_entry = Entry(main_frame)
showcode_entry.grid(row=4, column=1)

calendar_label = Label(main_frame, text="달력")
calendar_label.grid(row=5, column=0)

calender_entry = Entry(main_frame)
calender_entry.grid(row=5, column=1)

date_label = Label(main_frame, text="날짜")
date_label.grid(row=6, column=0)

date_entry = Entry(main_frame)
date_entry.grid(row=6, column=1)

round_label = Label(main_frame, text="회차")
round_label.grid(row=7, column=0)

round_entry = Entry(main_frame)
round_entry.grid(row=7, column=1)

ticket_label = Label(main_frame, text="티켓 수")
ticket_label.grid(row=8, column=0)

ticket_entry = Entry(main_frame)
ticket_entry.grid(row=8, column=1)

link_button = Button(main_frame, text="직링", command=link_go, height=2)
link_button.grid(row=9, column=0, sticky=E)

all_button = Button(main_frame, text='시작', command=all_go, height=2)
all_button.grid(row=9, column=1, sticky=W + E)

chair_button = Button(main_frame, text="좌석", command=go2, height=2)
chair_button.grid(row=9, column=2, sticky=W)

start_button = Button(main_frame, text="직좌", command=go, height=2)
start_button.grid(row=10, column=0, sticky=E)

credit_button = Button(main_frame, text="결제", command=credit, height=2)
credit_button.grid(row=10, column=1, sticky=W + E)

captcha_button = Button(main_frame, text='캡챠', command=captcha, height=2)
captcha_button.grid(row=10, column=2, sticky=W)

bank_var = IntVar(value=0)
bank_check = Checkbutton(main_frame, text='무통장', variable=bank_var)
bank_check.grid(row=9, column=3)

kakao_var = IntVar(value=0)
kakao_check = Checkbutton(main_frame, text='카카오', variable=kakao_var)
kakao_check.grid(row=10, column=3)

credit2_button = Button(main_frame, text="자동 예매", command=full_auto, height=2)
credit2_button.grid(row=12, column=1, sticky=N)

full_label = Label(main_frame, text="예매 시간")
full_label.grid(row=13, column=0)

full_entry = Entry(main_frame)
full_entry.grid(row=13, column=1)

time_label = Label(main_frame, height=2)
time_label.grid(row=14, column=1)

birth_label = Label(main_frame, text='생년월일')
birth_label.grid(row=15, column=0)

birth_entry = Entry(main_frame)
birth_entry.grid(row=15, column=1)

code_label = Label(main_frame, text='소요시간')
code_label.grid(row=16, column=0)

code_time = Entry(main_frame)
code_time.grid(row=16, column=1)

full_time = (datetime.datetime.combine(datetime.date(1, 1, 1), datetime.datetime.now().time()) + datetime.timedelta(
    seconds=20)).time()

if __name__ != "__main__":
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_name('userId').send_keys('eric3285')
    driver.find_element_by_id('userPwd').send_keys('Eric3371!')
    driver.find_element_by_id('btn_login').click()
    showcode_entry.insert(0, '19018396')
    calender_entry.insert(0, '0')
    date_entry.insert(0, '10')
    round_entry.insert(0, '1')
    ticket_entry.insert(0, '2')
    full_entry.insert(0, str(full_time)[:8])

clock_time()
dp.mainloop()
