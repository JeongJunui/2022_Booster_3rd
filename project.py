from asyncio.windows_events import NULL
from cgitb import text
#from curses import textpad
from glob import glob
from re import T
from jmespath import search
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import datetime as dt #날짜 관련 관리하는 라이브러리

send_data=''
send_data2=''

#rent, user, book_list 이 세개는 csv 파일에서 불러와서 인터페이스에 집어넣고 나면 안 써야 됩니다. 코드 본문에서 _list 쓰지 말고 인터페이스 경유해서 정보 받으세요

class Book:
    
    def __init__(self): #생성자
        self.__book=np.array([]) #self.__ : private
        self.__road_from_csv()
    def __road_from_csv(self):
        df=pd.read_csv('csv/Book.csv', encoding='UTF-8')
        book_list=np.array([])
        book_list=np.append(book_list,df)
        book_list=np.reshape(book_list,(int(book_list.size/9),9))
        book_list=book_list[:,1:]
        self.__book=book_list
    def get_Isbnlist(self): #접근자
        return self.__book[:0]

    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-007)
        book_col=["ISBN","TITLE","AUTHOR","PUB","PRICE","LINK","DESCRIP","PRE"] # 열 이름
        print(self.__book)
        bookdf=pd.DataFrame(self.__book, columns=book_col) # numpy 배열을 DataFrame 형식으로 변환
        bookdf.to_csv('csv/Book.csv', encoding='UTF-8') # to_csv는 numpy 배열에서 작동하지 않아 DataFrame으로 변환한 것
        self.__road_from_csv()
    
    def get_IsIn(self,isbn): # isbn이 안에 있는가 확인 (IF-001)
        if isbn in self.__book[:,0]: # 있으면 True 반환
            return True
        else:
            return False
    
    def add_Book_Info(self,inf): # 도서 등록 (IF-002)
        self.__book=np.append(self.__book,[inf],axis=0) # 행 방향으로 정보 추가
        self.save_to_csv()
        
    def get_Book_info(self,isbn): # 책 정보 확인
        ind=np.where(self.__book[:,0]==int(isbn)) #내부 인덱스를 찾아냄
        return self.__book[ind,:]# 인덱스에 해당하는 책 정보를 리턴

    def get_IsRented(self,isbn):#IF-008
        ind=np.where(self.__book[:,0]==isbn) #내부 인덱스를 찾아냄
        return self.__book[ind,7]
    def set_IsRented(self,isbn,rt):#IF-009
        ind=np.where(self.__book[:,0]==isbn) #내부 인덱스를 찾아냄
        self.__book[ind,7]=rt
        self.save_to_csv()
        
    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        search_list=np.array([]) # 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,1]==title)
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:]) # 제목이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록

    def search_Book_ByAuthor(self,author): # 책 저자로 검색 (IF-004)
        search_list=np.array([]) # 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,2]==author)
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:]) # 저자가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록
    
    def set_Book_Info(self,inf): # 도서 수정 (IF-005)
        ind=np.where(self.__book[:,0]==int(inf[0])) # 내부 인덱스를 찾아냄
        self.__book[ind,:]=inf# 인덱스 값에 해당하는 책 정보 삽입
        self.save_to_csv()
   
    def drop_Book_Info(self,isbn): # 도서 삭제 (IF-006)
        ind=np.where(self.__book[:,0]==isbn) # 내부 인덱스를 찾아냄
        self.__book=np.delete(self.__book,ind,axis=0)# 인덱스 값에 해당하는 정보 삭제
        self.save_to_csv()
        
class User:

    def __init__(self): # 생성자
        self.__user=np.array([]) #__ : private
        self.__road_from_csv()
    def __road_from_csv(self):
        df=pd.read_csv('csv/User.csv', encoding='UTF-8')
        user_list=np.array([])
        user_list=np.append(user_list,df)
        user_list=np.reshape(user_list,(int(user_list.size/9),9))
        user_list=user_list[:,1:]
        self.__user=user_list
    def get_Phonelist(self): # 접근자
        return self.__user[:,0]
    
    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-016)
        user_col=["PHONE","NAME","BIRTH","GENDER","MAIL","REG_DATE","OUT_DATE","RENT_CNT"]
        userdf=pd.DataFrame(self.__user, columns=user_col)
        userdf.to_csv('csv/User.csv', encoding='UTF-8') 
        self.__road_from_csv()

    def get_IsIn(self,phone): # 폰번호가 안에 있는가 확인 (IF-010)
        if phone in self.__user[:,0]: # 있으면 True 반환 np.isin(self.__user[:,0],phone)
            return True
        else:
            return False
        
    def get_User_info(self,phone): # 회원 정보 확인
        ind=np.where(self.__user[:,0]==phone) #내부 인덱스를 찾아냄
        return self.__user[ind,:] # 인덱스에 해당하는 책 정보 리턴
    
    def get_IsRented(self,phone):# 대출한 도서 갯수 반환(IF-017)
        ind=np.where(self.__user[:,0]==phone)#내부 인덱스를 찾아냄
        return self.__user[ind,7]

    def set_IsRented(self,phone,ud):#(IF-018)
        ind=np.where(self.__user[:,0]==phone)#내부 인덱스를 찾아냄
        self.__user[ind,7]+=ud#+1 혹은 -1을 받아서 계산
        self.save_to_csv()

    def add_User_Info(self,inf): # 회원 등록 (IF-011)
        self.__user=np.append(self.__user,[inf],axis=0) # 행 방향으로 정보 추가
        self.save_to_csv()
    
    def search_User_ByName(self,name): # 이름으로 회원 조회 (IF-012)
        search_list=np.array([]) # 검색된 회원 정보 저장할 리스트
        found_ind=np.where(self.__user[:,1]==name)
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:]) # 이름이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 회원 목록

    def search_User_ByPhone(self,phone): # 연락처로 회원 조회 (IF-013)
        search_list=np.array([]) # 검색된 회원 정보 저장할 리스트
        found_ind=np.where(self.__user[:,0]==phone)
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:]) # 연락처가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list# 반환 값 : 회원 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def set_User_Info(self,inf): # 회원 수정 (IF-014)
        ind=np.where(self.__user[:,0]==inf[0]) # 내부 인덱스를 찾아냄
        self.__user[ind,:]=inf # 인덱스 값에 해당하는 회원 정보 삽입
        self.save_to_csv()

    def drop_User_Info(self,phone,dat): # 회원 탈퇴 (IF-015)
        ind=np.where(self.__user[:,0]==phone) # 내부 인덱스를 찾아냄
        self.__user[ind,6]=dat # 인덱스 값에 해당하는 회원 탈퇴일자 저장
        self.save_to_csv()
        # 회원 탈퇴 시 재가입을 할 수도 있는경우를 위해회원을 삭제 하는 것이 아니라 탈퇴 날짜를 지정해줌

class Rent:
    def __init__(self): # 생성자
        self.__rent=np.array([])
        self.__road_from_csv()
    def __road_from_csv(self):
        df=pd.read_csv('csv/Rent.csv', encoding='UTF-8')
        rent_list=np.array([]) # 넘파이 빈리스트 생성
        rent_list=np.append(rent_list,df) # 값들을 append를 사용해 추가
        rent_list=np.reshape(rent_list,(int(rent_list.size/7),7)) # size행 8열로 모양 변환
        rent_list=rent_list[:,1:] #저장 시 생기는 인덱스 제거
        self.__rent=rent_list
            
    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-023)
        rent_col=["SEQ","ISBN","PHONE","DATE","RETURN_DATE","RETURN_YN"]
        rentdf=pd.DataFrame(self.__rent, columns=rent_col)
        rentdf.to_csv('csv/Rent.csv', encoding='UTF-8')
        self.__road_from_csv()
        
    def get_Rent_Info(self,ind): # 실제 인덱스 번호가 아니라 대출 테이블 내에 저장된 인덱스 번호를 넣을 것
        return self.__rent[ind-1,:]
    
    def rent_Book(self,isbn,phone,dat,datr): # 도서대출  (IF-019)
        add_info=np.array([int(self.__rent.size/6)+1,isbn,phone,dat,datr,False])# 대출 정보를 numpy 형태로 변환
        # 날짜 형식 계산은 나중에 추가할 예정
        self.__rent=np.append(self.__rent,[add_info],axis=0)# 대출 목록에 추가
        self.save_to_csv()
        
    def search_Rent_ByBook(self,isbn): # ISBN으로 대출 조회 (IF-020)
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind=np.where(self.__rent[:,1]==isbn)
        for i in found_ind:
            search_list=np.append(search_list,self.__rent[i,:])# ISBN이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록

    def search_Rent_ByUser(self, phone): # 연락처로 대출 조회 (IF-021)
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind=np.where(self.__rent[:,2]==phone)
        for i in found_ind:
            search_list=np.append(search_list,self.__rent[i,:])# 연락처가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록
        
    def back_Book(self,ind): # 도서 반납 (IF-022)
        self.__rent[ind-1,5]=True # 인덱스 값에 해당하는 대출 반납처리
        self.save_to_csv()

BO=Book()
US=User()
RE=Rent()

# Create object
root = Tk()

# Adjust size
root.geometry("1454x936")

def Book_Add():
    global confirmedISBN
    confirmedISBN="" # 중복확인한 ISBN 임시저장하는 문자열 변수, 체크할 때마다 저장할 것
    global isConfirmed # 체크를 했는가 저장하는 boolean 변수, 기본값은 False
    isConfirmed = False
    
    def get_user(): # ISBN 중복 확인을 위해 도서 리스트를 불러오는 위한 메소드
        global isConfirmed
        global confirmedISBN
        
        if textISBN.get().isdecimal()==False: # isdecimal : 주어진 문자열이 숫자로 되어있는지 검사하는 함수
            messagebox.showinfo("경고","ISBN은 숫자로만 입력해야 합니다.")
            return 0
            
        if BO.get_IsIn(int(textISBN.get())): # ISBN 집어넣어서 있으면 True(등록된 거 있음), 없으면 False 받아옴
            messagebox.showinfo("중복확인결과"," 이미 등록된 도서입니다.")
            isConfirmed=False
            
        else:
            messagebox.showinfo("중복확인결과","등록 가능한 도서입니다.")
            isConfirmed=True # 체크-> True
            confirmedISBN=textISBN.get() # 중복확인한 거 저장

    def add_book(): # 도서 등록을 위한 메소드
        global isConfirmed
        global confirmedISBN
        add_book_list=np.array([]) 
    
        if isConfirmed!=True: # 등록버튼을 눌렀을 때 isConfirmed가 False면 체크를 안 했다는 소리이므로 중복확인하라고 메세지박스 띄움
            messagebox.showinfo("경고","중복확인을 하세요")
            return 0
        
        else: # 등록버튼을 눌렀을 때
            if textISBN.get()!=confirmedISBN:  # get(): entry에서 입력된 값을 불러옴
                isConfirmed=False
                messagebox.showinfo("경고","중복확인을 다시 하세요")
                return 0
           
            if textBookName.get()=='' or textAuthor.get()=='' or textPub.get()=='': # 도서명,저자,출판사 셋중 하나를 입력하지 않았을경우 경고메세지 출력
                textWrite=""
                if textBookName.get()=='':
                    textWrite+="도서명이 입력되어있지 않습니다.\n" 
                elif textAuthor.get()=='':
                    textWrite+="저자명이 입력되어있지 않습니다.\n" 
                elif textPub.get()=='':
                    textWrite+="출판사가 입력되어있지 않습니다.\n"
                textWrite+="필수사항을 입력해주세요."
                messagebox.showinfo("경고",textWrite)  # 팝업창 처리
                return 0
            
            if textPrice.get().isdecimal()==False: # 가격이 숫자가 아닐경우
                messagebox.showinfo("경고","가격은 숫자만 입력하여야 합니다.")
                return 0
            
        add_book_list=np.append(add_book_list,textISBN.get()) # add_book_list에 값들을 저장
        add_book_list=np.append(add_book_list,textBookName.get())
        add_book_list=np.append(add_book_list,textAuthor.get())
        add_book_list=np.append(add_book_list,textPub.get())
        add_book_list=np.append(add_book_list,textPrice.get())
        add_book_list=np.append(add_book_list,textUrl.get())
        add_book_list=np.append(add_book_list,textDesc.get())
        add_book_list=np.append(add_book_list,True) # 대출 여부 초기값 True
        BO.add_Book_Info(add_book_list) # add_book_list를 book_list에 추가
        messagebox.showinfo("알림","도서 등록이 완료되었습니다.") # 팝업창
        confirmedISBN="" # 중복 등록 방지를 위해 초기화
        isConfirmed=False
        panedwindow1.destroy()

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 등록") # '도서등록' 화면에 출력 ( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=50)

    labelISBN = Label(panedwindow1, text="ISBN : ") # ' ISBN: ' 화면에 출력
    labelISBN.grid(row=1, column=0, padx=50, pady=10)
    textISBN = Entry(panedwindow1) # ISBN 넣는 텍스트박스
    textISBN.grid(row=1, column=1, padx=0, pady=10)
    btn_check_dup = Button(panedwindow1, text="중복확인", command=get_user) # "중복확인"버튼을 눌렀을 시에 get_user함수 호출
    btn_check_dup.grid(row=1, column=2, padx=50, pady=10) #화면을 표처럼 나눈다고 생각했을 때, 첫행, 두번째 열에 x축 공백을 50, y축 공백을 10으로 설정합니다

    labelBookName = Label(panedwindow1, text="도서명 : ") # ' 도서명: ' 화면에 출력
    textBookName = Entry(panedwindow1) #도서명 넣는 텍스트박스
    labelBookName.grid(row=2, column=0, padx=50, pady=10) #화면을 표처럼 나눈다고 생각했을 때, 두번째행, 0번째 열에 x축 공백을 50, y축 공백을 10으로 설정합니다
    textBookName.grid(row=2, column=1, padx=0, pady=10) #화면을 표처럼 나눈다고 생각했을 때, 두번째행, 1번째 줄에 x축 공백을 0, y축 공백을 10으로 설정합니다

    labelAuthor = Label(panedwindow1, text="저자 : ") # ' 저자: ' 화면에 출력
    textAuthor = Entry(panedwindow1) #저자 넣는 텍스트박스
    labelAuthor.grid(row=3, column=0, padx=50) #화면을 표처럼 나눈다고 생각했을 때, 세번째행, 0번째 줄에 x축 공백을 50, y축 공백을 10으로 설정합니다
    textAuthor.grid(row=3, column=1, padx=0) #화면을 표처럼 나눈다고 생각했을 때, 세번째행, 1번째 줄에 x축 공백을 0으로 설정합니다

    labelPub = Label(panedwindow1, text="출판사 : ") # ' 출판사: ' 화면에 출력
    textPub = Entry(panedwindow1) #출판사 넣는 텍스트박스
    labelPub.grid(row=4, column=0, padx=50, pady=10) #화면을 표처럼 나눈다고 생각했을 때, 4번째행, 0번째 줄에 x축 공백을 50, y축 공백을 10으로 설정합니다
    textPub.grid(row=4, column=1, padx=0, pady=10) #화면을 표처럼 나눈다고 생각했을 때, 4번째행, 1번째 줄에 x축 공백을 0, y축 공백을 10으로 설정

    labelPrice = Label(panedwindow1, text="가격 : ") # ' 가격: ' 화면에 출력
    textPrice = Entry(panedwindow1) #가격 넣는 텍스트박스
    labelPrice.grid(row=5, column=0, padx=50) #화면을 표처럼 나눈다고 생각했을 때, 5번째행, 0번째 줄에 x축 공백을 50으로 설정
    textPrice.grid(row=5, column=1, padx=0) #화면을 표처럼 나눈다고 생각했을 때, 5번째행, 1번째 줄에 x축 공백을 0으로 설정
    label_price_msg = Label(panedwindow1, text="가격은 쉼표 없이 숫자만 입력하세요!", fg = "red")  # 가격 입력 경고 문자
    label_price_msg.grid(row=6, column=1, padx=0)


    labelUrl = Label(panedwindow1, text="관련URL : ") # ' 관련URL: ' 화면에 출력
    textUrl = Entry(panedwindow1) #URL 넣는 텍스트박스
    labelUrl.grid(row=7, column=0, padx=50, pady=10)
    textUrl.grid(row=7, column=1, padx=0, pady=10)

    labelDesc = Label(panedwindow1, text="도서설명 : ") # ' 도서설명: ' 화면에 출력
    textDesc = Entry(panedwindow1) #도서설명 넣는 텍스트박스
    labelDesc.grid(row=8, column=0, padx=50)
    textDesc.grid(row=8, column=1, padx=0)

    btn_book_register = Button(panedwindow1, text="등록", command=add_book) # '등록' 버튼을 누를시에 add_book함수 호출
    btn_book_register.grid(row=9, column=0, padx=50, pady=10)
    # command=lambda: panedwindow1.pack_forget() -> 현재 panedwindow1 창을 닫음.
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget()) # '취소' 버튼을 누를시에 페이지 닫음
    btn_cancel.grid(row=9, column=1, padx=50, pady=10)


# 도서 조회
def Book_Search():

    def get_book_show(event): # 도서 조회시 도서를 선택했을 때 book show 클래스를 불러오는 메소드
        global send_data
        send_data=int(treeview.selection()[0])
        Book_Show() # 조회한 책의 정보를 출력하는 메소드

    def print_book_list(): # 도서 조회시 관련 도서의 리스트를 화면에 출력해주는 메소드
        #treeview랑 연계 
        searched_list=np.array([])
        if text_book_name.get(): # 도서명이 입력된 경우
            searched_list=BO.search_Book_ByTitle(text_book_name.get()) # 제목으로 도서 검색하는 함수 호출
            if not searched_list.all(): # 관련 도서명이 없는 경우
                messagebox.showinfo("경고","관련된 도서가 없습니다.\n올바른 제목을 입력해주세요.") # 팝업창
                return 0
            
        elif text_author.get(): # 저자명이 입력된 경우
            searched_list=BO.search_Book_ByAuthor(text_author.get()) # 책 저자로 검색하는 함수 호출
            if not searched_list.all(): # 관련 저자이름이 없는 경우
                messagebox.showinfo("경고","관련된 저자가 없습니다.\n올바른 저자이름을 입력해주세요.") # 팝업창
                return 0
                
        else:
            messagebox.showinfo("경고","도서명과 저자명 둘 중 하나라도 입력하시오")
            return 0
        
        treeview.delete(*treeview.get_children()) # treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        #treeV=[[for i in range(8)] for j in range(int(searched_list.size)/8)] # 2차원 배열
        for i in range(int(searched_list.size/8)):
            treeV=[]
            if searched_list[i,7]:#대출 여부에 따라 문장을 다르게 삽입
                treeV.append("X")
            else:
                treeV.append("대출 중")
            for j in range(1,6): # 대출여부 외에는 배치순서 동일하니 for문 처리
                treeV.append(searched_list[i,j-1])
            treeview.insert("", "end", text="", values=treeV, iid=treeV[1])
            treeview.bind("<Double-1>", get_book_show)
    
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 조회") # '도서 조회' 화면에 출력 ( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=10, pady=10)

    label_book_name = Label(panedwindow1, text="도서명 : ") # '도서명:' 화면에 출력
    label_book_name.grid(row=1, column=0, padx=10, pady=10)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=10, pady=10)
    btn_view = Button(panedwindow1, text="조회", command=print_book_list) # "조회"버튼을 누를시에 print_book_list함수 호출
    btn_view.grid(row=1, column=2, padx=10, pady=10)

    label_author = Label(panedwindow1, text="저자 : ") # '저자:' 화면에 출력
    label_author.grid(row=2, column=0, padx=10, pady=10)
    text_author = Entry(panedwindow1)
    text_author.grid(row=2, column=1, padx=10, pady=10)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    selectmode="browse")
    treeview.grid(row=3, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center")

    treeview.column("t_isbn", width=100, anchor="center") #검색해서 표출되는 표에서 isbn이 표시되는 열의 너비를 100으로 설정, 가운데 정렬
    treeview.heading("t_isbn", text="ISBN", anchor="center") #isbn이 표시되는 열의 제목에 ISBN이라는 텍스트를 넣고, 가운데 정렬

    treeview.column("t_title", width=100, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=100, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=100, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=100, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=100, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")


    treeview["show"] = "headings"

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget()) # "취소"버튼을 누를시에 창닫기
    btn_cancel.grid(row=4, column=1, padx=10, pady=10)

def Book_Show():
    # item = self.tree.selection()[0]
    global new
    global send_data
    bookInfo=BO.get_Book_info(int(send_data))[0,:]

    def modify_book(): # 수정 버튼을 눌렀을 때 원래 도서 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        #BO.set_Book_Info() # 도서 수정 함수 호출
        global bookInfo
        global send_data
        bookInfo=BO.get_Book_info(int(textISBN.get()))[0,:]
        if bookInfo[0,7]==False: # 대출중인 도서일 경우 -> 수정 불가능
            messagebox.showinfo("경고","대출 중인 도서는 수정할 수 없습니다.")
            return 0
        modify_list=np.array([])

        if textBookName.get()=='' or textAuthor.get()=='' or textPub.get()=='': # 도서명,저자,출판사 셋중 하나를 입력하지 않았을경우 경고메세지 출력
            textWrite=""
            if textBookName.get()=='':
                textWrite+="도서명이 입력되어있지 않습니다.\n" 
            elif textAuthor.get()=='':
                textWrite+="저자명이 입력되어있지 않습니다.\n" 
            elif textPub.get()=='':
                textWrite+="출판사가 입력되어있지 않습니다.\n"
            textWrite+="필수사항을 입력해주세요."
            messagebox.showinfo("경고",textWrite) # 팝업창 처리
            return 0
        
        if textPrice.get().isdecimal()==False: # 가격이 숫자가 아닐경우
            messagebox.showinfo("경고","가격은 숫자만 입력하여야 합니다.")
            return 0
                
        modify_list=np.append(modify_list,textISBN.get()) # modify_list에 값들 저장 / ISBN은 애초에 수정되지 않게 해야됨
        modify_list=np.append(modify_list,textBookName.get())
        modify_list=np.append(modify_list,textAuthor.get())
        modify_list=np.append(modify_list,textPub.get())
        modify_list=np.append(modify_list,textPrice.get())
        modify_list=np.append(modify_list,textUrl.get())
        modify_list=np.append(modify_list,textInfo.get())
        if textRent.get() == 'O':
            modify_list=np.append(modify_list, False)
        else:
            modify_list=np.append(modify_list, True)
        BO.set_Book_Info(modify_list) # set_Book_Info함수를 호출해 modify_list를 추가
        messagebox.showinfo("알림","도서 수정이 완료되었습니다.") # 팝업창
        bookInfo=BO.get_Book_info(textISBN.get())[0,:]


    def delete_book(): # 삭제 버튼을 눌렀을 때 해당된 도서 정보가 원래의 도서 리스트에서 삭제되어 도서 리스트에 저장 하기 위한 메소드
        if BO.get_IsRented(int(textISBN.get()))==False:
            messagebox.showinfo("경고","대출중인 도서는 삭제할 수 없습니다.")
            
        else:
            BO.drop_Book_Info(int(textISBN.get()))  # 도서 삭제 함수 호출 
            messagebox.showinfo("알림","해당 도서가 삭제되었습니다.") # 팝업창
            
    new = Toplevel()
    
    labelISBN = Label(new, text="ISBN : ")  # "ISBN : " 화면에 출력
    labelISBN.grid(row=1, column=0, padx=20, pady=20)
    textISBN = Entry(new)
    textISBN.insert(END,bookInfo[0,0])
    textISBN.grid(row=1, column=1, padx=20, pady=20)

    labelBookName = Label(new, text="도서명 : ") # "도서명 : " 화면에 출력
    textBookName = Entry(new)
    textBookName.insert(END,bookInfo[0,1])
    labelBookName.grid(row=2, column=0, padx=20)
    textBookName.grid(row=2, column=1, padx=20)

    labelAuthor = Label(new, text="저자 : ") # "저자 : " 화면에 출력
    textAuthor = Entry(new)
    textAuthor.insert(END,bookInfo[0,2])
    labelAuthor.grid(row=3, column=0, padx=20, pady=20)
    textAuthor.grid(row=3, column=1, padx=20, pady=20)

    labelPub = Label(new, text="출판사 : ") # "출판사 : " 화면에 출력
    textPub = Entry(new)
    textPub.insert(END,bookInfo[0,3])
    labelPub.grid(row=4, column=0, padx=20)
    textPub.grid(row=4, column=1, padx=20)

    labelPrice = Label(new, text="가격 : ")  # "가격 : " 화면에 출력
    textPrice = Entry(new)
    textPrice.insert(END,bookInfo[0,4])
    labelPrice.grid(row=5, column=0, padx=20, pady=20)
    textPrice.grid(row=5, column=1, padx=20, pady=20)

    labelUrl = Label(new, text="관련URL : ") # "관련URL : " 화면에 출력
    textUrl = Entry(new)
    textUrl.insert(END,bookInfo[0,5])
    labelUrl.grid(row=6, column=0, padx=20)
    textUrl.grid(row=6, column=1, padx=20)

    labelInfo = Label(new, text="설명 : ") # "설명 : " 화면에 출력 
    textInfo = Entry(new)
    textInfo.insert(END,bookInfo[0,6])
    labelInfo.grid(row=7, column=0, padx=20, pady=20)
    textInfo.grid(row=7, column=1, padx=20, pady=20)
    
    labelRent = Label(new, text="대출여부 : ") # "대출여부 : " 화면에 출력
    textRent = Entry(new)
    if bookInfo[0,7]:
        textRent.insert(END,'X')
    else:
        textRent.insert(END,'O')
    #textRent.insert(END,bookInfo[0,7])
    labelRent.grid(row=8, column=0, padx=20)
    textRent.grid(row=8, column=1, padx=20)

    btn_check_dup = Button(new, text="수정",command=modify_book) # '수정' 버튼을 누를시에 modify_book함수 호출
    btn_check_dup.grid(row=9, column=0, padx=10, pady=20)

    btn_check_dup = Button(new, text="삭제",command=delete_book) # '등록' 버튼을 누를시에 add_book함수 호출
    btn_check_dup.grid(row=9, column=1, padx=10, pady=20)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy()) # "취소" 버튼을 누를시에 창 닫기
    btn_check_dup.grid(row=9, column=2, padx=10, pady=20)

# 회원 등록 페이지
def User_Add():
    global confirmedHP
    confirmedHP="010-0000-0000" # 중복 확인한 전화번호 저장하는 문자열 변수, 체크할 때마다 저장할 것
    global isConfirmed # 중복 확인했는지 여부 저장하는 boolean 변수, 기본값은 False
    isConfirmed = False
    
    def check_user(): # 회원 중복 확인을 위한 메소드
        global isConfirmed
        global confirmedHP
        if US.get_IsIn(textHP.get()): # 중복되는 전화번호 있으면 True, 없으면 False
            messagebox.showinfo("중복확인결과","이미 등록된 회원입니다.") # 팝업창
            
        elif textHP.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
            messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
            return 0
        
        #elif textHP.get().isdigit()==False: # 전화번호가 숫자가 아닐경우-->'-'이 포함
        #    messagebox.showinfo("경고","전화번호는 숫자만 입력해야 합니다.") # 팝업창
        #    return 0
        
        else:
            messagebox.showinfo("중복확인결과","등록 가능한 회원입니다.") # 팝업창
            isConfirmed=True # 중복 확인했으므로 True
            confirmedHP=textHP.get() # 중복 확인한 전화번호 저장
    
    def add_user(): # 등록 버튼을 누를시에 이름, 생년월일, 전화번호, 성별, 이메일, 사진의 정보를 받아 원래 회원 리스트에 추가해주는 메소드
        global isConfirmed
        global confirmedHP
        add_user_list=np.array([])
    
        if isConfirmed != True: # 등록버튼을 눌렀을시에 중복확인을 하지 않았을 때(isConfirmed가 False면 체크를 안 했다는 소리이므로) 중복확인경고메세지 출력
            messagebox.showinfo("경고","중복확인을 하세요") # 팝업창
            return 0
        
        else: # 필수사항을 입력하지 않았을 때
            if textName.get()=='' or textBirth.get()=='' or textGender.get()=='' or textEmail.get()=='': # 이름,생년월일,성별,이메일 넷중 하나를 입력하지 않았을경우 경고메세지 
                textWrite=""
                if textName.get()=='':
                    textWrite+="회원명이 입력되어있지 않습니다.\n"
                elif textBirth.get()=='':
                    textWrite+="생년월일이 입력되어있지 않습니다.\n"
                elif textGender.get()=='':
                    textWrite+="성별이 입력되어있지 않습니다.\n" 
                elif textEmail.get()=='':
                    textWrite+="이메일이 입력되어있지 않습니다.\n"
                textWrite+="필수사항을 입력해주세요."
                messagebox.showinfo("경고",textWrite) # 팝업창 처리
                return 0
            
        if textHP.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
            messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
            return 0
            
        #if textBirth.get() # 생년월일이 숫자가 아닌 것일때 예외처리
            
        if textGender.get()!='남' and textGender.get()!='여': # 성별이 '남','여'가 아닐경우
            messagebox.showinfo("경고","성별은 '남' 혹은 '여' 둘 중 하나로만 입력해야 합니다.") # 팝업창
            return 0

        add_user_list=np.append(add_user_list,textHP.get()) # add_user_list에 값들 저장
        add_user_list=np.append(add_user_list,textName.get())
        add_user_list=np.append(add_user_list,textBirth.get())
        if textGender.get()=='남':
            add_user_list=np.append(add_user_list,True)
        else:
            add_user_list=np.append(add_user_list,False)
        add_user_list=np.append(add_user_list,textEmail.get())
        add_user_list=np.append(add_user_list,dt.datetime.now().strftime('%Y.%m.%d')) #사용자 정보를 추가하기 위해 만든 리스트에 datetime을 삽입. 연, 월, 일 형식으로
        add_user_list=np.append(add_user_list,'0')
        add_user_list=np.append(add_user_list,0) # 탈퇴날짜 빈값으로 기입
        US.add_User_Info(add_user_list)  # add_User_Info함수를 호출해 add_user_list값들을 추가
        messagebox.showinfo("알림","회원 등록이 완료되었습니다.") # 팝업창
        confirmedHP="" # 중복 등록 방지를 위해 초기화
        isConfirmed=False
        panedwindow1.destroy()

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 등록") # "회원 등록" 화면에 출력 ( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=50)

    labelName = Label(panedwindow1, text="이름 : ") # "이름 : " 화면에 출력
    labelName.grid(row=1, column=0, padx=50, pady=10)
    textName = Entry(panedwindow1) #이름 저장하는 텍스트박스
    textName.grid(row=1, column=1, padx=0, pady=10)


    labelBirth = Label(panedwindow1, text="생년월일 : ")  # "생년월일 : " 화면에 출력 
    textBirth = Entry(panedwindow1) #생년월일 저장하는 텍스트박스
    labelBirth.grid(row=2, column=0, padx=50)
    textBirth.grid(row=2, column=1, padx=0)
    label_Birth_msg = Label(panedwindow1, text="생년월일은 yyyy.mm.dd 형태로 입력해주세요!", fg = "red")
    label_Birth_msg.grid(row=3, column=1, padx=0)

    labelHP = Label(panedwindow1, text="전화번호 : ") # "전화번호 : " 화면에 출력 
    textHP = Entry(panedwindow1) #전화번호 저장하는 텍스트박스
    labelHP.grid(row=4, column=0, padx=50, pady=10)
    textHP.grid(row=4, column=1, padx=0, pady=10)
    label_HP_msg = Label(panedwindow1, text="전화번호는 000-0000-0000 형태로 '-'을 포함하여 입력해주세요!", fg = "red")
    label_HP_msg.grid(row=5, column=1, padx=0)
    btn_check = Button(panedwindow1, text="중복확인", command=check_user)
    btn_check.grid(row=4, column=2, padx=50, pady=10)


    labelGender = Label(panedwindow1, text="성별 : ")  # "성별 : " 화면에 출력 
    textGender = Entry(panedwindow1) #성별 저장하는 텍스트박스
    labelGender.grid(row=6, column=0, padx=50)
    textGender.grid(row=6, column=1, padx=0)

    labelEmail = Label(panedwindow1, text="이메일 : ")  # "이메일 : " 화면에 출력
    textEmail = Entry(panedwindow1) #이메일 저장하는 텍스트박스
    labelEmail.grid(row=7, column=0, padx=50, pady=10)
    textEmail.grid(row=7, column=1, padx=0, pady=10)

    labelJoin = Label(panedwindow1, text="가입일 : ") # "가입일 : " 화면에 출력
    labelJoin.grid(row=8, column=0, padx=50, pady=10)
    label_Join_msg = Label(panedwindow1, text="가입일은 자동으로 채워질 거예요!")
    label_Join_msg.grid(row=8, column=1, padx=0)

    labelJoin = Label(panedwindow1, text="탈퇴일 : ") # "탈퇴일 : " 화면에 출력
    labelJoin.grid(row=9, column=0, padx=50, pady=10)
    label_Join_msg = Label(panedwindow1, text="탈퇴일은 자동으로 채워질 거예요!")
    label_Join_msg.grid(row=9, column=1, padx=0)

    btn_book_register = Button(panedwindow1, text="등록", command=add_user) # "등록" 버튼 누를시에 add_user함수 호출
    btn_book_register.grid(row=10, column=0, padx=50, pady=10)
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget()) # "취소"버튼 누를시에 창 닫기
    btn_cancel.grid(row=10, column=1, padx=50, pady=10)

#회원 조회
def User_Search():

    def get_user_show(event): # 회원 조회 시 회원을 선택했을 때 book show 클래스를 불러오는 메소드
        global send_data
        send_data=treeview.selection()[0]
        User_Show()
    def get_user(): # 회원 정보를 불러오는 메소드
        searched_list=np.array([])
        if text_user_name.get(): # 사용자 이름으로 조회할 경우 
            searched_list=US.search_User_ByName(text_user_name.get())
            if not searched_list.all(): # 해당 사용자가 없을 경우
                messagebox.showinfo("경고","해당되는 사용자가 없습니다.")
                return 0
        
        elif text_phone.get(): # 사용자 폰번호로 조회할 경우
            if text_phone.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
                messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
                return 0
            searched_list=US.search_User_ByPhone(text_phone.get())
            if not searched_list.all(): # 해당 전화번호가 없을 경우
                messagebox.showinfo("경고","해당되는 전화번호가 없습니다.")
                return 0
        
        else: # 사용자 이름, 폰번호 둘다 입력하지 않은 경우
            messagebox.showinfo("경고","이름과 연락처 둘 중 하나라도 입력하시오")
            return 0
        
        print(searched_list)
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        #treeV=[[for i in range(8)] for j in range(int(searched_list.size)/8)]#2차원 배열
        for i in range(int(searched_list.size/8)):
            treeV=[]
            treeV.append(searched_list[i,1])
            treeV.append(searched_list[i,2])
            treeV.append(searched_list[i,0])
            if searched_list[i,3]:
                treeV.append('남')
            else:
                treeV.append('여')
            treeV.append(searched_list[i,4])
            if searched_list[i,7]!=0:
                treeV.append('O')
            else:
                treeV.append('X')
            if searched_list[i,6] == '0':
                treeV.append('X')
            else:
                treeV.append('탈퇴한 회원')
            treeview.insert("", "end", text="", values=treeV, iid=treeV[2])
            treeview.bind("<Double-1>", get_user_show)
        
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 조회") # "회원 조회" 화면에 출력 ( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=10, pady=10)

    label_user_name = Label(panedwindow1, text="이름 : ") # "이름 : " 화면에 출력
    label_user_name.grid(row=1, column=0, padx=10, pady=10)
    text_user_name = Entry(panedwindow1) #사용자 이름을 입력 받을 엔트리를 화면에 삽입
    text_user_name.grid(row=1, column=1, padx=10, pady=10) # 전체 화면을 표라고 가정하면 1행, 1열에 x축으로 여백을 10, y축으로 여백을 10 둠
    btn_view = Button(panedwindow1, text="조회",command=get_user) # "조회"버튼을 눌렀을 때 get_user함수 호출
    btn_view.grid(row=1, column=2, padx=10, pady=10)

    label_phone = Label(panedwindow1, text="연락처 : ") # "연락처 : " 화면에 출력
    label_phone.grid(row=2, column=0, padx=10, pady=10)
    text_phone = Entry(panedwindow1)
    text_phone.grid(row=2, column=1, padx=10, pady=10)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check", "t_check_for_exit"],
                                    displaycolumns=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check", "t_check_for_exit"],
                                    selectmode='browse')
    treeview.grid(row=3, column=1)

    treeview.column("t_name", width=100, anchor="center")
    treeview.heading("t_name", text="이름", anchor="center")

    treeview.column("t_birth", width=100, anchor="center")
    treeview.heading("t_birth", text="생년월일", anchor="center")

    treeview.column("t_hp", width=100, anchor="center")
    treeview.heading("t_hp", text="전화번호", anchor="center")

    treeview.column("t_gender", width=100, anchor="center")
    treeview.heading("t_gender", text="성별", anchor="center")

    treeview.column("t_email", width=100, anchor="center")
    treeview.heading("t_email", text="메일", anchor="center")

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출여부", anchor="center")

    treeview.column("t_check_for_exit", width=100, anchor="center")
    treeview.heading("t_check_for_exit", text="탈퇴여부", anchor="center")

    treeview["show"] = "headings"

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=10, pady=10)

def User_Show():
    global send_data
    userInfo=US.get_User_info(send_data)[0]
    global new
    global isConfirmed
    isConfirmed=False

    def modify_user(): # 수정 버튼을 눌렀을 때 원래 회원 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        global userInfo
        if textHP.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
            messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
            return 0
        userInfo=US.get_User_info(textHP.get())[0]
        if userInfo[0,7]!=0: 
            messagebox.showinfo("경고","도서 대출 중인 회원의 정보는 수정할 수 없습니다.")
            return 0
        modify_user_list=np.array([])

        if textName.get()=='' or textBirth.get()=='' or textGender.get()=='' or textEmail.get()=='': # 이름,생년월일,성별,이메일 넷중 하나를 입력하지 않았을경우 경고메세지 
            textWrite=""
            if textName.get()=='':
                textWrite+="회원명이 입력되어있지 않습니다.\n"
            elif textBirth.get()=='':
                textWrite+="생년월일이 입력되어있지 않습니다.\n"
            elif textGender.get()=='':
                textWrite+="성별이 입력되어있지 않습니다.\n"
            elif textEmail.get()=='':
                textWrite+="이메일이 입력되어있지 않습니다.\n"
            textWrite+="필수사항을 입력해주세요."
            messagebox.showinfo("경고",textWrite) # 팝업창 처리
            return 0
        
        #if textBirth.get().isdecimal()==False: # 생년월일이 숫자가 아닌경우  --> '.'이 포함
        #    messagebox.showinfo("경고","생년월일은 숫자로만 입력해야 합니다.")
        #    return 0
        
        if textGender.get()!='남' and textGender.get()!='여': # 성별은 '여','남'이 아닐경우 
            messagebox.showinfo("경고","성별은 '남' 혹은 '여' 둘 중 하나로만 입력해야 합니다.")
            return 0

        modify_user_list=np.append(modify_user_list,textHP.get()) # modify_user_list에 값들을 저장
        modify_user_list=np.append(modify_user_list,textName.get())
        modify_user_list=np.append(modify_user_list,textBirth.get())
        if textGender.get()=='남':
            modify_user_list=np.append(modify_user_list,True)
        else:
            modify_user_list=np.append(modify_user_list,False)
        modify_user_list=np.append(modify_user_list,textEmail.get())
        modify_user_list=np.append(modify_user_list,userInfo[0,5])
        if userInfo[0,6] == '0':
            modify_user_list=np.append(modify_user_list,'0')
        else:
            modify_user_list=np.append(modify_user_list,userInfo[0,6])
        modify_user_list=np.append(modify_user_list,userInfo[0,7])
        US.set_User_Info(modify_user_list) # set_User_Info 함수를 호출해 modify_user_list를 추가
        messagebox.showinfo("알림","회원 수정이 완료되었습니다.") # 팝업창
        userInfo=US.get_User_info(textHP.get())[0]

    def reAdd_user(): # 수정 버튼을 눌렀을 때 원래 회원 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        global userInfo
        if textHP.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
            messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
            return 0
        userInfo=US.get_User_info(textHP.get())[0]
        modify_user_list=np.array([])

        if textName.get()=='' or textBirth.get()=='' or textGender.get()=='' or textEmail.get()=='': # 이름,생년월일,성별,이메일 넷중 하나를 입력하지 않았을경우 경고메세지 
            textWrite=""
            if textName.get()=='':
                textWrite+="회원명이 입력되어있지 않습니다.\n"          
            elif textBirth.get()=='':
                textWrite+="생년월일이 입력되어있지 않습니다.\n" 
            elif textGender.get()=='':
                textWrite+="성별이 입력되어있지 않습니다.\n"
            elif textEmail.get()=='':
                textWrite+="이메일이 입력되어있지 않습니다.\n"
            textWrite+="필수사항을 입력해주세요."
            messagebox.showinfo("경고",textWrite) # 팝업창 처리 
            return 0
        
        #if textBirth.get().isdecimal()==False: # 생년월일이 숫자가 아닌경우  --> '.'이 포함
        #    messagebox.showinfo("경고","생년월일은 숫자로만 입력해야 합니다.")
        #    return 0
        
        if textGender.get()!='남' and textGender.get()!='여': # 성별이 '남','여'가 아닐경우
            messagebox.showinfo("경고","성별은 '남' 혹은 '여' 둘 중 하나로만 입력해야 합니다.")
            return 0

        modify_user_list=np.append(modify_user_list,textHP.get()) # modify_user_list에 값들을 저장
        modify_user_list=np.append(modify_user_list,textName.get())
        modify_user_list=np.append(modify_user_list,textBirth.get())
        if textGender.get()=='남':
            modify_user_list=np.append(modify_user_list,True)
        else:
            modify_user_list=np.append(modify_user_list,False)
        modify_user_list=np.append(modify_user_list,textEmail.get())
        modify_user_list=np.append(modify_user_list,userInfo[0,5])
        modify_user_list=np.append(modify_user_list,'0')
        modify_user_list=np.append(modify_user_list,userInfo[0,7])
        US.set_User_Info(modify_user_list) # set_User_Info 함수를 호출해 modify_user_list를 추가
        messagebox.showinfo("알림","회원 재가입이 완료되었습니다.") # 팝업창
        userInfo=US.get_User_info(textHP.get())[0]

    def delete_user(): # 삭제 버튼을 눌렀을 때 해당 회원 정보가 원래의 회원 리스트에서 삭제되어 회원 리스트에 저장하기 위한 메소드
        phone=textHP.get()
        global isConfirmed
        
        if isConfirmed: # 이미 탈퇴된 회원일 경우
            messagebox.showinfo("경고","이미 처리되었습니다.")
            return 0
        
        if US.get_IsRented(phone)!=0: # 사용자가 도서 대출 중일 때
            messagebox.showinfo("경고","도서 대출 중인 회원은 탈퇴할 수 없습니다.")
            return 0
        
        else: 
            d=dt.datetime.now().strftime('%Y.%m.%d') # 반납 예정일 저장
            US.drop_User_Info(phone,d) # 회원탈퇴 메소드 호출
            messagebox.showinfo("알림","회원탈퇴가 완료되었습니다.")
            isConfirmed=True

    new = Toplevel()
    
    labelName = Label(new, text="이름 : ")  # "이름 : " 화면에 출력 
    labelName.grid(row=1, column=0, padx=20, pady=20)
    textName = Entry(new)
    textName.insert(END,userInfo[0,1])
    textName.grid(row=1, column=1, padx=20, pady=20)

    labelBirth = Label(new, text="생년월일 : ") # "생년월일 : " 화면에 출력
    textBirth = Entry(new)
    textBirth.insert(END,userInfo[0,2])
    labelBirth.grid(row=2, column=0, padx=20)
    textBirth.grid(row=2, column=1, padx=20)

    labelHP = Label(new, text="전화번호 : ") # "전화번호 : " 화면에 출력
    textHP = Entry(new)
    textHP.insert(END,userInfo[0,0])
    labelHP.grid(row=3, column=0, padx=20, pady=20)
    textHP.grid(row=3, column=1, padx=20, pady=20)

    labelGender = Label(new, text="성별 : ") # "성별 : " 화면에 출력
    textGender = Entry(new)
    if userInfo[0,3]:
        textGender.insert(END,'남')
    else:
        textGender.insert(END,'여')
    labelGender.grid(row=4, column=0, padx=20)
    textGender.grid(row=4, column=1, padx=20)

    labelEmail = Label(new, text="이메일: ") # "이메일: " 화면에 출력
    textEmail = Entry(new)
    textEmail.insert(END,userInfo[0,4])
    labelEmail.grid(row=5, column=0, padx=20, pady=20)
    textEmail.grid(row=5, column=1, padx=20, pady=20)

    labelJoin = Label(new, text="가입일 : ")  # "가입일 : " 화면에 출력
    textJoin = Entry(new)
    textJoin.insert(END,userInfo[0,5])
    labelJoin.grid(row=6, column=0, padx=20)
    textJoin.grid(row=6, column=1, padx=20)

    labelExit = Label(new, text="탈퇴일 : ") # "탈퇴일 : " 화면에 출력 
    textExit = Entry(new)
    textExit.insert(END,userInfo[0,6])
    labelExit.grid(row=7, column=0, padx=20, pady=20)
    textExit.grid(row=7, column=1, padx=20, pady=20)

    labelRent = Label(new, text="대출여부 : ") # "대출여부 : " 화면에 출력
    textRent = Entry(new)
    ins_st=''
    ins_st+=str(userInfo[0,7])+'권 대출중'
    textRent.insert(END,ins_st)
    labelRent.grid(row=8, column=0, padx=20)
    textRent.grid(row=8, column=1, padx=20)

    labelExit = Label(new, text="탈퇴여부 : ") # "탈퇴여부: " 화면에 출력
    textExit = Entry(new)
    ins_st=''
    if userInfo[0,6] == '0':
        ins_st='X'
    else:
        ins_st='O'
    textExit.insert(END,ins_st)
    labelExit.grid(row=9, column=0, padx=20, pady=20)
    textExit.grid(row=9, column=1, padx=20, pady=20)

    btn_check_dup = Button(new, text="수정",command=modify_user) # "수정" 버튼을 누를시에 modify_user함수 호출
    btn_check_dup.grid(row=10, column=0, padx=20)

    btn_check_dup = Button(new, text="탈퇴",command=delete_user) # "탈퇴" 버튼을 누를시에 delete_user함수 호출
    btn_check_dup.grid(row=10, column=1, padx=20)

    btn_check_dup = Button(new, text="재가입",command=reAdd_user) # "재가입" 버튼을 누를시에 reAdd_user함수 호출
    btn_check_dup.grid(row=11, column=0, padx=20, pady=20)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy()) # "취소" 버튼을 누를시에 new.destroy함수 호출
    btn_check_dup.grid(row=11, column=1, padx=20, pady=20)


#책 대여하기
def Rent_User_Search():
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)
        #ind,isbn,phone,dat
    global send_data
    
    def update_rent_situation(before): # 선택 버튼을 눌렀을 시에 해당 회원의 대출 여부가 도서 대출 중으로 바뀌어 저장하는 메소드
        phone=treeview.selection()[0]
        if US.get_User_info(phone)[0,0,6]!='0': 
            messagebox.showinfo("경고","이미 탈퇴한 회원입니다.")
            return 0
        
        if US.get_IsRented(phone)==3:#US.user_list[ind,8]==3: # 대출 진행 불가능 -> 해당 회원이 3권을 빌린 상태인지를 먼저 체크 
            messagebox.showinfo("경고","각 회원당 대출할 수 있는 최대 권수는 3권입니다.") 
            return 0
        
        global send_data
        send_data=phone
        messagebox.showinfo("알림","회원을 선택하였습니다.") # 팝업창
        Rent_Book_Search(before)
        #US.user_list[ind,8]+=1 # 대출 권수 1추가 
        #RE.rent_Book(isbn,phone,dat) # 대출 여부
        
    def print_rent_user(): # 이름 검색을 누를시에 회원 리스트와 대출여부가 출력되게 하는 메소드
        searched_list=np.array([])
        if text_user_name.get(): # 회원 이름으로 검색할 경우
            searched_list=US.search_User_ByName(text_user_name.get())
            
        elif text_phone.get(): # 회원 전화번호로 검색할 경우
            if text_phone.get()!=13: # 전화번호가 '-'을 포함한 13자리가 아닐 경우
                messagebox.showinfo("경고","전화번호는 '-'을 포함한 13자리를 입력해야 합니다.") # 팝업창
                return 0
            searched_list=US.search_User_ByPhone(text_phone.get())
            
        #elif text_phone.get().isdecimal()==False: # 전화번호가 숫자가 아닌경우 --> '-'포함
        #    messagebox.showinfo("경고","전화번호를 숫자로 입력하세요.")
        #    return 0
        
        else: # 회원 이름,전화번호 둘다 입력하지 않은 경우
            messagebox.showinfo("경고","이름과 연락처 둘 중 하나라도 입력하시오")
            return 0
        
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        for i in range(int(searched_list.size/8)):
            treeV=[]
            treeV.append(searched_list[i,1])
            treeV.append(searched_list[i,2])
            treeV.append(searched_list[i,0])
            if searched_list[i,3]:
                treeV.append('남')
            else:
                treeV.append('여')
            treeV.append(searched_list[i,4])
            if searched_list[i,7]!=0:
                treeV.append('도서 대출 중')
            else:
                treeV.append('대출한 도서 없음')
            if searched_list[i,6] == '0':
                treeV.append('X')
            else:
                treeV.append('탈퇴한 회원')
            treeview.insert("", "end", text="", values=treeV, iid=treeV[2])

    title = Label(panedwindow1, text="도서 대여 - 회원 선택") # "도서 대여 - 회원 선택" 화면에 출력( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=10, pady=10)

    label_user_name = Label(panedwindow1, text="이름 : ") # "이름 : " 화면에 출력
    label_user_name.grid(row=1, column=0, padx=10, pady=10)
    text_user_name = Entry(panedwindow1)
    text_user_name.grid(row=1, column=1, padx=10, pady=10)
    btn_view = Button(panedwindow1, text="조회",command=print_rent_user) # "조회"버튼을 눌렀을시에 print_rent_user 호출
    btn_view.grid(row=1, column=2, padx=10, pady=10)

    label_phone = Label(panedwindow1, text="연락처 : ")  # "연락처 : " 화면에 출력
    label_phone.grid(row=2, column=0, padx=10, pady=10)
    text_phone = Entry(panedwindow1)
    text_phone.grid(row=2, column=1, padx=10, pady=10)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check"],
                                    displaycolumns=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check"],
                                    selectmode="browse")
    treeview.grid(row=3, column=1)

    treeview.column("t_name", width=100, anchor="center")
    treeview.heading("t_name", text="이름", anchor="center") 

    treeview.column("t_birth", width=100, anchor="center")
    treeview.heading("t_birth", text="생년월일", anchor="center")

    treeview.column("t_hp", width=100, anchor="center")
    treeview.heading("t_hp", text="전화번호", anchor="center")

    treeview.column("t_gender", width=100, anchor="center")
    treeview.heading("t_gender", text="성별", anchor="center")

    treeview.column("t_email", width=100, anchor="center")
    treeview.heading("t_email", text="이메일", anchor="center")

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출상태", anchor="center")

    treeview["show"] = "headings"


    btn_select = Button(panedwindow1, text="선택", command=lambda: update_rent_situation(panedwindow1)) # "선택"버튼을 누를시에 update_rent_situation함수 실행
    btn_select.grid(row=4, column=0, padx=10, pady=10)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget()) # "취소" 버튼을 누를시에 창닫기
    btn_cancel.grid(row=4, column=1, padx=10, pady=10)

def Rent_Book_Search(before):
    global send_data2
    send_data2=''
    isChecked=False
    def check_book_rent(): # 도서 정보를 검색시에 해당 도서의 대출 여부 정보를 불러오는 메소드
        #Book_Search에서 도서명으로 검색했던 것처럼
        #treeview랑 연계 
        searched_list=np.array([])
        if text_member_name.get(): # 도서명이 입력된 경우
            searched_list=BO.search_Book_ByTitle(text_member_name.get()) # 제목으로 도서 검색하는 함수 호출
            if not searched_list.all(): # 해당 도서가 없을경우
                messagebox.showinfo("경고","해당되는 도서가 없습니다.\n올바른 제목을 입력해주세요.")
                return 0
            
        else: # 도서명을 입력하지 않았을 경우
            messagebox.showinfo("경고","도서명을 입력하시오")
            return 0
            
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        #treeV=[[for i in range(8)] for j in range(int(searched_list.size)/8)]#2차원 배열
        for i in range(int(searched_list.size/8)):
            treeV=[]#
            if searched_list[i,7]:#대출 여부에 따라 문장을 다르게 삽입
                treeV.append("x")
            else:
                treeV.append("대출 중")
            for j in range(1,6): #대출여부 외에는 배치순서 동일하니 for문 처리
                treeV.append(searched_list[i,j-1])
            treeview.insert("", "end", text="", values=treeV, iid=treeV[1])

    def update_rent_situation(before): # 선택 버튼을 눌렀을 시에 대출 상태가 대출중으로 바뀌어 저장되게하고, 대출 정보 화면을 띄어주게 하는 메소드
        isbn=int(treeview.selection()[0])
        if BO.get_IsRented(isbn)==False:
            messagebox.showinfo("경고","이미 대출 중인 도서입니다.") # 팝업창
            return 0
        global send_data2
        send_data2=isbn
        messagebox.showinfo("알림","도서가 선택되었습니다.") # 팝업창
        global isChecked
        isChecked=True
        Rent_Show(before)

    before.pack_forget()

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 대여 - 도서 선택") # "도서 대여 - 도서 선택" 상단에 출력
    title.grid(row=0, column=1, padx=10, pady=10)

    label_member_name = Label(panedwindow1, text="도서 선택 : ") # "도서 선택 : " 화면에 출력
    label_member_name.grid(row=1, column=0, padx=10, pady=10)
    text_member_name = Entry(panedwindow1)
    text_member_name.grid(row=1, column=1, padx=10, pady=10)
    btn_view = Button(panedwindow1, text="조회", command=check_book_rent) # "조회" 버튼 누를시에 check_book_rent 함수 호출
    btn_view.grid(row=1, column=2, padx=10, pady=10)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    selectmode="browse")
    treeview.grid(row=2, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center") 

    treeview.column("t_isbn", width=100, anchor="center")
    treeview.heading("t_isbn", text="ISBN", anchor="center")

    treeview.column("t_title", width=100, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=100, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=100, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=100, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=100, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")

    treeview["show"] = "headings"

    btn_select = Button(panedwindow1, text="선택", command=lambda: update_rent_situation(panedwindow1))
    btn_select.grid(row=3, column=0, padx=10, pady=10)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=3, column=1, padx=10, pady=10)


def Rent_Show(before):
    global new
    global send_data
    global send_data2
    userInfo=US.get_User_info(send_data)[0,:]
    bookInfo=BO.get_Book_info(send_data2)[0,:]
    global isChecked
    isChecked=False
    global phone
    phone=userInfo[0,0]

    def save_rent(): # 대출 완료 버튼을 눌렀을 시에 대출 정보를 저장하는 메소드
        global isChecked
        global phone
        print(phone)
        if isChecked:
            messagebox.showinfo("경고","이미 처리되었습니다.")
            return 0
        d=dt.datetime.now()
        dr=(d+dt.timedelta(days=14)).strftime('%Y.%m.%d')
        d=d.strftime('%Y.%m.%d')
        isbn=textISBN.get()
        RE.rent_Book(isbn,phone,d,dr)
        US.set_IsRented(phone,1)
        BO.set_IsRented(int(isbn),False)
        messagebox.showinfo("알림","대출이 완료되었습니다.\n반납 예정 일자는 "+dr+"입니다.") # 팝업창
        isChecked=True

    new = Toplevel()

    labelTitle = Label(new, text="대출 정보") # "대출 정보" 화면에 출력 ( 상단의 타이틀 )
    labelTitle.grid(row=0, column=0, padx=20, pady=20)

    labelBookInfo = Label(new, text="도서 정보") # "도서 정보" 화면에 출력 ( 상단의 타이틀 )
    labelBookInfo.grid(row=1, column=0, padx=20, pady=20)

    labelMemboerInfo = Label(new, text="회원 정보")  # "회원명 : " 화면에 출력
    labelMemboerInfo.grid(row=1, column=2, padx=20, pady=20)

    labelBookName = Label(new, text="도서명 : ") # "도서명 : " 화면에 출력 
    textBookName = Entry(new)
    textBookName.insert(END,bookInfo[0,1])
    labelBookName.grid(row=2, column=0, padx=20)
    textBookName.grid(row=2, column=1, padx=20)
    labelName = Label(new, text="이름 : ")  # "이름 : " 화면에 출력 
    textName = Entry(new)
    textName.insert(END,userInfo[0,1])
    labelName.grid(row=2, column=2, padx=20)
    textName.grid(row=2, column=3, padx=20)

    labelAuthor = Label(new, text="저자 : ") # "저자 : " 화면에 출력
    textAuthor = Entry(new)
    textAuthor.insert(END,bookInfo[0,2])
    labelAuthor.grid(row=3, column=0, padx=20, pady=20)
    textAuthor.grid(row=3, column=1, padx=20, pady=20)
    labelBirth = Label(new, text="생년월일 : ") # "생년월일 : " 화면에 출력 
    textBirth = Entry(new)
    textBirth.insert(END,userInfo[0,2])
    labelBirth.grid(row=3, column=2, padx=20, pady=20)
    textBirth.grid(row=3, column=3, padx=20, pady=20)

    labelPub = Label(new, text="출판사 : ") # "출판사 : " 화면에 출력
    textPub = Entry(new)
    textPub.insert(END,bookInfo[0,3])
    labelPub.grid(row=4, column=0, padx=20)
    textPub.grid(row=4, column=1, padx=20)
    labelGender = Label(new, text="성별 : ") # "성별 : " 화면에 출력
    textGender = Entry(new)
    if userInfo[0,3]:
        textGender.insert(END,'남')
    else:
        textGender.insert(END,'여')
    labelGender.grid(row=4, column=2, padx=20)
    textGender.grid(row=4, column=3, padx=20)

    labelPrice = Label(new, text="가격 : ") # "가격 : "  화면에 출력
    textPrice = Entry(new)
    textPrice.insert(END,bookInfo[0,4])
    labelPrice.grid(row=5, column=0, padx=20, pady=20)
    textPrice.grid(row=5, column=1, padx=20, pady=20)
    labelEmail = Label(new, text="이메일 : ") # "이메일 : " 화면에 출력
    textEmail = Entry(new)
    textEmail.insert(END,userInfo[0,4])
    labelEmail.grid(row=5, column=2, padx=20, pady=20)
    textEmail.grid(row=5, column=3, padx=20, pady=20)

    labelUrl = Label(new, text="관련URL : ") # "관련URL : " 화면에 출력
    textUrl = Entry(new)
    textUrl.insert(END,bookInfo[0,5])
    labelUrl.grid(row=6, column=0, padx=20)
    textUrl.grid(row=6, column=1, padx=20)
    labelRentDay = Label(new, text="대여일 : ")  # "대여일 : " 화면에 출력
    textRentDay = Entry(new)
    d=dt.datetime.now()
    textRentDay.insert(END,d.strftime('%Y.%m.%d'))
    labelRentDay.grid(row=6, column=2, padx=20)
    textRentDay.grid(row=6, column=3, padx=20)

    labelISBN = Label(new, text="ISBN : ")
    labelISBN.grid(row=7, column=0, padx=20, pady=20)
    textISBN = Entry(new)
    textISBN.insert(END,bookInfo[0,0])
    textISBN.grid(row=7, column=1, padx=20, pady=20)

    labelBackDay = Label(new, text="반납 예정일 : ") # "반납 예정일 : " 화면에 출력
    textBackDay = Entry(new)
    d=d+dt.timedelta(days=14)
    textBackDay.insert(END,d.strftime('%Y.%m.%d'))
    labelBackDay.grid(row=7, column=2, padx=20, pady=20)
    textBackDay.grid(row=7, column=3, padx=20, pady=20)

    labelBackCheck = Label(new, text="반납 여부 : ") # "반납 여부 : "  화면에 출력
    textBackCheck = Entry(new)
    textBackCheck.insert(END,'X')
    labelBackCheck.grid(row=8, column=2, padx=20)
    textBackCheck.grid(row=8, column=3, padx=20)

    btn_check_dup = Button(new, text="대여하기",command=save_rent) # "대여하기" 버튼을 누를시에 save_rent함수 호출
    btn_check_dup.grid(row=9, column=1, padx=20, pady=20)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy()) #"취소"버튼을 누를시에 창닫기
    btn_check_dup.grid(row=9, column=2, padx=20, pady=20)


# 대여 책 조회
def Rent_Search():
    
    def get_rent(): # 대출 정보를 불러오는 메소드 
        #treeview랑 연계 
        isBook=False
        searched_list=np.array([])
        if text_book_name.get(): # 도서명이 입력된 경우
            searched_list=BO.search_Book_ByTitle(text_book_name.get()) # 제목으로 도서 검색하는 함수 호출
            isBook=True
            if not searched_list.all(): # 해당 도서가 없을 경우
                messagebox.showinfo("경고","해당 도서의 대출기록이 없습니다.")
                return 0
            
        elif text_member.get(): # 회원명이 입력된 경우
            searched_list=US.search_User_ByName(text_member.get()) # 회원명으로 검색하는 함수 호출
            if not searched_list.all(): # 해당 회원이 없을 경우
                messagebox.showinfo("경고","해당 회원은 대출기록이 없습니다.")
                return 0
        else:
            messagebox.showinfo("경고","도서명과 회원명 둘 중 하나라도 입력하시오")
            return 0
        
        searched_list=searched_list[:,0]
        if searched_list.size!=1:
            adv_search=np.array([])
            if isBook:
                for i in range(searched_list.size):
                    searched_rent=RE.search_Rent_ByBook(searched_list[i])
                    np.union1d(adv_search,searched_rent)
                #if np.isin(adv_search,searched_rent[0])[0]:
                #    continue
                #adv_search=np.append(adv_search,searched_rent)
                searched_list=np.reshape(searched_rent,(int(searched_rent.size/6),6))
            else:
                for i in range(searched_list.size):
                    searched_rent=RE.search_Rent_ByUser(searched_list[i])
                    np.union1d(adv_search,searched_rent)
                #if np.isin(adv_search,searched_rent[0])[0]:
                #    continue
                #adv_search=np.append(adv_search,searched_rent)
                searched_list=np.reshape(searched_rent,(int(searched_rent.size/6),6))
        else:
            if isBook:
                searched_list=RE.search_Rent_ByBook(searched_list[0])
            else:
                searched_list=RE.search_Rent_ByUser(searched_list[0])
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        for i in range(int(searched_list.size/6)):
            treeV=[]#
            if searched_list[i,5] == True:
                treeV.append('반납 완료')
            else:
                treeV.append('대출 중')
            rentBookInfo=BO.get_Book_info(searched_list[i,1])[0]
            for j in range(6):
                treeV.append(rentBookInfo[0,j])
            treeview.insert("", "end", text="", values=treeV, iid=searched_list[i,0])
            treeview.bind("<Double-1>", get_rent_state_show)
        
    def get_rent_state_show(event): # 대출 조회 시, 확인을 원하는 대출 내역을 선택했을 때 get_rent_state_show() 클래스를 불러오는 메소드-> gui
        global send_data
        send_data=treeview.selection()[0]
        Rent_State_Show()

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="대출 조회") # "대출 조회" 화면에 출력 ( 상단의 타이틀 )
    title.grid(row=0, column=1, padx=10, pady=10)

    label_book_name = Label(panedwindow1, text="도서명 : ") # "도서명 : " 화면에 출력
    label_book_name.grid(row=1, column=0, padx=10, pady=10)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=10, pady=10)
    btn_view = Button(panedwindow1, text="조회",command=get_rent)
    btn_view.grid(row=1, column=2, padx=10, pady=10)

    label_member = Label(panedwindow1, text="회원명 : " ) # "회원명 : " 화면에 출력
    label_member.grid(row=2, column=0, padx=10, pady=10)
    text_member = Entry(panedwindow1)
    text_member.grid(row=2, column=1, padx=10, pady=10)


    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    selectmode='browse')
    treeview.grid(row=3, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center")

    treeview.column("t_isbn", width=100, anchor="center")
    treeview.heading("t_isbn", text="ISBN", anchor="center")

    treeview.column("t_title", width=100, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=100, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=100, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=100, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=100, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")

    treeview["show"] = "headings"

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=10, pady=10)


def Rent_State_Show():
    global new
    global send_data
    rentInfo=RE.get_Rent_Info(int(send_data))
    bookInfo=BO.get_Book_info(int(rentInfo[1]))[0]
    userInfo=US.get_User_info(rentInfo[2])[0]
    global isBacked
    isBacked=False
    
    def book_return(): # 도서 반납 메소드
        global isBacked
        if isBacked or rentInfo[5]:
            messagebox.showinfo("경고","이미 처리되었습니다.") # 팝업창
            return 0
        RE.back_Book(rentInfo[0])
        US.set_IsRented(userInfo[0,0],-1)
        BO.set_IsRented(bookInfo[0,0],True)
        messagebox.showinfo("알림","반납 처리가 완료되었습니다.") # 팝업창
        isBacked=True

    new = Toplevel()

    labelTitle = Label(new, text="대출 정보")  # "대출 정보" 화면에 출력 ( 상단의 타이틀 )
    labelTitle.grid(row=0, column=0, padx=20, pady=20)

    labelBookInfo = Label(new, text="도서 정보") # "도서 정보" 화면에 출력 ( 상단의 타이틀 )
    labelBookInfo.grid(row=1, column=0, padx=20, pady=20)

    labelMemboerInfo = Label(new, text="회원 정보") # "회원 정보" 화면에 출력( 상단의 타이틀 )
    labelMemboerInfo.grid(row=1, column=2, padx=20, pady=20)

    labelBookName = Label(new, text="도서명 : ")  # "도서명 : " 화면에 출력 
    textBookName = Entry(new)
    textBookName.insert(END,bookInfo[0,1])
    labelBookName.grid(row=2, column=0, padx=20)
    textBookName.grid(row=2, column=1, padx=20)
    labelName = Label(new, text="이름 : ") # "이름 : " 화면에 출력
    textName = Entry(new)
    textName.insert(END,userInfo[0,1])
    labelName.grid(row=2, column=2, padx=20)
    textName.grid(row=2, column=3, padx=20)

    labelAuthor = Label(new, text="저자 : ")  # "저자 : " 화면에 출력
    textAuthor = Entry(new) # 저자 정보 엔트리 생성
    textAuthor.insert(END,bookInfo[0,2]) # bookInfo에서 저자에 해당하는 정보를 리스트에서 빼와서 넣음. 불러오는 과정은 사전에 수행이 되어 있음
    labelAuthor.grid(row=3, column=0, padx=20, pady=20)
    textAuthor.grid(row=3, column=1, padx=20, pady=20)
    labelBirth = Label(new, text="생년월일 : ")  # "생년월일 : " 화면에 출력 
    textBirth = Entry(new)
    textBirth.insert(END,userInfo[0,2])
    labelBirth.grid(row=3, column=2, padx=20, pady=20)
    textBirth.grid(row=3, column=3, padx=20, pady=20)

    labelPub = Label(new, text="출판사 : ") # "출판사 : " 화면에 출력
    textPub = Entry(new)
    textPub.insert(END,bookInfo[0,3])
    labelPub.grid(row=4, column=0, padx=20)
    textPub.grid(row=4, column=1, padx=20)
    labelGender = Label(new, text="성별 : ") # "성별 : " 화면에 출력
    textGender = Entry(new)
    if userInfo[0,3]:
        textGender.insert(END,'남')
    else:
        textGender.insert(END,'여')
    labelGender.grid(row=4, column=2, padx=20)
    textGender.grid(row=4, column=3, padx=20)

    labelPrice = Label(new, text="가격 : ")  # "가격 : "  화면에 출력
    textPrice = Entry(new)
    if bookInfo[0,4] == NULL:
        textPrice.insert(END,'')
    else:
        textPrice.insert(END,bookInfo[0,4])
    labelPrice.grid(row=5, column=0, padx=20, pady=20)
    textPrice.grid(row=5, column=1, padx=20, pady=20)
    labelEmail = Label(new, text="이메일 : ") # "이메일 : " 화면에 출력
    textEmail = Entry(new)
    textEmail.insert(END,userInfo[0,4])
    labelEmail.grid(row=5, column=2, padx=20, pady=20)
    textEmail.grid(row=5, column=3, padx=20, pady=20)

    labelUrl = Label(new, text="관련URL : ")  # "관련URL : " 화면에 출력
    textUrl = Entry(new)
    textUrl.insert(END,bookInfo[0,5])
    labelUrl.grid(row=6, column=0, padx=20)
    textUrl.grid(row=6, column=1, padx=20)
    labelRentDay = Label(new, text="대여일 : ") # "대여일 : " 화면에 출력
    textRentDay = Entry(new) # 대여일 정보가 삽입될 엔트리 생성
    textRentDay.insert(END,rentInfo[3])
    labelRentDay.grid(row=6, column=2, padx=20)
    textRentDay.grid(row=6, column=3, padx=20)

    labelISBN = Label(new, text="ISBN : ")  # "ISBN : " 화면에 출력
    labelISBN.grid(row=7, column=0, padx=20, pady=20)
    textISBN = Entry(new)
    textISBN.insert(END,bookInfo[0,0])
    textISBN.grid(row=7, column=1, padx=20, pady=20)
    labelBackDay = Label(new, text="반납 예정일 : ") # "반납 예정일 : " 화면에 출력
    textBackDay = Entry(new)
    textBackDay.insert(END,rentInfo[4])
    labelBackDay.grid(row=7, column=2, padx=20, pady=20)
    textBackDay.grid(row=7, column=3, padx=20, pady=20)

    labelBackCheck = Label(new, text="반납 여부 : ")  # "반납 여부 : "  화면에 출력
    textBackCheck = Entry(new)
    if rentInfo[5]:
        textBackCheck.insert(END,'O')
    else:
        textBackCheck.insert(END,'X')
    labelBackCheck.grid(row=8, column=2, padx=20)
    textBackCheck.grid(row=8, column=3, padx=20)

    btn_check_dup = Button(new, text="반납하기", command=book_return) # "반납하기" 버튼을 누를시에 book_return 호출
    btn_check_dup.grid(row=9, column=1, padx=20, pady=20)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy()) # "취소" 버튼을 누를시에 창 닫기
    btn_check_dup.grid(row=9, column=2, padx=20, pady=20)




# Add image file
bg = PhotoImage(file="background.png")

# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

my_frame = Frame(root)
my_frame.configure(bg='#B2CCFF')
my_frame.pack(pady=100)

label2 = Label(my_frame, text="도서 관리 메뉴") # "도서 관리 메뉴" 화면에 출력
label2.grid(row=0, column=0, padx=100, pady=10)
label2.configure(bg='#B2CCFF')
my_button1 = Button(my_frame, text="도서 등록", command=Book_Add) # "도서 등록" 버튼을 누를시에 Book_Add 함수 호출
my_button1.grid(row=1, column=0, padx=100)
my_button2 = Button(my_frame, text="도서 조회 수정 삭제", command=Book_Search) # "도서 조회 수정 삭제" 버튼을 누를시에 Book_Search 함수 호출
my_button2.grid(row=2, column=0, padx=100, pady=10)

label3 = Label(my_frame, text="회원 관리 메뉴") # "회원 관리 메뉴" 화면에 출력
label3.grid(row=0, column=1, padx=100, pady=10)
label3.configure(bg='#B2CCFF')
my_button3 = Button(my_frame, text="회원 등록", command=User_Add) # "회원 등록" 버튼을 누를시에 User_Add 함수 호출
my_button3.grid(row=1, column=1, padx=100)
my_button4 = Button(my_frame, text="회원 조회 수정 탈퇴", command=User_Search) # "회원 조회 수정 탈퇴" 버튼을 누를시에 User_Search 함수 호출
my_button4.grid(row=2, column=1, padx=100, pady=10)

label4 = Label(my_frame, text="도서 대출 메뉴") # "도서 대출 메뉴" 화면에 출력
label4.grid(row=0, column=2, padx=100, pady=10)
label4.configure(bg='#B2CCFF')
my_button5 = Button(my_frame, text="도서 대여", command=Rent_User_Search) # "도서 대여" 버튼을 누를시에 Rent_User_Search 함수 호출
my_button5.grid(row=1, column=2, padx=100)
my_button6 = Button(my_frame, text="대출 조회 반납" , command=Rent_Search) # "대출 조회 반납" 버튼을 누를시에 Rent_Search 함수 호출
my_button6.grid(row=2, column=2, padx=100, pady=10)

# Execute tkinter
root.mainloop()
