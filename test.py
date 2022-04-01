import pandas as pd

df=pd.read_csv('./Rent.csv', encoding='UTF-8') # cvs파일 불러옴
df1=pd.read_csv('./User.csv', encoding='UTF-8')
df2=pd.read_csv('./Book.csv', encoding='UTF-8')

class Book:
    def __init__(self,isbn,title,author,pub,price,link,description,pre=True):#생성자
        self.isbn=isbn
        self.title=title
        self.author=author
        self.pub=pub
        self.price=price
        self.link=link
        self.description=description
        self.pre=pre
    def setInfo(self,title,author,pub,price,link,description):
        self.title=title
        self.author=author
        self.pub=pub
        self.price=price
        self.link=link
        self.description=description
    def setPre(self,pre):#설정자/ 존재여부
        self.pre=pre
    def getPre(self):#접근자
        return self.pre

class User:
    def __init__(self,phone,name,brith,gender,mail,reg,out,cnt):
        self.phone=phone
        self.name=name
        self.birth=birth
        self.gender=gender
        self.mail=mail
        self.reg=reg
        self.out=out
        self.cnt=cnt
    def setCnt(self,cnt):
        self.cnt+=cnt
    def getCnt(self):
        return cnt

def i_01(isbn):
    ilist=df2["ISBN"].to_list()
    print(ilist)
    print(isbn)
    if isbn in ilist:
        return True
    else:
        return False
print(df)
