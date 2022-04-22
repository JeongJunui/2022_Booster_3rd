import pandas as pd
import numpy as np

df=pd.read_csv('./Rent.csv', encoding='UTF-8') # cvs파일 불러옴
df1=pd.read_csv('./User.csv', encoding='UTF-8')
df2=pd.read_csv('./Book.csv', encoding='UTF-8')

rent_list=np.array([]) # 넘파이 빈리스트 생성
rent_list=np.append(rent_list,df) # 값들을 append를 사용해 추가
rent_list=np.reshape(rent_list,(int(rent_list.size/6),6)) # size행 8열로 모양 변환

user_list=np.array([])
user_list=np.append(user_list,df1)
user_list=np.reshape(user_list,(int(user_list.size/8),8))

book_list=np.array([])
book_list=np.append(book_list,df2)
book_list=np.reshape(book_list,(int(book_list.size/8),8))

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
        return self.__book[ind,:] # 인덱스에 해당하는 책 정보를 리턴

    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        search_list=np.array([])

        for s in len(str(title)): # 검색된 문자열을 문자열 길이만큼 반복문으로 돌림
            title+=s # 반복하며 문자열이 추가 됨
            if book_list.at(title): # 만약 반복하다가 같은 문자열이 발견된다면 문자열에 저장
                search_list=np.append(search_list,title)
                return search_list; # 비슷한 문자열을 가진 도서목록을 출력해줌 

        search_list=np.array([]) # 검색된 책 정보 저장할 리스트
        j=0 # 인덱스 체크용
        for i in self.__book[:1]:
            if title==i:
                search_list=np.append(search_list,self.__book[j,:])# 제목이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 도서 목록
        
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def search_Book_ByAuthor(self,author): # 책 저자로 검색 (IF-004)
        search_list=np.array([]) # 검색된 책 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__book[:2]:
            if author==i:
                search_list=np.append(search_list,self.__book[j,:])# 저자가 동일하면 리스트에 추가
            j+=1
            
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 도서 목록
    
    def set_Book_Info(self,ind,inf): # 도서 수정 (IF-005)
        self.__user[ind,:]=inf # 인덱스 값에 해당하는 책 정보 삽입
   
    def drop_Book_Info(self,ind): # 도서 삭제 (IF-006)
        self.__book=np.delete(self.__book,ind) # 인덱스 값에 해당하는 정보 삭제
        
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
        
    def get_User_info(self,ind): # 회원 정보 확인
        return self.__user[ind,:] # 인덱스에 해당하는 책 정보 리턴

    def add_User_Info(self,inf): # 회원 등록 (IF-008)
        self.__user=np.append(self.__book,inf,axis=0) # 행 방향으로 정보 추가
    
    def search_User_ByName(self,name): # 이름으로 회원 조회 (IF-009)
        search_list=np.array([]) # 검색된 회원 정보 저장할 리스트
        j=0 # 인덱스 체크용
        for i in self.__user[:2]:
            if title==i:
                search_list=np.append(search_list,self.__user[j,:])# 이름이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 회원 목록

    def search_User_ByPhone(self,phone): # 연락처로 회원 조회 (IF-010)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__user[:1]:
            if title==i:
                search_list=np.append(search_list,self.__user[j,:])# 연락처가 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 회원 목록
    # 일부만 일치해도 검색할 수 있게 개선 필요함
    
    def set_User_Info(self,ind,inf): # 회원 수정 (IF-011)
        self.__user[ind,:]=inf # 인덱스 값에 해당하는 회원 정보 삽입

    def drop_User_Info(self,ind,dat): # 회원 탈퇴 (IF-012)
        self.__user[ind,6]=dat # 인덱스 값에 해당하는 회원 탈퇴일자 저장
        # 회원 탈퇴 시 재가입을 할 수도 있는경우를 위해회원을 삭제 하는 것이 아니라 탈퇴 날짜를 지정해줌

class Rent:
    def __init__(self,rent): # 생성자
        self.__rent=rent

    def getRentInfo(self,ind): # 도서 대출 정보
        return self.__rent[ind,:]  

    def rent_Book(self,isbn,phone,dat): # 도서대출 (IF-013)
        add_info=np.array([int(self.__rent.size/6),isbn,phone,dat,dat,False])# 대출 정보를 numpy 형태로 변환
        # 날짜 형식 계산은 나중에 추가할 예정
        self.__rent=np.append(self.__rent,add_info,axis=0)# 대출 목록에 추가
        
    def search_Rent_ByBook(self,isbn): # ISBN으로 대출 조회 (IF-014)
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__rent[:,1]:
            if isbn==i:
                search_list=np.append(search_list,self.__rent[j,:])# ISBN이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/6),6))
        return search_list # 반환 값 : 대출 목록

    def search_Rent_ByUser(self, phone): # 연락처로 대출 조회 (IF-015) 
        search_list=np.array([]) # 검색된 대출 정보 저장할 리스트
        j=0 # 인덱스 체크용
        for i in self.__rent[:,2]:
            if phone==i:
                search_list=np.append(search_list,self.__rent[j,:])# 연락처가 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/6),6))
        return search_list# 반환 값 : 대출 목록
        
    def back_Book(self,ind):# 도서 반납 (IF-016)
        self.__rent[ind,5]=True# 인덱스 값에 해당하는 대출 반납처리

from tkinter import *

root=Tk()

class main: # 메인 GUI를 출력하는 클래스
    """
    def get_Book_Add(): # 도서 등록 페이지를 불러오는 메소드
    
    def get_Book_Search(): # 도서 조회 페이지를 불러오는 메소드

    def get_User_Add(): # 회원 등록 페이지를 불러오는 메소드

    def get_User_Search(): # 회원 조회 페이지를 불러오는 메소드
    
    def get_Rent_User_Search(): # 대출 실행 페이지를 불러오는 메소드

    def get_Rent_Search(): # 대출 조회 페이지를 불러오는 메소드
    
    """
BO=Book(book_list)
class book_add: #도서 등록하는 GUI를 출력하는 클래스
    
    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    def get_user(isbn): # ISBN 중복 확인을 위해 도서 리스트를 불러오는 위한 메소드
        if BO.get_IsIn(isbn): 
            print(" 이미 등록된 도서입니다.")
        else:
            print("등록 가능한 도서입니다.")
        
    def add_book(inf): # 등록 버튼을 눌렀을 때 등록한 도서의 정보가 원래 도서 리스트에 추가해 주는 메소드
        bookadd_label=Label("도서등록")
        ISBN_label=Label("ISBN")
        ISBN_textbox=Text(root,width=17,height=3)
        ISBN_textbox.pack()
        ISBN_btn=Button(root,text="중복확인",command=get_user)
        root.title("ISBN의 중복 확인")
        messagebox.showinfo("ISBN의 중복 확인",get_user) #메세지박스(박스제목,박스내용)

        bookname_label=Label("도서명 : ")
        bookname_textbox=Text(root,width=20,height=3)
        author_label=Label("저자 : ")
        author_textbox=Text(root,width=20,height=3)
        publisher_label=Label("출판사 : ")
        publisher_textbox=Text(root,width=20,height=3)
        price_label=Label("가격 : ")
        price_textbox=Text(root,width=20,height=3)
        URL_label=Label("관련URL : ")
        URL_textbox=Text(root,width=20,height=3)
        bookex_label=Label("도서 설명 : ")
        bookex_textbox=Text(root,width=20,height=3)

        add_btn=Button(root,text="등록")
        Cancel_btn=Button(root,text="취소")

        BO.add_Book_Info(inf) # 도서 등록 메소드 불러옴

class book_search: # 도서 조회 GUI를 출력하는 클래스
    
    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    #def column(column,option): # 표 열의 속성을 설정하는 메소드 -> gui?

    #def Heading(column,option): # 표의 행 제목을 설정하는 메소드
    
    def get_book_show(): # 도서 조회시 도서를 선택했을 때 book show 클래스를 불러오는 메소드 -> gui?
        book_show.print_book_info() # 조회한 책의 정보를 출력하는 메소드

    def print_book_list(): # 도서 조회시 관련 도서의 리스트를 화면에 출력해주는 메소드
        
        booksearch_label=Label("도서 조회 : ")
        bookname_label=Label("도서명 : ")
        book_textbox=Text(root,width=15,height=3)
        author_label=Label("저자 : ")
        author_textbox=Text(root,width=17,height=3)
        
        if book_textbox.get(): # 도서명이 입력된 경우
            print(BO.search_Book_ByTitle()) # 제목으로 도서 검색하는 함수 호출
        elif author_textbox.get(): # 저자명이 입력된 경우
            print(BO.search_Book_ByAuthor()) # 책 저자로 검색하는 함수 호출

    def get_book(ind): # 도서 정보를 불러오는 메소드
        print(BO) # 책 정보 확인 ( 도서 정보 리스트 출력 )
        
class book_show: # 선택한 도서 정보 GUI를 출력하는 클래스
    
    bookinfor_label=Label("도서 정보 - ISBN:9788970504773") # --> 도서가 바뀔때마다 바뀌도록 
    ISBN_label=Label("ISBN : ")
    ISBN_textbox=Text(root,width=20,height=3)
    bookname_label=Label("도서명 : ")
    bookname_textbox=Text(root,width=20,height=3)
    author_label=Label("저자 : ")
    author_textbox=Text(root,width=20,height=3)
    publisher_label=Label("출판사 : ")
    publisher_textbox=Text(root,width=20,height=3)
    price_label=Label("가격 : ")
    price_textbox=Text(root,width=20,height=3)
    URL_label=Label("관련URL : ")
    URL_textbox=Text(root,width=20,height=3)
    bookloan_label=Label("대출여부 : ")
    bookloan_textbox=Text(root,width=20,height=3)

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    def print_book_info(ind): # 조회한 책의 정보 출력을 위한 메소드
        book_show.get_book(ind) # 조회한 책의 정보를 불러오는 메소드 호출
        print(BO.book[ind,1]) # isbn 출력
        print(BO.book[ind,2]) # 제목 출력
        print(BO.book[ind,3]) # 저자 출력
        print(BO.book[ind,4]) # 출판사 출력
        print(BO.book[ind,5]) # 가격 출력
        print(BO.book[ind,6]) # 관련링크 출력
        print(BO.book[ind,7]) # 대출 여부 출력

        # -> 칸에 맞게 조회한 책의 정보를 출력해줌
            
    def modify_book(ind,inf): # 수정 버튼을 눌렀을 때 원래 도서 정보의 내용이 바뀌어서 저장되게 하기 위한 메소드
        BO.set_Book_Info(ind,inf) # 도서 수정 함수 호출

    def delete_book(ind): # 삭제 버튼을 눌렀을 때 해당된 도서 정보가 원래의 도서 리스트에서 삭제되어 도서 리스트에 저장 하기 위한 메소드
        BO.drop_Book_Info(ind)  # 도서 삭제 함수 호출

    def get_book(ind): # 도서 정보를 불러오는 메소드
        BO.get_Book_info(ind)

US=User(user_list)

class user_add: # 회원 등록 GUI를 출력하는 클래스

    useradd_label=Label("회원 등록")
    username_label=Label("이 름 : ")
    username_textbox=Text(root,width=20,height=3)
    userbirth_label=Label("생년월일 : ")
    userbirth_textbox=Text(root,width=20,height=3)
    userphone_label=Label("전화번호 : ")
    userphone_textbox=Text(root,width=20,height=3)
    usergender_label=Label("성 별 : ")
    usergender_textbox=Text(root,width=20,height=3)
    useremail_label=Label("이메일 : ")
    useremail_textbox=Text(root,width=20,height=3)
    userimage_label=Label("사 진 : ")
    userimage_textbox=Text(root,width=20,height=3)


    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    def check_user(): # 회원 중복 확인을 위한 메소드

        if US.get_IsIn():
            useradd_msgbox.showinfo(text="이미 등록된 회원입니다.")
        else:
            useradd_msgbox.showinfo(text="등록 가능한 회원입니다.")
    
    def add_user(inf): # 등록 버튼을 누를시에 이름, 생년월일, 전화번호, 성별, 이메일, 사진의 정보를 받아 원래 회원 리스트에 추가해주는 메소드
        US.add_User_Info(inf)

    # def search_photo(): # PC에서 사용자 사진을 찾도록 하는 메소드 --> gui


class user_saerch: # 회원 조회 GUI를 출력하는 클래스

    usersearch_label=Label("회원 조회")
    username_label=Label("이름 : ")
    userphone_label=Label("연락처 : ")

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    #def column(column,option): # 표 열의 속성을 설정하는 메소드
    
    #def Heading(column,option): # 표의 행 제목을 설정하는 메소드

    def get_user(ind): # 회원 정보를 불러오는 메소드
        US.get_User_info(ind)

    #def get_user_show(): # 회원 조회 시 회원을 선택했을 때 book show 클래스를 불러오는 메소드 -> 새창을 띄우는것 gui?

class user_show: # 선택한 회원 정보 GUI를 출력하는 클래스

    userInfo_label=Label("회원 정보")
    name_label=Label("이름")
    birth_label=Label("생년월일")
    phone_label=Label("전화번호")
    gender_label=Label("성별")
    mail_label=Label("이메일")
    rent_check_label=Label("대출여부")
    withdrawal_check_label=Label("탈퇴여부")

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

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
    
    #def find_photo(): # 사진 경로를 찾는 메소드 -> gui

RE=Rent(rent_list)
class rent_user_search: # 도서 대출을 실행할 회원을 조회하는 GUI를 출력하는 클래스

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

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

class rent_book_search: # 대출할 도서 정보 검색 GUI를 출력하는 클래스

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

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

class rent_show: # 대출 정보 GUI를 출력해주는 클래스

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

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

class rent_search: # 대여 조회 GUI를 출력하는 클래스

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    #def column(column,option): # 표 열의 속성을 설정하는 메소드
    
    #def Heading(column,option): # 표의 행 제목을 설정하는 메소드
    
    def get_rent(isbn,phone,dat): # 대출 정보를 불러오는 메소드 --> 도서정보,회원정보를 불러오는것?
        Book.rent_Book(isbn,phone,dat)
        
    #def get_rent_state_show(): # 대출 조회 시, 확인을 원하는 대출 내역을 선택했을 때 get_rent_state_show() 클래스를 불러오는 메소드

class rent_state_show: # 선택한 대출 정보 GUI를 출력해주는 클래스

    #def onClick(): # 클릭 이벤트 처리를 위한 메소드

    def book_return(ind): # 도서 반납 메소드
        Book.back_Book(ind)

    def get_rent_book_info(ind): # 대출된 도서의 정보를 불러오는 메소드
        Rent.getRentInfo(ind)

    def get_rent_user_info(ind): # 대출을 실행한 회원의 정보를 불러오는 메소드 -> 해당 책을 빌린 사람의 정보
        User.get_User_info(ind)

    #def get_rent_info(): # 상단 대출 정보를 표시하는 메소드 -> gui ?
        






