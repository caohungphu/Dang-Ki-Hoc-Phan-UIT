#Code by Cao Hung Phu - 19520214 - FB.com/caohungphuvn
#Url: https://dkhp.uit.edu.vn/sinhvien/hocphan/dangky

import os
import time
import requests
from os import path
from bs4 import BeautifulSoup

#Define
hp_file_taikhoan = "hp_taikhoan.txt"
hp_file_mamon = "hp_mamon.txt"

#Khai bao
hp_username = ""
hp_password = ""
hp_mamon = []
hp_check = True

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/83.0.144 Chrome/77.0.3865.144 Safari/537.36'
}

login_data = {
        'form_id': 'user_login',
        'op': 'Log in'
}

hocphan_data = {
        'loaimonhoc': '',
        'khoaql': '',
        'mamh': '',
        'op': 'Đăng ký',
        'form_id': 'uit_dkhp_dangky_form'
}
 
#Print info
def printInfo():
    os.system("color a")
    os.system("title TOOL DANG KI HOC PHAN UIT - HUNG PHU - 19520214")
    print(" ____                    _  ___ _   _            ____  _                 _   _ ___ _____ ")
    print("|  _ \  __ _ _ __   __ _| |/ (_) | | | ___   ___|  _ \| |__   __ _ _ __ | | | |_ _|_   _|")
    print("| | | |/ _` | '_ \ / _` | ' /| | |_| |/ _ \ / __| |_) | '_ \ / _` | '_ \| | | || |  | |  ")
    print("| |_| | (_| | | | | (_| | . \| |  _  | (_) | (__|  __/| | | | (_| | | | | |_| || |  | |  ")
    print("|____/ \__,_|_| |_|\__, |_|\_\_|_| |_|\___/ \___|_|   |_| |_|\__,_|_| |_|\___/|___| |_|  ")
    print("                   |___/                                                                 ")
    print("|==================> TOOL DANG KI HOC PHAN UIT - HUNG PHU - 19520214 <==================|\n")   
    print("+========================================LUU Y==========================================+")                                                                  
    print("|--> De check xem dang ki chua: Vao student.uit.edu.vn -> Sinh vien -> Thong tin DKHP   |")
    print("|--> Bam Ctrl + C de dung lai!                                                          |")
    print("+=======================================================================================+\n")

#Check file
def checkFile(hp_file):
    if path.exists(hp_file):
        return True
    return False

#Check main file
def checkMainFile():
    global hp_check
    if not checkFile(hp_file_taikhoan):
        print("|=> Error: Thieu file hp_taikhoan.txt!")
        hp_check = False
    if not checkFile(hp_file_mamon):
        print("|=> Error: Thieu file hp_mamon.txt!")
        hp_check = False

#Get tai khoan
def getTaiKhoan():
    global hp_username, hp_password, hp_check
    if checkFile(hp_file_taikhoan):
        with open(hp_file_taikhoan) as f:
            user_arr = f.read().splitlines()
        if (len(user_arr) != 2):
            print("|=> Error: File tai khoan gom 2 dong!")
            hp_check = False
        else:
            hp_username = user_arr[0]
            hp_password = user_arr[1]

#Get mon hoc
def getMonHoc():
    global hp_mamon
    if checkFile(hp_file_mamon):
        with open(hp_file_mamon) as f:
            hp_mamon = f.read().splitlines()

def printThongTinUser():
    print("+===================================THONG TIN DANG KI===================================+")
    print("|--> Dang ki cho sinh vien:",hp_username)
    print("|--> Mon hoc dang ki:", end=" ")
    print(*hp_mamon, sep=", ")
    print("+=======================================================================================+\n")

#Khoi tao dang ki
def initDangKi():
    global login_data, hocphan_data
    login_data['name'] = hp_username
    login_data['pass'] = hp_password
    hocphan_data['txtmasv'] = hp_username
    for mon in hp_mamon:
        str_mon = 'table_lophoc[' + mon + ']'
        hocphan_data[str_mon] = mon

#Dang ki
def DangKi():
    global login_data, hocphan_data
    with requests.Session() as s:
        url = "https://dkhp.uit.edu.vn/sinhvien/hocphan/dangky"
        r = s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        if (soup.find('input', attrs={'name' : 'form_build_id'})):
            print("|--> Loading success!!!")
            login_data['form_build_id'] = soup.find('input', attrs={'name' : 'form_build_id'})['value']
            #DangNhap
            r = s.post(url, data = login_data, headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            if ((soup.find('input', attrs={'name' : 'form_build_id'})) and (soup.find('input', attrs={'name' : 'form_token'}))):
                hocphan_data['form_build_id'] = soup.find('input', attrs={'name' : 'form_build_id'})['value']
                hocphan_data['form_token'] = soup.find('input', attrs={'name' : 'form_token'})['value']
                time.sleep(3) #Delay for bypass
            #DangKi
                r = s.post(url, data = hocphan_data, headers = headers)           
            print("|--> Registration status:", r.status_code)          
        else:
            print("|--> Loading fail!!! -> ", r.status_code)

#MAIN
def main():
    printInfo()
    checkMainFile()
    getTaiKhoan()
    getMonHoc()
    if (hp_check):
        printThongTinUser()
        initDangKi()
        print("=====================================BAT DAU DANG KI=====================================")
        num = 0
        while True:
            num += 1
            print("|--> STT:",num)
            DangKi()
            print("-----------------------------------------------------------------------------------------")
            time.sleep(3)
    os.system("pause")

if __name__ == "__main__":
    main()