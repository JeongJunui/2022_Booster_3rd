#실행 전에 background.png 파일 제가 올린 gui 폴더에서 다운해서 소스코드랑 같은 폴더 내에 집어 넣고 돌려야 함요

from cgitb import text
import pandas as pd
import numpy as np
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
import datetime as dt #날짜 관련 관리하는 라이브러리

df=pd.read_csv('./Rent.csv', encoding='UTF-8') # cvs파일 불러옴
df1=pd.read_csv('./User.csv', encoding='UTF-8')
df2=pd.read_csv('./Book.csv', encoding='UTF-8')

rent_list=np.array([]) # 넘파이 빈리스트 생성
rent_list=np.append(rent_list,df) # 값들을 append를 사용해 추가
rent_list=np.reshape(rent_list,(int(rent_list.size/7),7)) # size행 8열로 모양 변환
rent_list=rent_list[:,1:] #저장 시 생기는 인덱스 제거

user_list=np.array([])
user_list=np.append(user_list,df1)
user_list=np.reshape(user_list,(int(user_list.size/9),9))
user_list=user_list[:,1:]

book_list=np.array([])
book_list=np.append(book_list,df2)
book_list=np.reshape(book_list,(int(book_list.size/9),9))
book_list=book_list[:,1:]

#rent, user, book_list 이 세개는 csv 파일에서 불러와서 인터페이스에 집어넣고 나면 안 써야 됩니다. 코드 본문에서 _list 쓰지 말고 인터페이스 경유해서 정보 받으세요

class Book:
    
    def __init__(self,book): #생성자
        self.__book=book #self.__ : private
    def get_Isbnlist(self): #접근자
        return self.__book[:0]

    #def get_AllInfo(self): # 저장할 때 정보를 전부 불러오는 용도, 우선은 사용하지 않아 더미 데이터 처리
        #return self.__book

    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-007)
        book_col=["ISBN","TITLE","AUTHOR","PUB","PRICE","LINK","DESCRIP","PRE"] # 열 이름
        bookdf=pd.DataFrame(self.__book, columns=book_col) # numpy 배열을 DataFrame 형식으로 변환
        bookdf.to_csv('./Book.csv', encoding='UTF-8') # to_csv는 numpy 배열에서 작동하지 않아 DataFrame으로 변환한 것
    
    def get_IsIn(self,isbn): # isbn이 안에 있는가 확인 (IF-001)
        if isbn in self.__book[:,0]: # 있으면 True 반환
            return True
        else:
            return False
    
    def add_Book_Info(self,inf): # 도서 등록 (IF-002)
        self.__book=np.append(self.__book,inf,asix=0)# 행 방향으로 정보 추가
        self.save_to_csv()
        
    def get_Book_info(self,isbn): # 책 정보 확인
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        return self.__book[ind,:]# 인덱스에 해당하는 책 정보를 리턴

    def get_IsRented(self,isbn):#IF-008
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        return self.__book[ind,7]
    def set_IsRented(self,isbn,rt):#IF-009
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        self.__book[ind,7]=rt
        self.save_to_csv()
        
    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        """
        for s in len(str(title)): # 검색된 문자열을 문자열 길이만큼 반복문으로 돌림
            stitle+=s # 반복하며 문자열이 추가 됨
            if self.__book[:,1].at(stitle): # 만약 반복하다가 같은 문자열이 발견된다면
                ind=np.where(self.__book[:,1]==stitle) # 일단 인덱스를 가져옴
                if isChecked.at(ind): # 만약 이미 확인한 인덱스면
                    continue # 넘어감
                isChecked=np.append(isChecked,ind) # 확인을 했다는 의미로 추가
                search_list=np.append(search_list,self.__book[ind,:])# 제목이 유사하므로 리스트에 추가
        return search_list # 비슷한 문자열을 가진 도서목록을 출력해줌 

        """
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,1])
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:])# 제목이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def search_Book_ByAuthor(self,author): # 책 저자로 검색 (IF-004)
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        found_ind=np.where(self.__book[:,2])
        for i in found_ind:
            search_list=np.append(search_list,self.__book[i,:])# 저자가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list # 반환 값 : 도서 목록
    
    def set_Book_Info(self,inf): # 도서 수정 (IF-005)
        ind=np.where(self.__book[:,0]==inf[0])#내부 인덱스를 찾아냄
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 책 정보 삽입
        self.save_to_csv()
   
    def drop_Book_Info(self,isbn): # 도서 삭제 (IF-006)
        ind=np.where(self.__book[:,0]==isbn)#내부 인덱스를 찾아냄
        self.__book=np.delete(self.__book,ind)# 인덱스 값에 해당하는 정보 삭제
        self.save_to_csv()
        
class User:

    def __init__(self,user): #생성자
        self.__user=user #__ : private
    def get_Phonelist(self): #접근자
        return self.__user[:0]
    
    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-016)
        user_col=["PHONE","NAME,BIRTH","GENDER","MAIL","REG_DATE","OUT_DATE","RENT_CNT"]
        userdf=pd.DataFrame(self.__user, columns=user_col)
        userdf.to_csv('./User.csv', encoding='UTF-8')
    def get_IsIn(self,phone): # 폰번호가 안에 있는가 확인 (IF-010)
        if phone in self.__user[:,0]: # 있으면 True 반환
            return True
        else:
            return False
        
    def get_User_info(self,phone): # 회원 정보 확인
        ind=np.where(self.__user[:,0]==phone)#내부 인덱스를 찾아냄
        return self.__user[ind,:]# 인덱스에 해당하는 책 정보 리턴
    
    def get_IsRented(self,phone):# 대출한 도서 갯수 반환(IF-017)
        ind=np.where(self.__user[:,0]==phone)#내부 인덱스를 찾아냄
        return self.__user[ind,7]

    def set_IsRented(self,phone,ud):#(IF-018)
        ind=np.where(self.__book[:,0]==phone)#내부 인덱스를 찾아냄
        self.__user[ind,7]+=ud#+1 혹은 -1을 받아서 계산
        self.save_to_csv()

    def add_User_Info(self,inf): # 회원 등록 (IF-011)
        self.__user=np.append(self.__book,inf,axis=0) # 행 방향으로 정보 추가
        self.save_to_csv()
    
    def search_User_ByName(self,name): # 이름으로 회원 조회 (IF-012)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        found_ind=np.where(self.__user[:,1])
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:])# 이름이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list# 반환 값 : 회원 목록

    def search_User_ByPhone(self,phone): # 연락처로 회원 조회 (IF-013)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        found_ind=np.where(self.__user[:,0])
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:])# 연락처가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/8),8))
        return search_list# 반환 값 : 회원 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def set_User_Info(self,inf): # 회원 수정 (IF-014)
        ind=np.where(self.__book[:,0]==inf[0])#내부 인덱스를 찾아냄
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 회원 정보 삽입
        self.save_to_csv()

    def drop_User_Info(self,phone,dat): # 회원 탈퇴 (IF-015)
        ind=np.where(self.__book[:,0]==phone)#내부 인덱스를 찾아냄
        self.__user[ind,6]=dat# 인덱스 값에 해당하는 회원 탈퇴일자 저장
        self.save_to_csv()
        # 회원 탈퇴 시 재가입을 할 수도 있는경우를 위해회원을 삭제 하는 것이 아니라 탈퇴 날짜를 지정해줌

class Rent:
    def __init__(self,rent): # 생성자
        self.__rent=rent
            
    def save_to_csv(self): # 변동사항 생길 때마다 저장(IF-023)
        rent_col=["SEQ","ISBN","PHONE","DATE","RETURN_DATE","RETURN_YN"]
        rentdf=pd.DataFrame(self.__rent, columns=rent_col)
        rentdf.to_csv('./Rent.csv', encoding='UTF-8')
        
    def get_Rent_Info(self,ind):#실제 인덱스 번호가 아니라 대출 테이블 내에 저장된 인덱스 번호를 넣을 것
        return self.__rent[ind-1,:]
    
    def rent_Book(self,isbn,phone,dat): # 도서대출  (IF-019)
        add_info=np.array([int(self.__rent.size/6)+1,isbn,phone,dat,dat+timedelta(days=14),False])# 대출 정보를 numpy 형태로 변환
        # 날짜 형식 계산은 나중에 추가할 예정
        self.__rent=np.append(self.__rent,add_info,axis=0)# 대출 목록에 추가
        self.save_to_csv()
        
    def search_Rent_ByBook(self,isbn): # ISBN으로 대출 조회 (IF-020)
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind=np.where(self.__rent[:,1])
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:])# ISBN이 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록

    def search_Rent_ByUser(self, phone): # 연락처로 대출 조회 (IF-021)
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        found_ind=np.where(self.__rent[:,2])
        for i in found_ind:
            search_list=np.append(search_list,self.__user[i,:])# 연락처가 동일하면 리스트에 추가
        search_list=np.reshape(search_list,(int(search_list.size/6),6))
        return search_list # 반환 값 : 대출 목록
        
    def back_Book(self,ind): # 도서 반납 (IF-022)
        self.__rent[ind-1,5]=True # 인덱스 값에 해당하는 대출 반납처리
        self.save_to_csv()

BO=Book(book_list)
US=User(user_list)
RE=Rent(rent_list)

# Create object
root = Tk()

# Adjust size
root.geometry("1454x936")
root.resizable(0, 0)

# 버튼 클릭 이벤트 핸들러
def Book_Add():

    confirmedISBN="" # 중복확인한 ISBN 임시저장하는 문자열 변수, 체크할 때마다 저장할 것
    isConfirmed=False # 체크를 했는가 저장하는 boolean 변수, 기본값은 False
    def get_user(): # ISBN 중복 확인을 위해 도서 리스트를 불러오는 위한 메소드
        if BO.get_IsIn("""textISBN에서 문자열 불러와서 집어넣기"""): # ISBN 집어넣어서 있으면 True(등록된 거 있음), 없으면 False 받아옴
            messagebox.showinfo("중복확인결과"," 이미 등록된 도서입니다.")
        else:
            messagebox.showinfo("중복확인결과","등록 가능한 도서입니다.")
            isConfirmed=True # 체크-> True
            confirmedISBN="""textISBN에서 불러온 문자열""" # 중복확인한 거 저장

    def add_book():
        add_book_list=np.array([])
    
        if: #등록버튼을 눌렀을 때 isConfirmed가 False면 체크를 안 했다는 소리이므로 중복확인하라고 메세지박스 띄우고 리턴(빠꾸) -> 버튼처리
            messagebox.showinfo("경고","중복확인을 하세요")
            return 0
        else:
            if textISBN!=confirmedISBN:
                isConfirmed=False
                messagebox.showinfo("경고","중복확인을 다시 하세요")
                return 0
            
            if textBookName.get()=='' or textAuthor.get()=='' or textPub.get()=='': # 도서명,저자,출판사 셋중 하나를 입력하지 않았을경우 경고메세지 출력
                #이거 and 말고 or 써야됩니다
                textWrite=""
                if textBookName=='':
                    textWrite+="도서명이 입력되어있지 않습니다.\n" # 팝업창 처리
                elif textAuthor=='':
                    textWrite+="저자명이 입력되어있지 않습니다.\n" # 팝업창 처리
                elif textPub=='':
                    textWrite+="출판사가 입력되어있지 않습니다.\n" # 팝업창 처리
                textWrite+="필수사항을 입력해주세요."
                messagebox.showinfo("경고",textWrite)
                return 0
        
        add_book_list=np.append(textISBN.get())
        add_book_list=np.append(textBookName.get())
        add_book_list=np.append(textAuthor.get())
        add_book_list=np.append(textPub.get())
        add_book_list=np.append(textPrice.get())
        add_book_list=np.append(textUrl.get())
        add_book_list=np.append(textDesc.get())
        add_book_list=np.append(True)
        #대출 여부 초기값 True로 배열에 추가해야 됩니다
        BO.add_Book_Info(add_book_list)
        messagebox.showinfo("알림","도서 등록이 완료되었습니다.")# 팝업창
        confirmedISBN="" # 중복 등록 방지를 위해 초기화
        isConfirmed=False

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 등록")
    title.grid(row=0, column=1, padx=100)

    labelISBN = Label(panedwindow1, text="ISBN : ")
    labelISBN.grid(row=1, column=0, padx=100)
    textISBN = Entry(panedwindow1) #ISBN 넣는 텍스트박스
    textISBN.grid(row=1, column=1, padx=100)
    btn_check_dup = Button(panedwindow1, text="등록")
    btn_check_dup.grid(row=1, column=2, padx=100)

    labelBookName = Label(panedwindow1, text="도서명 : ")
    textBookName = Entry(panedwindow1) #도서명 넣는 텍스트박스
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)

    labelAuthor = Label(panedwindow1, text="저자 : ")
    textAuthor = Entry(panedwindow1) #저자 넣는 텍스트박스
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)


    labelPub = Label(panedwindow1, text="출판사 : ")
    textPub = Entry(panedwindow1) #출판사 넣는 텍스트박스
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)

    labelPrice = Label(panedwindow1, text="가격 : ")
    textPrice = Entry(panedwindow1) #가격 넣는 텍스트박스
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)


    labelUrl = Label(panedwindow1, text="관련URL : ")
    textUrl = Entry(panedwindow1) #URL 넣는 텍스트박스
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)

    labelDesc = Label(panedwindow1, text="도서설명 : ")
    textDesc = Entry(panedwindow1) #도서설명 넣는 텍스트박스
    labelDesc.grid(row=7, column=0, padx=100)
    textDesc.grid(row=7, column=1, padx=100)

    btn_book_register = Button(panedwindow1, text="등록")
    btn_book_register.grid(row=8, column=0, padx=100)
    # command=lambda: panedwindow1.pack_forget() -> 현재 panedwindow1 창을 닫음.
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=8, column=1, padx=100)


# 도서 조회
def Book_Search():

    #def get_book_show(): # 도서 조회시 도서를 선택했을 때 book show 클래스를 불러오는 메소드 -> gui?
        #book_show.print_book_info() # 조회한 책의 정보를 출력하는 메소드
        #gui 불러오는 거니까 건드리지 않아도 됨

    def print_book_list(): # 도서 조회시 관련 도서의 리스트를 화면에 출력해주는 메소드
        #treeview랑 연계 
        searched_list=np.array([])
        if book_textbox.get(): # 도서명이 입력된 경우
            searched_list=BO.search_Book_ByTitle(text_book_name.get()) # 제목으로 도서 검색하는 함수 호출
        elif author_textbox.get(): # 저자명이 입력된 경우
            searched_list=BO.search_Book_ByAuthor(text_author.get()) # 책 저자로 검색하는 함수 호출
        else:
            messagebox.showinfo("경고","도서명과 저자명 둘 중 하나라")
        treeview.delete(*treeview.get_children())#treeview 전체를 지우는 문장
        #treeview에 넣을 데이터 정제 과정
        treeV=[[] for i in range(8)]#2차원 배열
        for i in range(int(searched_list.size)/8):
            if searched_list[i,7]:#대출 여부에 따라 문장을 다르게 삽입
                treeV[i,0]="X"
            else:
                treeV[i,0]="대출 중"
            for j in range(1,6):#대출여부 외에는 배치순서 동일하니 for문 처리
                treeV[i,j]=searched_list[i,j-1]
        #이하 treeview에 추가하는 for문
        for i in range(int(searched_list.size)/8):
            treeview.insert("", "end", text="", values=searched_list[i,:], iid=i)
            treeview.bind("<Double-1>", onDetailViewForBook)

    #def get_book(): # 도서 정보를 불러오는 메소드
        #print(BS.get_Book_info()) # 책 정보 확인 ( 도서 정보 리스트 출력 )
        #get_book_show랑 역할 겹치는 거 같은데 일단 보류
    
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 조회")
    title.grid(row=0, column=1, padx=100)

    label_book_name = Label(panedwindow1, text="도서명 : ")
    label_book_name.grid(row=1, column=0, padx=100)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회", command=print_book_list)
    btn_view.grid(row=1, column=2, padx=100)

    label_author = Label(panedwindow1, text="저자 : ")
    label_author.grid(row=2, column=0, padx=100)
    text_author = Entry(panedwindow1)
    text_author.grid(row=2, column=1, padx=100)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"])
    treeview.grid(row=3, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center")

    treeview.column("t_isbn", width=50, anchor="center")
    treeview.heading("t_isbn", text="ISBN", anchor="center")

    treeview.column("t_title", width=50, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=50, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=50, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=50, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=50, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")


    treeview["show"] = "headings"

    treeValueList = [("대출중", 9788970504773, "따라하며 배우는 파이썬과 데이터 과학", "천인국", "생능출판", 26000, "https://~"),
                     (" X ", 1234970504773, "예제 중심의 파이썬 입문", "황재호", "생능출판", 26000, "https://~")]

    for i in range(len(treeValueList)):
        treeview.insert("", "end", text="", values=treeValueList[i], iid=i)
        treeview.bind("<Double-1>", onDetailViewForBook)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=100)

def Book_Show(event):
    # item = self.tree.selection()[0]
    global new
    
    #def print_book_info(): # 조회한 책의 정보 출력을 위한 메소드
        #BO.get_Book_info() # 책 정보 확인 함수 호출
        #아마 생성자처럼 작동하는 거 같은데 일단 보류

    # 취소 버튼을 눌렀을때의 경우는 없는가 ?

    def modify_book(): # 수정 버튼을 눌렀을 때 원래 도서 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        #BO.set_Book_Info() # 도서 수정 함수 호출
        modify_list=np.array([])

        if textBookName.get()=='' or textAuthor.get()=='' or textPub.get()=='': # 도서명,저자,출판사 셋중 하나를 입력하지 않았을경우 경고메세지 출력
            textWrite=""
            if textBookName.get()=='':
                textWrite+="도서명이 입력되어있지 않습니다.\n" # 팝업창 처리
            elif textAuthor.get()=='':
                textWrite+="저자명이 입력되어있지 않습니다.\n" # 팝업창 처리
            elif textPub.get()=='':
                textWrite+="출판사가 입력되어있지 않습니다.\n" # 팝업창 처리
            textWrite+="필수사항을 입력해주세요."
            messagebox.showinfo("경고",textWrite)
            return 0

        modify_list=np.append(textISBN.get())
        modify_list=np.append(textBookName.get())
        modify_list=np.append(textAuthor.get())
        modify_list=np.append(textPub.get())
        modify_list=np.append(textPrice.get())
        modify_list=np.append(textUrl.get())
        modify_list=np.append(np.nan)
        #도서 설명이 빠져있어서 일단 null값으로 설정함
        modify_list=np.append(textRent)
        BO.set_Book_Info(modify_list)
        print("도서 수정이 완료되었습니다.") # 팝업창
        
        #isbn이 수정되는걸 체크해야되나 ?<-애초에 수정되면 안 되니 isbn을 아예 못 건드리게 하는게 좋을 거 같음

    def delete_book(): # 삭제 버튼을 눌렀을 때 해당된 도서 정보가 원래의 도서 리스트에서 삭제되어 도서 리스트에 저장 하기 위한 메소드
        if BO.get_IsRented(textIsbn.get()):#book_list[ind:8]==True:#BO.get_IsRented(ind)로 불러오시면 됩니다. 좀전에 
            messagebox.showinfo("경고","대출중인 도서는 삭제할 수 없습니다.")
        else:
            BO.drop_Book_Info()  # 도서 삭제 함수 호출
            messagebox.showinfo("알림","해당 도서가 삭제되었습니다.")# 팝업창
            
    def get_book(): # 도서 정보를 불러오는 메소드
        #print(BS)
        #print_book_info랑 겹치는 거 같은데 일단 보류

    new = Toplevel()
    labelISBN = Label(new, text="ISBN : ")
    labelISBN.grid(row=1, column=0, padx=100)
    
    textISBN = Entry(new)
    textISBN.grid(row=1, column=1, padx=100)

    labelBookName = Label(new, text="도서명 : ")
    textBookName = Entry(new)
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)

    labelAuthor = Label(new, text="저자 : ")
    textAuthor = Entry(new)
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)

    labelPub = Label(new, text="출판사 : ")
    textPub = Entry(new)
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)

    labelPrice = Label(new, text="가격 : ")
    textPrice = Entry(new)
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)

    labelUrl = Label(new, text="관련URL : ")
    textUrl = Entry(new)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)
    
    labelRent = Label(new, text="대출여부 : ") 
    textRent = Entry(new)
    labelRent.grid(row=7, column=0, padx=100)
    textRent.grid(row=7, column=1, padx=100)

    btn_check_dup = Button(new, text="수정",command=modify_book)
    btn_check_dup.grid(row=8, column=0, padx=100)

    btn_check_dup = Button(new, text="등록")
    btn_check_dup.grid(row=8, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=8, column=2, padx=100)

# 회원 등록 페이지
def User_Add():
    confirmedHP="010-0000-0000" # 중복 확인한 전화번호 저장하는 문자열 변수, 체크할 때마다 저장할 것
    isConfirmed=False # 중복 확인했는지 여부 저장하는 boolean 변수, 기본값은 False
    
    def check_user(): # 회원 중복 확인을 위한 메소드
        if US.get_IsIn(textHP): # 중복되는 전화번호 있으면 True, 없으면 False
            messagebox.showinfo(text="이미 등록된 회원입니다.") # 팝업창
        else:
            useradd_msgbox.showinfo(text="등록 가능한 회원입니다.") # 팝업창
            isConfirmed=True # 중복 확인했으므로 True
            confirmedHP=textHP # 중복 확인한 전화번호 저장
    
    def add_user(): # 등록 버튼을 누를시에 이름, 생년월일, 전화번호, 성별, 이메일, 사진의 정보를 받아 원래 회원 리스트에 추가해주는 메소드
        add_user_list=np.array([])
    
        if isConfirmed==False: # 등록버튼을 눌렀을 때 isConfirmed가 False면 체크를 안 했다는 소리이므로 중복확인하라고 메세지박스 띄우고 리턴(빠꾸) -> 버튼처리
            messagebox.showinfo("경고","중복확인을 하세요")
            return 0
        else:
            if textName.get()=='' or textBirth.get()=='' or textGender.get()=='' or textEmail.get()=='': # 이름,생년월일,성별,이메일 넷중 하나를 입력하지 않았을경우 경고메세지 
                #여기도 and 말고 or
                textWrite=""
                if textName.get()=='':
                    textWrite+="회원명이 입력되어있지 않습니다.\n" # 팝업창 처리
                elif textBirth.get()=='':
                    textWrite+="생년월일이 입력되어있지 않습니다.\n" # 팝업창 처리
                elif textGender.get()=='':
                    textWrite+="성별이 입력되어있지 않습니다.\n" # 팝업창 처리
                elif textEmail.get()=='':
                    textWrite+="이메일이 입력되어있지 않습니다.\n"
                textWrite+="필수사항을 입력해주세요."
                messagebox.showinfo("경고",textWrite)
                return 0
        
        d=dt.datetime.now().strftime('%Y-%m-%d')
        add_user_list=np.append(textName.get())
        add_user_list=np.append(textBirth.get())
        add_user_list=np.append(textHP.get())
        add_user_list=np.append(textGender.get())
        add_user_list=np.append(textEmail.get())
        #add_user_list=np.append(textUrl.get())#Url?
        #필요없는 값 같아서 주석처리
        add_user_list=np.append(dt.datetime.now().strftime('%Y-%m-%d'))
        add_user_list=np.append(np.nan)
        add_user_list=np.append(0)
        #가입일자 추가가 안 되어있네요
        #탈퇴일자도 빈 값으로 추가를 해주세요
        US.add_User_Info(add_user_list)
        messagebox.showinfo("알림","회원 등록이 완료되었습니다.")# 팝업창
        confirmedHP="" # 중복 등록 방지를 위해 초기화
        isConfirmed=False

    # def search_photo(): # PC에서 사용자 사진을 찾도록 하는 메소드 --> gui

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 등록")
    title.grid(row=0, column=1, padx=100)

    labelName = Label(panedwindow1, text="이름 : ")
    labelName.grid(row=1, column=0, padx=100)
    textName = Entry(panedwindow1) #이름 저장하는 텍스트박스
    textName.grid(row=1, column=1, padx=100)


    labelBirth = Label(panedwindow1, text="생년월일 : ")
    textBirth = Entry(panedwindow1) #생년월일 저장하는 텍스트박스
    labelBirth.grid(row=2, column=0, padx=100)
    textBirth.grid(row=2, column=1, padx=100)

    labelHP = Label(panedwindow1, text="전화번호 : ")
    textHP = Entry(panedwindow1) #전화번호 저장하는 텍스트박스
    labelHP.grid(row=3, column=0, padx=100)
    textHP.grid(row=3, column=1, padx=100)
    btn_check = Button(panedwindow1, text="중복확인", command=check_user)
    btn_check.grid(row=3, column=2, padx=100)


    labelGender = Label(panedwindow1, text="성별 : ")
    textGender = Entry(panedwindow1) #성별 저장하는 텍스트박스
    labelGender.grid(row=4, column=0, padx=100)
    textGender.grid(row=4, column=1, padx=100)

    labelEmail = Label(panedwindow1, text="이메일 : ")
    textEmail = Entry(panedwindow1) #이메일 저장하는 텍스트박스
    labelEmail.grid(row=5, column=0, padx=100)
    textEmail.grid(row=5, column=1, padx=100)


    labelPicture = Label(panedwindow1, text="사 진 : ") 
    textPicture = Entry(panedwindow1) #사진 저장하는 텍스트박스
    labelPicture.grid(row=6, column=0, padx=100)
    textPicture.grid(row=6, column=1, padx=100)
    btn_check = Button(panedwindow1, text="찾기")
    btn_check.grid(row=6, column=2, padx=100)

    btn_book_register = Button(panedwindow1, text="등록", command=add_user)
    btn_book_register.grid(row=7, column=0, padx=100)
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=7, column=1, padx=100)


#회원 조회
def User_Search():

    def get_user(ind): # 회원 정보를 불러오는 메소드
        #위에 Book_Search에서 하셨던 대로 하시면 되는데...
        
        #User.search_User_ByName(name) # 1. 이름으로 회원조회 -> 선택하는 과정 추가 ( 원하는 이름 선택)-> gui?
        #user=User.search_list[name,2] # 이름 선택
        #User.get_User_info(user) # 해당 회원의 정보 출력
        
        #User.search_User_ByPhone(phone) # 2. 연락처로 회원조회 ->  선택하는 과정 추가 ( 원하는 전화번호 선택)-> gui?
        #user=User.search_list[phone,1]
        #User.get_User_info(user) # 해당 회원의 정보 출력
        
    #def get_user_show(): # 회원 조회 시 회원을 선택했을 때 book show 클래스를 불러오는 메소드 -> 새창을 띄우는것 gui
      
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 조회")
    title.grid(row=0, column=1, padx=100)

    label_user_name = Label(panedwindow1, text="이름 : ")
    label_user_name.grid(row=1, column=0, padx=100)
    text_user_name = Entry(panedwindow1)
    text_user_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    label_phone = Label(panedwindow1, text="연락처 : ")
    label_phone.grid(row=2, column=0, padx=100)
    text_phone = Entry(panedwindow1)
    text_phone.grid(row=2, column=1, padx=100)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check", "t_check_for_exit"],
                                    displaycolumns=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check", "t_check_for_exit"])
    treeview.grid(row=3, column=1)

    treeview.column("t_name", width=100, anchor="center")
    treeview.heading("t_name", text="이름", anchor="center")

    treeview.column("t_birth", width=50, anchor="center")
    treeview.heading("t_birth", text="생년월일", anchor="center")

    treeview.column("t_hp", width=50, anchor="center")
    treeview.heading("t_hp", text="전화번호", anchor="center")

    treeview.column("t_gender", width=50, anchor="center")
    treeview.heading("t_gender", text="성별", anchor="center")

    treeview.column("t_email", width=50, anchor="center")
    treeview.heading("t_email", text="메일", anchor="center")

    treeview.column("t_check", width=50, anchor="center")
    treeview.heading("t_check", text="대출여부", anchor="center")

    treeview.column("t_check_for_exit", width=50, anchor="center")
    treeview.heading("t_check_for_exit", text="탈퇴여부", anchor="center")

    treeview["show"] = "headings"

    treeValueList = [("손다연", "2000.11.07", "010-1234-5678", "여", "123@naver.com", "도서 대출 중", "X")]

    for i in range(len(treeValueList)):
        treeview.insert("", "end", text="", values=treeValueList[i], iid=i)
        treeview.bind("<Double-1>", onDetailViewForMemeber)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=100)

def User_Show(event):
    global new
    
    #def print_user_info(ind): # 조회한 회원의 정보 출력을 위한 메소드
        #US.get_User_info(ind)
        #print(US.book[ind,1]) # 폰번호 출력
        #print(US.book[ind,2]) # 이름 출력
        #print(US.book[ind,3]) # 생년월일 출력
        #print(US.book[ind,4]) # 성별 출력
        #print(US.book[ind,5]) # 메일 출력
        # 사진 찾기
        #print(US.book[ind,6]) # 대출여부 출력
        #print(US.book[ind,7]) # 탈퇴여부 출력

    def modify_user(): # 수정 버튼을 눌렀을 때 원래 회원 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        modify_user_list=np.array([])

        if textName.get()=='' or textBirth.get()=='' or textGender.get()=='' or textEmail.get()=='': # 이름,생년월일,성별,이메일 넷중 하나를 입력하지 않았을경우 경고메세지 
            #and 말고 or
            textWrite=""
            if textName.get()=='':
                textWrite+="회원명이 입력되어있지 않습니다.\n" # 팝업창 처리
            elif textBirth.get()=='':
                textWrite+="생년월일이 입력되어있지 않습니다.\n" # 팝업창 처리
            elif textGender.get()=='':
                textWrite+="성별이 입력되어있지 않습니다.\n" # 팝업창 처리
            elif textEmail.get()=='':
                textWrite+="이메일이 입력되어있지 않습니다.\n"
            textWrite+="필수사항을 입력해주세요."
            messagebox.showinfo("경고",textWrite)
            return 0

        d=dt.datetime.now().strftime('%Y-%m-%d')
        #가입일자를 다시 읽어올 필요는 없습니다
        modify_user_list=np.append(textName.get())
        modify_user_list=np.append(textBirth.get())
        modify_user_list=np.append(textHP.get())
        modify_user_list=np.append(textGender.get())
        modify_user_list=np.append(textEmail.get())
        #modify_user_list=np.append(textUrl.get())
        modify_user_list=np.append(np.nan)#가입일 그대로 가져올 것, 우선은 공백처리
        modify_user_list=np.append(np.nan)#탈퇴한 회원은 수정하지 않는다는 전제조건 하에 작업
        US.set_User_Info(modify_user_list)
        messagebox.showinfo("알림","도서 수정이 완료되었습니다.")# 팝업창
        
    def delete_user(): # 삭제 버튼을 눌렀을 때 해당 회원 정보가 원래의 회원 리스트에서 삭제되어 회원 리스트에 저장하기 위한 메소드
        phone=textHP.get()
        if US.get_IsRented(phone)!=0: # 사용자가 도서 대출 중일 때 #US.get_IsRented(ind) 쓰시면 됩니다. 리턴 값은 대출 중인 책 권수(int형)
            messagebox.showinfo("경고","도서 대출 중인 회원은 탈퇴할 수 없습니다.")
        else:
            d=dt.datetime.now() # 반납 예정일 저장
            US.drop_User_Info(phone,d) # 회원탈퇴 메소드 호출
            messagebox.showinfo("알림","회원탈퇴가 완료되었습니다.")

    def get_user(name,phone): # 회원 정보를 불러오는 메소드
        #User.search_User_ByName(name) # 이름으로 회원 조회했을시
        #User.search_User_ByPhone(phone) # 연락처로 회원 조회했을시

    new = Toplevel()
    labelName = Label(new, text="이름 : ")
    labelName.grid(row=1, column=0, padx=100)

    textName = Entry(new)
    textName.grid(row=1, column=1, padx=100)

    labelBirth = Label(new, text="생년월일 : ")
    textBirth = Entry(new)
    labelBirth.grid(row=2, column=0, padx=100)
    textBirth.grid(row=2, column=1, padx=100)

    labelHP = Label(new, text="전화번호 : ")
    textHP = Entry(new)
    labelHP.grid(row=3, column=0, padx=100)
    textHP.grid(row=3, column=1, padx=100)

    labelGender = Label(new, text="성별 : ")
    textGender = Entry(new)
    labelGender.grid(row=4, column=0, padx=100)
    textGender.grid(row=4, column=1, padx=100)

    labelEmail = Label(new, text="이메일: ")
    textEmail = Entry(new)
    labelEmail.grid(row=5, column=0, padx=100)
    textEmail.grid(row=5, column=1, padx=100)

    labelPicture = Label(new, text="사진 : ") 
    textPicture = Entry(new)
    labelPicture.grid(row=6, column=0, padx=100)
    textPicture.grid(row=6, column=1, padx=100)

    labelRent = Label(new, text="대출여부 : ")
    textRent = Entry(new)
    labelRent.grid(row=7, column=0, padx=100)
    textRent.grid(row=7, column=1, padx=100)

    labelExit = Label(new, text="탈퇴여부 : ")
    textExit = Entry(new)
    labelExit.grid(row=8, column=0, padx=100)
    textExit.grid(row=8, column=1, padx=100)

    btn_check_dup = Button(new, text="수정",command=modify_user)
    btn_check_dup.grid(row=9, column=0, padx=100)

    btn_check_dup = Button(new, text="등록")
    btn_check_dup.grid(row=9, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=9, column=2, padx=100)


#책 대여하기
def Rent_User_Search():
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    def print_rent_user(ind): # 이름 검색을 누를시에 회원 리스트와 대출여부가 출력되게 하는 메소드
        #User_Search에서 했던 것처럼 -> user_search에서 ?
        
        #US.get_User_info(ind) # 해당 이름의 회원들 정보 불러오는 메소드
        #for i in US.get_User_info(ind): # 해당 이름의 회원들의 정보를 출력
            #print(US.book[ind,2],axis='\t') # 이름 출력
            #print(US.book[ind,3],axis='\t') # 생년월일 출력
            #print(US.book[ind,4],axis='\t') # 성별 출력
            #print(US.book[ind,5],axis='\t') # 메일 출력
            #print(US.book[ind,7],axis='\t') # 탈퇴여부 출력
            #print("%d권 대출 중",user_list[ind,8],axis='\n') # 대출여부 출력
        
    def update_rent_situation(ind,isbn,phone,dat): # 선택 버튼을 눌렀을 시에 해당 회원의 대출 여부가 도서 대출 중으로 바뀌어 저장하는 메소드
        if US.get_IsRented(phone)==3:#US.user_list[ind,8]==3: # 대출 진행 불가능 -> 해당 회원이 3권을 빌린 상태인지를 먼저 체크해야 함#US.get_IsRented(ind)로 불러오시면 
            messagebox.showinfo("경고","대출할 수 있는 최대 권수는 3권입니다.")
        
        #US.user_list[ind,8]+=1 # 대출 권수 1추가 
        #RE.rent_Book(isbn,phone,dat) # 대출 여부

    #def get_rent_book_search(): # book search 클래스 페이지로 넘어가는 메소드
        #gui

    title = Label(panedwindow1, text="도서 대여 - 회원 선택")
    title.grid(row=0, column=1, padx=100)

    label_user_name = Label(panedwindow1, text="이름 : ")
    label_user_name.grid(row=1, column=0, padx=100)
    text_user_name = Entry(panedwindow1)
    text_user_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    label_phone = Label(panedwindow1, text="연락처 : ")
    label_phone.grid(row=2, column=0, padx=100)
    text_phone = Entry(panedwindow1)
    text_phone.grid(row=2, column=1, padx=100)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check"],
                                    displaycolumns=["t_name", "t_birth", "t_hp", "t_gender", "t_email", "t_check"])
    treeview.grid(row=3, column=1)

    treeview.column("t_name", width=100, anchor="center")
    treeview.heading("t_name", text="이름", anchor="center")

    treeview.column("t_birth", width=50, anchor="center")
    treeview.heading("t_birth", text="생년월일", anchor="center")

    treeview.column("t_hp", width=50, anchor="center")
    treeview.heading("t_hp", text="전화번호", anchor="center")

    treeview.column("t_gender", width=50, anchor="center")
    treeview.heading("t_gender", text="성별", anchor="center")

    treeview.column("t_email", width=50, anchor="center")
    treeview.heading("t_email", text="이메일", anchor="center")

    treeview.column("t_check", width=50, anchor="center")
    treeview.heading("t_check", text="대출상태", anchor="center")

    treeview["show"] = "headings"

    treeValueList = [("손다연", "2000.11.07", "010-1234-5678", "여", "123@naver.com", "3권 대출 중")]

    for i in range(len(treeValueList)):
        treeview.insert("", "end", text="", values=treeValueList[i], iid=i)
        treeview.bind("<Double-1>", onDetailViewForMemeber)

    btn_cancel = Button(panedwindow1, text="선택", command=lambda: rentBookForDetail(panedwindow1))
    btn_cancel.grid(row=4, column=0, padx=100)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=100)

def Rent_Book_Search(before):
    def check_book_rent(title): # 도서 정보를 검색시에 해당 도서의 대출 여부 정보를 불러오는 메소드
        #Book_Search에서 도서명으로 검색했던 것처럼
        #BO.search_Book_ByTitle(title)
        #book_list[ind,8] # 해당 도서의 대출 여부 정보 

    def update_rent_situation(ind): # 선택 버튼을 눌렀을 시에 대출 상태가 대출중으로 바뀌어 저장되게하고, 대출 정보 화면을 띄어주게 하는 메소드
        if BO.get_IsRented(ind):#BO.get_IsRented(ind)
            messagebox.showinfo("경고","이미 대출 중인 도서입니다.")
        else:
            #book_list[ind,8]==TRUE
            
        #rent_show 클래스를 불러와야 함 ( 대출 정보 화면 띄워주기 ) -> gui

    def get_book(ind): # 도서 정보를 불러오는 메소드
        #BO.get_Book_info(ind)
    before.pack_forget()

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 대여 - 도서 선택")
    title.grid(row=0, column=1, padx=100)

    label_member_name = Label(panedwindow1, text="도서 선택 : ") 
    label_member_name.grid(row=1, column=0, padx=100)
    text_member_name = Entry(panedwindow1)
    text_member_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"])
    treeview.grid(row=2, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center")

    treeview.column("t_isbn", width=50, anchor="center")
    treeview.heading("t_isbn", text="ISBN", anchor="center")

    treeview.column("t_title", width=50, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=50, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=50, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=50, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=50, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")

    treeview["show"] = "headings"

    treeValueList = [("대출중", 9788970504773, "따라하며 배우는 파이썬과 데이터 과학", "천인국", "생능출판", 26000, "https://~"),
                     (" X ", 1234970504773, "예제 중심의 파이썬 입문", "황재호", "생능출판", 26000, "https://~")]

    for i in range(len(treeValueList)):
        treeview.insert("", "end", text="", values=treeValueList[i], iid=i)
        treeview.bind("<Double-1>", onWantRentBookView)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=3, column=1, padx=100)


def Rent_Show(event):
    global new

    def save_rent(SEQ,ISBN,PHONE,DATE,RETURN_DATE,RETURN_YN): # 대출 완료 버튼을 눌렀을 시에 대출 정보를 저장하는 메소드 -> gui (버튼작용)
        #Rent.save_to_csv(SEQ,ISBN,PHONE,DATE,RETURN_DATE,RETURN_YN) 

    def get_rent_book_info(ind): # 대출할 도서의 정보를 불러오는 메소드
        #BO.get_Book_info(ind)

    def get_rent_user_info(ind): # 대출할 회원의 정보를 불러오는 메소드
        #US.get_User_info(ind)

    def set_return_date(ind): # 반납 날짜를 지정하는 메소드
        #date=rent_list[ind,4]
        #date=datetime.strptime(date,'%Y.%m.%d')
        #date=date+timedelta(days=14)
        #rent_list[ind,4]=date

    new = Toplevel()

    labelTitle = Label(new, text="대출 정보")
    labelTitle.grid(row=0, column=0, padx=100)

    labelBookInfo = Label(new, text="도서 정보")
    labelBookInfo.grid(row=1, column=0, padx=100)

    labelMemboerInfo = Label(new, text="회원 정보")
    labelMemboerInfo.grid(row=1, column=2, padx=100)

    labelBookName = Label(new, text="도서명 : ")
    textBookName = Entry(new)
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)
    labelName = Label(new, text="이름 : ")
    textName = Entry(new)
    labelName.grid(row=2, column=2, padx=100)
    textName.grid(row=2, column=3, padx=100)

    labelAuthor = Label(new, text="저자 : ")
    textAuthor = Entry(new)
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)
    labelBirth = Label(new, text="생년월일 : ")
    textBirth = Entry(new)
    labelBirth.grid(row=3, column=2, padx=100)
    textBirth.grid(row=3, column=3, padx=100)

    labelPub = Label(new, text="출판사 : ")
    textPub = Entry(new)
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)
    labelGender = Label(new, text="성별 : ")
    textGender = Entry(new)
    labelGender.grid(row=4, column=2, padx=100)
    textGender.grid(row=4, column=3, padx=100)

    labelPrice = Label(new, text="가격 : ")
    textPrice = Entry(new)
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)
    labelEmail = Label(new, text="이메일 : ")
    textEmail = Entry(new)
    labelEmail.grid(row=5, column=2, padx=100)
    textEmail.grid(row=5, column=3, padx=100)

    labelUrl = Label(new, text="관련URL : ")
    textUrl = Entry(new)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)
    labelRentDay = Label(new, text="대여일 : ")
    textRentDay = Entry(new)
    labelRentDay.grid(row=6, column=2, padx=100)
    textRentDay.grid(row=6, column=3, padx=100)

    labelISBN = Label(new, text="ISBN : ")
    labelISBN.grid(row=7, column=0, padx=100)
    textISBN = Entry(new)
    textISBN.grid(row=7, column=1, padx=100)
    labelBackDay = Label(new, text="반납 예정일 : ")
    textBackDay = Entry(new)
    labelBackDay.grid(row=7, column=2, padx=100)
    textBackDay.grid(row=7, column=3, padx=100)

    labelBackCheck = Label(new, text="반납 여부 : ")
    textBackCheck = Entry(new)
    labelBackCheck.grid(row=8, column=2, padx=100)
    textBackCheck.grid(row=8, column=3, padx=100)

    btn_check_dup = Button(new, text="대여하기")
    btn_check_dup.grid(row=9, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=9, column=2, padx=100)


# 대여 책 조회
def Rent_Search():
    
    def get_rent(): # 대출 정보를 불러오는 메소드 --> 도서정보,회원정보를 불러오는것?
        #Book.search_Book_ByTitle(title) # 1. 도서명으로 검색
        #isbn=Book.search_list[title,1] # 결과값에서 isbn을 추출함
        #Rent.search_Rent_ByBook(isbn) # 해당 isbn으로 대출조회

        #User.search_User_ByName(name) # 2. 회원명으로 검색
        #phone=User.search_list[name,1] # 결과값에서 전화번호를 추출
        #Rent.search_Rent_ByUser(phone) # 해당 전화번호로 대출조회
        
    #def get_rent_state_show(): # 대출 조회 시, 확인을 원하는 대출 내역을 선택했을 때 get_rent_state_show() 클래스를 불러오는 메소드-> gui

    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="대출 조회")
    title.grid(row=0, column=1, padx=100)

    label_book_name = Label(panedwindow1, text="도서명 : ")
    label_book_name.grid(row=1, column=0, padx=100)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    label_member = Label(panedwindow1, text="회원명 : ")
    label_member.grid(row=2, column=0, padx=100)
    text_member = Entry(panedwindow1)
    text_member.grid(row=2, column=1, padx=100)


    treeview = tkinter.ttk.Treeview(panedwindow1,
                                    column=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"],
                                    displaycolumns=["t_check", "t_isbn", "t_title", "t_author", "t_pub", "t_price", "t_url"])
    treeview.grid(row=3, column=1)

    treeview.column("t_check", width=100, anchor="center")
    treeview.heading("t_check", text="대출 여부", anchor="center")

    treeview.column("t_isbn", width=50, anchor="center")
    treeview.heading("t_isbn", text="ISBN", anchor="center")

    treeview.column("t_title", width=50, anchor="center")
    treeview.heading("t_title", text="제목", anchor="center")

    treeview.column("t_author", width=50, anchor="center")
    treeview.heading("t_author", text="저자", anchor="center")

    treeview.column("t_pub", width=50, anchor="center")
    treeview.heading("t_pub", text="출판사", anchor="center")

    treeview.column("t_price", width=50, anchor="center")
    treeview.heading("t_price", text="가격", anchor="center")

    treeview.column("t_url", width=50, anchor="center")
    treeview.heading("t_url", text="관련URL", anchor="center")

    treeview["show"] = "headings"

    treeValueList = [("대출중", 9788970504773, "따라하며 배우는 파이썬과 데이터 과학", "천인국", "생능출판", 26000, "https://~"),
                     (" X ", 1234970504773, "예제 중심의 파이썬 입문", "황재호", "생능출판", 26000, "https://~")]

    for i in range(len(treeValueList)):
        treeview.insert("", "end", text="", values=treeValueList[i], iid=i)
        treeview.bind("<Double-1>", onSearchRentBookInfoView)

    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=4, column=1, padx=100)


def Rent_State_Show(event):
    global new
    
    def book_return(ind): # 도서 반납 메소드
        #Rent.back_Book(ind)

    def get_rent_book_info(ind): # 대출된 도서의 정보를 불러오는 메소드
        #Rent 인터페이스에서 불러온 정보에서 ISBN을 불러와서 Book 인터페이스에서 재검색하는 식으로 해야되는 해당 인터페이스 추가
        #Rent.getRentInfo(ind)

    def get_rent_user_info(): # 대출을 실행한 회원의 정보를 불러오는 메소드 -> 해당 책을 빌린 사람의 정보
        #user= #도서대출 저장하는 메소드에서 회원이름을 뽑아옴
        #User.get_User_info(user)

    #def get_rent_info(): # 상단 대출 정보를 표시하는 메소드 -> gui

    new = Toplevel()

    labelTitle = Label(new, text="대출 정보")
    labelTitle.grid(row=0, column=0, padx=100)

    labelBookInfo = Label(new, text="도서 정보")
    labelBookInfo.grid(row=1, column=0, padx=100)

    labelMemboerInfo = Label(new, text="회원 정보")
    labelMemboerInfo.grid(row=1, column=2, padx=100)

    labelBookName = Label(new, text="도서명 : ")
    textBookName = Entry(new)
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)
    labelName = Label(new, text="이름 : ")
    textName = Entry(new)
    labelName.grid(row=2, column=2, padx=100)
    textName.grid(row=2, column=3, padx=100)

    labelAuthor = Label(new, text="저자 : ")
    textAuthor = Entry(new)
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)
    labelBirth = Label(new, text="생년월일 : ")
    textBirth = Entry(new)
    labelBirth.grid(row=3, column=2, padx=100)
    textBirth.grid(row=3, column=3, padx=100)

    labelPub = Label(new, text="출판사 : ")
    textPub = Entry(new)
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)
    labelGender = Label(new, text="성별 : ")
    textGender = Entry(new)
    labelGender.grid(row=4, column=2, padx=100)
    textGender.grid(row=4, column=3, padx=100)

    labelPrice = Label(new, text="가격 : ")
    textPrice = Entry(new)
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)
    labelEmail = Label(new, text="이메일 : ")
    textEmail = Entry(new)
    labelEmail.grid(row=5, column=2, padx=100)
    textEmail.grid(row=5, column=3, padx=100)

    labelUrl = Label(new, text="관련URL : ")
    textUrl = Entry(new)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)
    labelRentDay = Label(new, text="대여일 : ")
    textRentDay = Entry(new)
    labelRentDay.grid(row=6, column=2, padx=100)
    textRentDay.grid(row=6, column=3, padx=100)

    labelISBN = Label(new, text="ISBN : ")
    labelISBN.grid(row=7, column=0, padx=100)
    textISBN = Entry(new)
    textISBN.grid(row=7, column=1, padx=100)
    labelBackDay = Label(new, text="반납 예정일 : ")
    textBackDay = Entry(new)
    labelBackDay.grid(row=7, column=2, padx=100)
    textBackDay.grid(row=7, column=3, padx=100)

    labelBackCheck = Label(new, text="반납 여부 : ")
    textBackCheck = Entry(new)
    labelBackCheck.grid(row=8, column=2, padx=100)
    textBackCheck.grid(row=8, column=3, padx=100)

    btn_check_dup = Button(new, text="반납하기", command=book_return)
    btn_check_dup.grid(row=9, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=9, column=2, padx=100)




# Add image file
bg = PhotoImage(file="background.png")

# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)


my_frame = Frame(root)
my_frame.pack(pady=100)

my_button1 = Button(my_frame, text="도서 관리")
my_button1.grid(row=0, column=0, padx=100)
my_button1 = Button(my_frame, text="도서 등록", command=Book_Add)
my_button1.grid(row=1, column=0, padx=100)
my_button1 = Button(my_frame, text="도서 조회 수정 삭제", command=Book_Search)
my_button1.grid(row=2, column=0, padx=100)

my_button1 = Button(my_frame, text="회원 관리")
my_button1.grid(row=0, column=1, padx=100)
my_button1 = Button(my_frame, text="회원 등록", command=User_Add)
my_button1.grid(row=1, column=1, padx=100)
my_button1 = Button(my_frame, text="회원 조회 수정 탈퇴", command=User_Search)
# , command=viewMemeber)
my_button1.grid(row=2, column=1, padx=100)

my_button1 = Button(my_frame, text="도서 대여")
my_button1.grid(row=0, column=2, padx=100)
my_button1 = Button(my_frame, text="도서 대여", command=Rent_User_Search)
my_button1.grid(row=1, column=2, padx=100)
my_button1 = Button(my_frame, text="대출 조회 반납" , command=searchRentBookInfo)
my_button1.grid(row=2, column=2, padx=100)

# Execute tkinter
root.mainloop()
