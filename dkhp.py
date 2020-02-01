#Code by Hung Phu - 19520214 - FB.com/caohungphuvn
#Url: https://dkhp.uit.edu.vn/sinhvien/hocphan/dangky
import requests
import time
import sys
import os
from os import path
from bs4 import BeautifulSoup

#Khai bao
hp_username = ''
hp_password = ''
mamonhoc = []
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
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/83.0.144 Chrome/77.0.3865.144 Safari/537.36'
}

#Get User
def GetUser():
    global hp_username, hp_password
    with open(sys.argv[1]) as f:
        user_arr = f.read().splitlines()
    hp_username = user_arr[0]
    hp_password = user_arr[1]

#Get Mon Hoc
def GetMonHoc():
    global mamonhoc
    with open(sys.argv[2]) as f:
        mamonhoc = f.read().splitlines()
       
#Usage
def HDSD():
    os.system("cls")
    os.system("color a")
    os.system("title TOOL DANG KI HOC PHAN UIT - HUNG PHU - 19520214")
    print("=========================================================================================")
    print("|==================> TOOL DANG KI HOC PHAN UIT - HUNG PHU - 19520214 <==================|")
    print("=========================================================================================")
    print("--> HDSD: python dkhp.py [file user] [file ma mon]")
    print("--> Vd: python dkhp.py user.txt mamon.txt")
    print("--> Vui long thu lai!!!")
    print("=========================================================================================")

#Error path
def Error(file):
    print("--> Error: Khong tim thay tap tin: ", file,"!!!")
    
#Khai Bao
def Init():
    #Add mon hoc vao hocphan_data
    login_data['name'] = hp_username
    login_data['pass'] = hp_password
    hocphan_data['txtmasv'] = hp_username
    for mon in mamonhoc:
        str_mon = 'table_lophoc[' + mon + ']'
        hocphan_data[str_mon] = mon

#Dang Ki Mon Hoc
def DangKi():
    with requests.Session() as s:
        #DangNhap
        url = "https://dkhp.uit.edu.vn/sinhvien/hocphan/dangky"
        r = s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        if (soup.find('input', attrs={'name' : 'form_build_id'})):
            print("Loading success!!!")
            login_data['form_build_id'] = soup.find('input', attrs={'name' : 'form_build_id'})['value']
            r = s.post(url, data = login_data, headers = headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            if ((soup.find('input', attrs={'name' : 'form_build_id'})) and (soup.find('input', attrs={'name' : 'form_token'}))):
                hocphan_data['form_build_id'] = soup.find('input', attrs={'name' : 'form_build_id'})['value']
                hocphan_data['form_token'] = soup.find('input', attrs={'name' : 'form_token'})['value']
                time.sleep(3) #Delay for bypass
                r = s.post(url, data = hocphan_data, headers = headers)           
            print("Registration status:", r.status_code)                   
        else:
            print("Loading fail!!! -> ",r.status_code)
        
#Main
if (len(sys.argv) < 3):
    HDSD()
    sys.exit()
else:
    os.system("cls")
    os.system("color a")
    print("=========================================================================================")
    print("|==================> TOOL DANG KI HOC PHAN UIT - HUNG PHU - 19520214 <==================|")
    print("=========================================================================================")
    if (path.exists(sys.argv[1]) != True):
        Error(sys.argv[1])
    elif (path.exists(sys.argv[2]) != True):
        Error(sys.argv[2])
    else:
        GetUser()
        print("--> Dang ki cho sinh vien: ", hp_username)
        GetMonHoc()
        print("--> Mon hoc dang ki: ")
        for i in mamonhoc:
            print("  +", i)
        Init() 
        print("=========================================================================================")
        print("--> Dang dang ki...")
        print("--> De check xem dang ki chua: Vao student.uit.edu.vn -> Sinh vien -> Thong tin DKHP")
        print("--> Bam Ctrl + C de dung lai!")
        print("=========================================================================================")
        #Loop
        num = 0
        while True:
            num += 1
            print("STT:",num)
            DangKi()
            print("-----------------------------------------------------------")
            time.sleep(3)
   
    