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
        
    def get_Book_info(self,ind): # 책 정보 확인
        return self.__book[ind,:]# 인덱스에 해당하는 책 정보를 리턴

    def search_Book_ByTitle(self,title): # 책 제목으로 검색 (IF-003)
        search_list=np.array([])# 검색된 책 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__book[:1]:
            if title==i:
                search_list=np.append(search_list,self.__book[j,:])# 제목이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list # 반환 값 : 도서 목록
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
    
    def set_Book_Info(self,ind,inf): # 도서 수정 (IF-05)
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 책 정보 삽입
   
    def add_Book_Info(self,inf): # 도서 추가 (IF-002)
        self.__book=np.append(self.__book,inf,asix=0)# 행 방향으로 정보 추가
        
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
        
    def get_User_info(self,ind): # 회원 정보 확인 (IF-008)
        return self.__user[ind,:]#인덱스에 해당하는 책 정보 리턴

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
    
    def search_User_ByName(self,name): # 이름으로 회원 조회 (IF-009)
        search_list=np.array([])# 검색된 회원 정보 저장할 리스트
        j=0# 인덱스 체크용
        for i in self.__user[:2]:
            if title==i:
                search_list=np.append(search_list,self.__user[j,:])# 이름이 동일하면 리스트에 추가
            j+=1
        search_list=np.reshape(search_list,(int(search_list,size/8),8))
        return search_list# 반환 값 : 회원 목록
    
    def set_User_Info(self,ind,inf): # 회원 수정 (IF-011)
        self.__user[ind,:]=inf# 인덱스 값에 해당하는 회원 정보 삽입

    def add_User_Info(self,inf): # 회원 등록 (IF-008)
        self.__user=np.append(self.__book,inf,axis=0)# 행 방향으로 정보 추가
        
    def drop_User_Info(self,ind,dat): # 회원 탈퇴 (IF-012)
        self.__user[ind,6]=dat# 인덱스 값에 해당하는 회원 탈퇴일자 저장
        # 회원 탈퇴 시 재가입을 할 수도 있는경우를 위해회원을 삭제 하는 것이 아니라 탈퇴 날짜를 지정해줌

class Rent:
    def __init__(self,rent): # 생성자
        self.__rent=rent
        
    def rent_Book(self,isbn,phone,dat): # 도서대출  (IF-013)
        add_info=np.array([int(self.__rent.size/6),isbn,phone,dat,dat,False])# 대출 정보를 numpy 형태로 변환
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

from tkinter import *

root=Tk()

class book_add:
    B1=Book(book_list)

    #def onClick():

    def get_user():
        if B1.get_IsIn(isbn) == True:
            print(" 이미 등록된 도서입니다.")
        else:
            print("등록 가능한 도서입니다.")
        
    def add_book():
        bookadd_label=Label("도서등록")
        ISBN_label=Label("ISBN")
        ISBN_btn=Button(root,text="중복확인",command=get_user)
        root.title("ISBN의 중복 확인")
        messagebox.showinfo("ISBN의 중복 확인",get_user) #메세지박스(박스제목,박스내용)

