
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import time
import urllib
from pathlib import Path
import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

existed_files = []
checked_files = []
username=["selenagomez","justinbieber"] #isi username jadi array

def get_img(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()),dtype=np.uint8)
    img = cv2.imdecode(arr,cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def check_img_size(gray):
    print("Size: "+str(gray.shape))
    if gray.shape[0] < 512 or gray.shape[1]<512:
       print("Small picture detected, rejecting")
       return False
    return True

def check_face(url):
    gray = get_img(url)
    if check_img_size(gray) is False:
        return False
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        return True
    return False

def write_checked(uname):
    file = open(uname+'\\checked.txt','w')
    for item in checked_files:
        file.write(item+"\n")
    file.close()

def list_existing_files(uname):
    listdir = Path(uname).glob('**/*')
    files = [x for x in listdir if x.is_file()]
    for i in files:
        filename = str(i).replace(uname,'')
        existed_files.append(filename)
        checked_files.append(filename)

def check_existed_or_checked(filename):
    filename='\\'+filename
    if filename in existed_files or filename in checked_files:
        return True
    else:
        checked_files.append(filename)
        return False

def save_story():
    while True:
        try:
            img = driver.find_element(By.XPATH,"//img[@decoding='sync']")
            time.sleep(1)
            src = img.get_attribute("src")
            filename = src[56:src.find('jpg')+3] 
            filename = filename.replace('?','')
            print("Checking: "+filename)
            if check_existed_or_checked(filename) is False and check_face(src):
                print(filename+" has face, downloading...")
                urllib.request.urlretrieve(src, u+"/"+filename)
            driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
        except Exception as e:
            try:
                driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
            except Exception as e:
                return
        

def open_story():
    stories = driver.find_elements(By.XPATH, "//div[@role='button']")
    for s in stories:
        s.click()
        save_story()

def open_highlights():
    driver.find_element(By.XPATH, "//div[@role='menuitem']").click()
    while True:
        try:
            try:
                if driver.find_element(By.TAG_NAME,"video"):
                    print("skipping video")
                    driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
            except:
                print("Not a video")
            src = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//img[@decoding='sync']"))).get_attribute("src")
            filename = src[56:src.find('jpg')+3] 
            filename = filename.replace('?','')
            print("Checking: "+filename)
            if check_existed_or_checked(filename) is False and check_face(src):
                print(filename+" has face, downloading...")
                urllib.request.urlretrieve(src, u+"/"+filename)
            try:
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
            except:
                return
        except Exception as e:
            print(e)

def open_feeds():
    anchors = driver.find_elements(By.TAG_NAME,"a")
    for tag in anchors: 
        href = tag.get_attribute("href")
        print(href[25:])
        if href[25:28] == '/p/':
            try:
                tag.click()
                time.sleep(2)
                break
            except:
                print("error click")
        else:  
            continue

    while True:
        time.sleep(1)
        imgs = driver.find_elements(By.TAG_NAME,"img")
        # videos = driver.find_elements(By.TAG_NAME,"video") #Belum bisa download video
        for img in imgs:
            try:
                src = img.get_attribute("src")
                filename = src[56:src.find('jpg')+3] 
                filename = filename.replace('?','')
                print("Checking: "+filename)
                if check_existed_or_checked(filename) is False and check_face(src):
                    print(filename+" has face, downloading...")
                    urllib.request.urlretrieve(src, u+"/"+filename)
                else:
                    print("File "+filename+"is checked or existed")
            except Exception as e:
                print (e)
        try:
            driver.find_element(By.CLASS_NAME,'_aaqg').click()
        except Exception as e:
            print(e)
            print("End of profile")
            write_checked(u)
            break

#Pakai edge, pakai profile yg udh login IG buat akses private account, kalau nggak, boleh komen aja line 161-163
option = EdgeOptions()
option.add_argument("--user-data-dir=C:\\Users\\bericxz\\AppData\\Local\\Microsoft\\Edge\\User Data1"); 
option.add_argument("--profile-directory=Profile 3"); 
ser = Service("D:\\Utils\\msedgedriver.exe")    #Isi driver edge https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/
driver = webdriver.Edge(options=option, service=ser) #mau pake chrome jg bebas sih 
screen_height = driver.execute_script("return window.screen.height;") 

timeout = 5
scroll_pause_time = 1

for u in username:

    Path(u).mkdir(parents=True, exist_ok=True)
    list_existing_files(u)

    driver.get("https://www.instagram.com/"+u)
    time.sleep(timeout)
    i = 1
    ii=0
    #Pilih antara open highlights apa open feeds karena masi rusak pas pindah dr highlights ke feeds
    # open_highlights()
    open_feeds()
    
time.sleep(timeout)
driver.quit()


#abaikan line bawah ini, ini tadinya bekas infinite scroll profile ke bwh

    # while ii<10:
    #     # scroll one screen height each time
    #     x = driver.find_elements(By.TAG_NAME,"img") #Get all image tapi nggak bisa geser kalo dia ada banyak foto
    #     z = driver.find_elements(By.TAG_NAME,"a")

    #     # ahrefCount = 0
    #     for tag in z: 
    #         href = tag.get_attribute("href")
    #         print(href[25:])
    #         if href[25:28] == '/p/':
    #             try:
    #                 tag.click()
    #                 time.sleep(2)
    #                 break
    #             except:
    #                 print("error click")
    #         else:  
    #             continue
    #         # ahrefCount+=1
    #             # for iii in x:
    #             #     src = iii.get_attribute("src")
    #             #     # if any([x in src for x in matches]):
    #             #     filename = src[56:src.find('jpg')+3] 
    #             #     filename = filename.replace('?','')
    #             #     my_file = Path(username+"/"+filename)
    #             #     if my_file.is_file():
    #             #         print(filename+" exists!")
    #             #         continue
    #             #     elif check_face(src):
    #             #         print(filename+" has face")
    #             #         print("Downloading: "+filename)
    #             #         urllib.request.urlretrieve(src, username+"/"+filename)
    #             #         ii+=1
    #             # try:
    #                 # print ("xpath: "+xpath)
    #                 # showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #                 # showmore_link.click()
    #             # except ElementClickInterceptedException:
    #             #     print("Trying to click on the button again")
    #             #     driver.execute_script("arguments[0].click()", showmore_link)
    #     # for iii in x:
    #     #     src = iii.get_attribute("src")
    #     #     # if any([x in src for x in matches]):
    #     #     filename = src[56:src.find('jpg')+3] 
    #     #     filename = filename.replace('?','')
    #     #     my_file = Path(username+"/"+filename)
    #     #     if my_file.is_file():
    #     #         print(filename+" exists!")
    #     #         continue
    #     #     elif check_face(src):
    #     #         print(filename+" has face")
    #     #         print("Downloading: "+filename)
    #     #         urllib.request.urlretrieve(src, username+"/"+filename)
    #     #         ii+=1
    #     time.sleep(2)
    #     nextBtn = driver.find_element(By.CLASS_NAME,'_aaqg')
    #     nextBtn.click()
    #     ii+=1
    #     # driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    #     # i += 1

    #     # time.sleep(scroll_pause_time)
    #     # scroll_height = driver.execute_script("return document.body.scrollHeight;")  

