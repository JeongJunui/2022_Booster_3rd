import pandas as pd
import numpy as np
from tkinter import *
import tkinter.ttk
from tkinter import messagebox

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

class Book:
    
    def __init__(self,book): #생성자
        self.__book=book; #self.__ : private
    def get_Isbnlist(self): #접근자
        return self.__book[:0]
    
    def get_IsIn(self,isbn): # isbn이 안에 있는가 확인 (IF-001)
        if isbn in self.__book[:,0]: # 있으면 True 반환
            return True
        else:
            return False
    
    def add_Book_Info(self,inf): # 도서 등록 (IF-002)
        self.__book=np.append(self.__book,inf,asix=0)# 행 방향으로 정보 추가
        
    def get_Book_info(self,ind): # 책 정보 확인
        return self.__book[ind,:]# 인덱스에 해당하는 책 정보를 리턴

    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        search_list=np.array([])

        for s in len(str(title)): # 검색된 문자열을 문자열 길이만큼 반복문으로 돌림
            title+=s # 반복하며 문자열이 추가 됨
            if book_list.at(title): # 만약 반복하다가 같은 문자열이 발견된다면 문자열에 저장
                search_list=np.append(search_list,title)
        return search_list; # 비슷한 문자열을 가진 도서목록을 출력해줌 

        """
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__book[:1]:
            if title==i:
                search_list=np.append(search_list,self.__book[j,:])# 제목이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 도서 목록
        """
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def search_Book_ByAuthor(self,author): # 책 저자로 검색 (IF-004)
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__book[:2]:
            if author==i:
                search_list=np.append(search_list,self.__book[j,:])# 저자가 동일하면 리스트에 추가
            j+=1
            
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 도서 목록
    
    def set_Book_Info(self,ind,inf): # 도서 수정 (IF-005)
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 책 정보 삽입
   
    def drop_Book_Info(self,ind): # 도서 삭제 (IF-006)
        self.__book=np.delete(self.__book,ind)# 인덱스 값에 해당하는 정보 삭제
        
class User:

    def __init__(self,user): #생성자
        self.__user=user #__ : private
    def get_Phonelist(self): #접근자
        return self.__user[:0]
    
    def get_IsIn(self,phone): # 폰번호가 안에 있는가 확인 (IF-007)
        if phone in self.__user[:,0]: # 있으면 True 반환
            return True
        else:
            return False
        
    def get_User_info(self,ind): # 회원 정보 확인 (IF-008)  ---->>>> ????? 이건 무엇
        return self.__user[ind,:]# 인덱스에 해당하는 책 정보 리턴

    def add_User_Info(self,inf): # 회원 등록 (IF-008)
        self.__user=np.append(self.__book,inf,axis=0) # 행 방향으로 정보 추가
    
    def search_User_ByName(self,name): # 이름으로 회원 조회 (IF-009)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__user[:2]:
            if title==i:
                search_list=np.append(search_list,self.__user[j,:])# 이름이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list# 반환 값 : 회원 목록

    def search_User_ByPhone(self,phone): # 연락처로 회원 조회 (IF-010)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__user[:1]:
            if title==i:
                search_list=np.append(search_list,self.__user[j,:])# 연락처가 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list# 반환 값 : 회원 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def set_User_Info(self,ind,inf): # 회원 수정 (IF-011)
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 회원 정보 삽입

    def drop_User_Info(self,ind,dat): # 회원 탈퇴 (IF-012)
        self.__user[ind,6]=dat# 인덱스 값에 해당하는 회원 탈퇴일자 저장
        # 회원 탈퇴 시 재가입을 할 수도 있는경우를 위해회원을 삭제 하는 것이 아니라 탈퇴 날짜를 지정해줌

class Rent:
    def __init__(self,rent): # 생성자
        self.__rent=rent
        
    def rent_Book(self,isbn,phone,dat): # 도서대출  (IF-013)
        add_info=np.array([int(self.__rent.size/6),isbn,phone,dat,dat+timedelta(days=14),False])# 대출 정보를 numpy 형태로 변환
        # 날짜 형식 계산은 나중에 추가할 예정
        self.__rent=np.append(self.__rent,add_info,axis=0)# 대출 목록에 추가
        
    def search_Rent_ByBook(self,isbn): # ISBN으로 대출 조회 (IF-014)
        search_list=np.array([])# 검색된 대출 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__rent[:,1]:
            if isbn==i:
                search_list=np.append(search_list,self.__rent[j,:])# ISBN이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/6),6))
        return search_list# 반환 값 : 대출 목록

    def search_Rent_ByUser(self, phone): # 연락처로 대출 조회 (IF-015)
        search_list=np.array([])# 검색된 대출 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__rent[:,2]:
            if phone==i:
                search_list=np.append(search_list,self.__rent[j,:])# 연락처가 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/6),6))
        return search_list# 반환 값 : 대출 목록
        
    def back_Book(self,ind):# 도서 반납 (IF-016)
        self.__rent[ind,5]=True# 인덱스 값에 해당하는 대출 반납처리

Bk=Book(book_list)
Ur=User(user_list)
Rt=Rent(rent_list)

# Create object
root = Tk()

# Adjust size
root.geometry("1454x936")
root.resizable(0, 0)



# 버튼 클릭 이벤트 핸들러
def Book_Add():

    confirmedISBN=" "
    isConfirmed=False
    def get_user(): # ISBN 중복 확인을 위해 도서 리스트를 불러오는 위한 메소드
        if Bk.get_IsIn("""textISBN에서 문자열 불러와서 집어넣기"""): 
            print(" 이미 등록된 도서입니다.")
            isConfirmed=True
            confirmedISBN="""textISBN에서 불러온 문자열"""
        else:
            print("등록 가능한 도서입니다.")

    def add_book():
        #
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 등록")
    title.grid(row=0, column=1, padx=100)

    labelISBN = Label(panedwindow1, text="ISBN : ")
    labelISBN.grid(row=1, column=0, padx=100)
    textISBN = Entry(panedwindow1)
    textISBN.grid(row=1, column=1, padx=100)
    btn_check_dup = Button(panedwindow1, text="등록")
    btn_check_dup.grid(row=1, column=2, padx=100)

    labelBookName = Label(panedwindow1, text="도서명 : ")
    textBookName = Entry(panedwindow1)
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)

    labelAuthor = Label(panedwindow1, text="저자 : ")
    textAuthor = Entry(panedwindow1)
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)


    labelPub = Label(panedwindow1, text="출판사 : ")
    textPub = Entry(panedwindow1)
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)

    labelPrice = Label(panedwindow1, text="가격 : ")
    textPrice = Entry(panedwindow1)
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)


    labelUrl = Label(panedwindow1, text="관련URL : ")
    textUrl = Entry(panedwindow1)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)

    labelDesc = Label(panedwindow1, text="도서설명 : ")
    textDesc = Entry(panedwindow1)
    labelDesc.grid(row=7, column=0, padx=100)
    textDesc.grid(row=7, column=1, padx=100)

    btn_book_register = Button(panedwindow1, text="등록")
    btn_book_register.grid(row=8, column=0, padx=100)
    # command=lambda: panedwindow1.pack_forget() -> 현재 panedwindow1 창을 닫음.
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=8, column=1, padx=100)

    # pw = Label(root, text="asdasdasdd", width=160, height=40)
    # pw.place(x=200, y=200)

    # frame1 = Frame(root, relief="solid", bd=2)
    # frame1.pack(side="left", fill="both", expand=True)


# 도서 조회
def Book_Search():

    def get_book_show(): # 도서 조회시 도서를 선택했을 때 book show 클래스를 불러오는 메소드 -> gui?
        book_show.print_book_info() # 조회한 책의 정보를 출력하는 메소드

    def print_book_list(): # 도서 조회시 관련 도서의 리스트를 화면에 출력해주는 메소드
        BS=Book(book_list)
        
        if book_textbox.get(): # 도서명이 입력된 경우
            print(BS.search_Book_ByTitle()) # 제목으로 도서 검색하는 함수 호출
        elif author_textbox.get(): # 저자명이 입력된 경우
            print(BS.search_Book_ByAuthor()) # 책 저자로 검색하는 함수 호출
    def get_book(): # 도서 정보를 불러오는 메소드
        #print(BS.get_Book_info()) # 책 정보 확인 ( 도서 정보 리스트 출력 )
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="도서 조회")
    title.grid(row=0, column=1, padx=100)

    label_book_name = Label(panedwindow1, text="도서명 : ")
    label_book_name.grid(row=1, column=0, padx=100)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
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
    
    def print_book_info(): # 조회한 책의 정보 출력을 위한 메소드
        Bk.get_Book_info() # 책 정보 확인 함수 호출

    def modify_book(): # 수정 버튼을 눌렀을 때 원래 도서 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        Bk.set_Book_Info() # 도서 수정 함수 호출

    def delete_book(): # 삭제 버튼을 눌렀을 때 해당된 도서 정보가 원래의 도서 리스트에서 삭제되어 도서 리스트에 저장 하기 위한 메소드
        Bk.drop_Book_Info()  # 도서 삭제 함수 호출

    def get_book(): # 도서 정보를 불러오는 메소드
        #print(BS)
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
    
    labelUrl = Label(new, text="대출여부 : ")
    textUrl = Entry(new)
    labelUrl.grid(row=7, column=0, padx=100)
    textUrl.grid(row=7, column=1, padx=100)

    btn_check_dup = Button(new, text="수정")
    btn_check_dup.grid(row=8, column=0, padx=100)

    btn_check_dup = Button(new, text="등록")
    btn_check_dup.grid(row=8, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=8, column=2, padx=100)




# 회원 등록 페이지
def User_Add():
    confirmedHP="010-0000-0000"
    isConfirmed=False
    def check_user(): # 회원 중복 확인을 위한 메소드
        if US.get_IsIn("""textHP에서 문자열 받아오기"""):
            useradd_msgbox.showinfo(text="이미 등록된 회원입니다.")
            isConfirmed=True
            confirmedHP="""textHP에서 받아온 문자열"""
        else:
            useradd_msgbox.showinfo(text="등록 가능한 회원입니다.")
    
    def add_user(inf): # 등록 버튼을 누를시에 이름, 생년월일, 전화번호, 성별, 이메일, 사진의 정보를 받아 원래 회원 리스트에 추가해주는 메소드
        US.add_User_Info(inf)

    # def search_photo(): # PC에서 사용자 사진을 찾도록 하는 메소드 --> gui
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 등록")
    title.grid(row=0, column=1, padx=100)

    labelName = Label(panedwindow1, text="이름 : ")
    labelName.grid(row=1, column=0, padx=100)
    textName = Entry(panedwindow1)
    textName.grid(row=1, column=1, padx=100)


    labelBirth = Label(panedwindow1, text="생년월일 : ")
    textBirth = Entry(panedwindow1)
    labelBirth.grid(row=2, column=0, padx=100)
    textBirth.grid(row=2, column=1, padx=100)

    labelHP = Label(panedwindow1, text="전화번호 : ")
    textHP = Entry(panedwindow1)
    labelHP.grid(row=3, column=0, padx=100)
    textHP.grid(row=3, column=1, padx=100)
    btn_check = Button(panedwindow1, text="중복확인", command=check_user)
    btn_check.grid(row=3, column=2, padx=100)


    labelGender = Label(panedwindow1, text="성별 : ")
    textGender = Entry(panedwindow1)
    labelGender.grid(row=4, column=0, padx=100)
    textGender.grid(row=4, column=1, padx=100)

    labelEmail = Label(panedwindow1, text="이메일 : ")
    textEmail = Entry(panedwindow1)
    labelEmail.grid(row=5, column=0, padx=100)
    textEmail.grid(row=5, column=1, padx=100)


    labelUrl = Label(panedwindow1, text="사 진 : ")
    textUrl = Entry(panedwindow1)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)
    btn_check = Button(panedwindow1, text="찾기")
    btn_check.grid(row=6, column=2, padx=100)

    btn_book_register = Button(panedwindow1, text="등록", command=add_user)
    btn_book_register.grid(row=7, column=0, padx=100)
    btn_cancel = Button(panedwindow1, text="취소", command=lambda: panedwindow1.pack_forget())
    btn_cancel.grid(row=7, column=1, padx=100)


#회원 조회
def User_Search():

    def get_user(ind): # 회원 정보를 불러오는 메소드
        US.get_User_info(ind)

    #def get_user_show(): # 회원 조회 시 회원을 선택했을 때 book show 클래스를 불러오는 메소드 -> 새창을 띄우는것 gui?
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    title = Label(panedwindow1, text="회원 조회")
    title.grid(row=0, column=1, padx=100)

    label_book_name = Label(panedwindow1, text="이름 : ")
    label_book_name.grid(row=1, column=0, padx=100)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    label_author = Label(panedwindow1, text="연락처 : ")
    label_author.grid(row=2, column=0, padx=100)
    text_author = Entry(panedwindow1)
    text_author.grid(row=2, column=1, padx=100)

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
    # item = self.tree.selection()[0]
    global new
    
    def print_user_info(ind): # 조회한 회원의 정보 출력을 위한 메소드
        US.get_User_info(ind)
        print(US.book[ind,1]) # 폰번호 출력
        print(US.book[ind,2]) # 이름 출력
        print(US.book[ind,3]) # 생년월일 출력
        print(US.book[ind,4]) # 성별 출력
        print(US.book[ind,5]) # 메일 출력
        # 사진 찾기
        print(US.book[ind,6]) # 대출여부 출력
        print(US.book[ind,7]) # 탈퇴여부 출력

    def modify_user(ind,inf): # 수정 버튼을 눌렀을 때 원래 회원 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        US.set_User_Info(ind,inf)

    def delete_user(ind,dat): # 삭제 버튼을 눌렀을 때 해당 회원 정보가 원래의 회원 리스트에서 삭제되어 회원 리스트에 저장하기 위한 메소드
        US.drop_User_Info(ind,dat)

    def get_user(name,phone): # 회원 정보를 불러오는 메소드
        US.search_User_ByName(name) # 이름으로 회원 조회했을시
        US.search_User_ByPhone(phone) # 연락처로 회원 조회했을시
    new = Toplevel()
    labelISBN = Label(new, text="이름 : ")
    labelISBN.grid(row=1, column=0, padx=100)

    textISBN = Entry(new)
    textISBN.grid(row=1, column=1, padx=100)

    labelBookName = Label(new, text="생년월일 : ")
    textBookName = Entry(new)
    labelBookName.grid(row=2, column=0, padx=100)
    textBookName.grid(row=2, column=1, padx=100)

    labelAuthor = Label(new, text="전화번호 : ")
    textAuthor = Entry(new)
    labelAuthor.grid(row=3, column=0, padx=100)
    textAuthor.grid(row=3, column=1, padx=100)

    labelPub = Label(new, text="성별 : ")
    textPub = Entry(new)
    labelPub.grid(row=4, column=0, padx=100)
    textPub.grid(row=4, column=1, padx=100)

    labelPrice = Label(new, text="이메일: ")
    textPrice = Entry(new)
    labelPrice.grid(row=5, column=0, padx=100)
    textPrice.grid(row=5, column=1, padx=100)

    labelUrl = Label(new, text="사진 : ")
    textUrl = Entry(new)
    labelUrl.grid(row=6, column=0, padx=100)
    textUrl.grid(row=6, column=1, padx=100)

    labelUrl = Label(new, text="대출여부 : ")
    textUrl = Entry(new)
    labelUrl.grid(row=7, column=0, padx=100)
    textUrl.grid(row=7, column=1, padx=100)

    labelUrl = Label(new, text="탈퇴여부 : ")
    textUrl = Entry(new)
    labelUrl.grid(row=8, column=0, padx=100)
    textUrl.grid(row=8, column=1, padx=100)

    btn_check_dup = Button(new, text="수정")
    btn_check_dup.grid(row=9, column=0, padx=100)

    btn_check_dup = Button(new, text="등록")
    btn_check_dup.grid(row=9, column=1, padx=100)

    btn_check_dup = Button(new, text="취소", command=lambda: new.destroy())
    btn_check_dup.grid(row=9, column=2, padx=100)


#책 대여하기
def Rent_User_Search():
    panedwindow1 = PanedWindow(relief="raised", bd=2)
    panedwindow1.pack(expand=True)

    # 먼저 회원을 선택해야함.

    def print_rent_user(ind): # 이름 검색을 누를시에 회원 리스트와 대출여부가 출력되게 하는 메소드
        US.get_User_info(ind) # 해당 이름의 회원들 정보 불러오는 메소드
        for i in US.get_User_info(ind): # 해당 이름의 회원들의 정보를 출력
            print(US.book[ind,2],axis='\t') # 이름 출력
            print(US.book[ind,3],axis='\t') # 생년월일 출력
            print(US.book[ind,4],axis='\t') # 성별 출력
            print(US.book[ind,5],axis='\t') # 메일 출력
            print(US.book[ind,7],axis='\t') # 탈퇴여부 출력
            print("%d권 대출 중",user_list[ind,8],axis='\n') # 대출여부 출력
        
    def update_rent_situation(ind,isbn,phone,dat): # 선택 버튼을 눌렀을 시에 해당 회원의 대출 여부가 도서 대출 중으로 바뀌어 저장하는 메소드
        US.user_list[ind,8]+=1 # 대출 권수 1추가 
        RE.rent_Book(isbn,phone,dat) # 대출 여부

        if US.user_list[ind,8]==3: # 대출 진행 불가능
            print("대출할 수 있는 최대 권수를 3권입니다.") 

    #def get_rent_book_search(): # book search 클래스 페이지로 넘어가는 메소드

    title = Label(panedwindow1, text="도서 대여 - 회원 선택")
    title.grid(row=0, column=1, padx=100)

    label_book_name = Label(panedwindow1, text="이름 : ")
    label_book_name.grid(row=1, column=0, padx=100)
    text_book_name = Entry(panedwindow1)
    text_book_name.grid(row=1, column=1, padx=100)
    btn_view = Button(panedwindow1, text="조회")
    btn_view.grid(row=1, column=2, padx=100)

    label_author = Label(panedwindow1, text="연락처 : ")
    label_author.grid(row=2, column=0, padx=100)
    text_author = Entry(panedwindow1)
    text_author.grid(row=2, column=1, padx=100)

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
    # 이전 창을 닫습니다.
    def check_book_rent(title): # 도서 정보를 검색시에 해당 도서의 대출 여부 정보를 불러오는 메소드
        BO.search_Book_ByTitle(title)
        book_list[ind,8] # 해당 도서의 대출 여부 정보 

    def update_rent_situation(ind): # 선택 버튼을 눌렀을 시에 대출 상태가 대출중으로 바뀌어 저장되게하고, 대출 정보 화면을 띄어주게 하는 메소드
        if book_list[ind,8]==TRUE:
            print("이미 대출 중인 도서입니다.")
        else:
            book_list[ind,8]==TRUE
            

        # rent_show 클래스를 불러와야 함 ( 대출 정보 화면 띄워주기 )

    def get_book(ind): # 도서 정보를 불러오는 메소드
        BO.get_Book_info(ind) # 해당하는 책을 불러와야 되는지? 아니면 
    before.pack_forget();

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
    # item = self.tree.selection()[0]
    global new

    def save_rent(ind): # 대출 완료 버튼을 눌렀을 시에 대출 정보를 저장하는 메소드
        rent_book_search.update_rent_situation(ind) 

    def get_rent_book_info(ind): # 대출할 도서의 정보를 불러오는 메소드
        BO.get_Book_info(ind)

    def get_rent_user_info(ind): # 대출할 회원의 정보를 불러오는 메소드
        US.get_User_info(ind)

    def set_return_date(ind): # 반납 날짜를 지정하는 메소드
        date=rent_list[ind,4]
        date=datetime.strptime(date,'%Y.%m.%d')
        date=date+timedelta(days=14)
        rent_list[ind,4]=date
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
    
    def get_rent(isbn,phone,dat): # 대출 정보를 불러오는 메소드 --> 도서정보,회원정보를 불러오는것?
        Book.rent_Book(isbn,phone,dat)
        
    #def get_rent_state_show(): # 대출 조회 시, 확인을 원하는 대출 내역을 선택했을 때 get_rent_state_show() 클래스를 불러오는 메소드
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
    # item = self.tree.selection()[0]
    global new
    
    def book_return(ind): # 도서 반납 메소드
        Book.back_Book(ind)

    def get_rent_book_info(ind): # 대출된 도서의 정보를 불러오는 메소드
        Rent.getRentInfo(ind)

    def get_rent_user_info(ind): # 대출을 실행한 회원의 정보를 불러오는 메소드 -> 해당 책을 빌린 사람의 정보
        User.get_User_info(ind)

    #def get_rent_info(): # 상단 대출 정보를 표시하는 메소드 -> gui ?
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

    btn_check_dup = Button(new, text="반납하기")
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
