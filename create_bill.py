import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton,  QWidget, QGridLayout ,QLineEdit ,QMessageBox,QCalendarWidget,QTableWidget,QTableWidgetItem,QAbstractItemView

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import mysql.connector
from mysql.connector import Error
from datetime import datetime
cnx = mysql.connector.connect(user='root', password='Ya3an3anter', host='127.0.0.1')

# Check if a database exists
cursor = cnx.cursor()
cursor.execute("SHOW DATABASES LIKE 'application'")
result = cursor.fetchone()
if result:
  print("The database exists.")
  try:
      connection = mysql.connector.connect(host='127.0.0.1',
                                           port='3306',
                                           database='application',
                                           user='root',
                                           password="Ya3an3anter",
                                           auth_plugin='mysql_native_password')
      if connection.is_connected():
          db_Info = connection.get_server_info()
          print("Connected to MySQL Server version ", db_Info)
          cursor = connection.cursor(buffered=True)
          # cursor = connection.cursor()
          cursor.execute("select database();")
          record = cursor.fetchone()
          print("You're connected to database: ", record)
          cursor.execute("SELECT * FROM application.items")
  except Error as e:
      print("Error while connecting to MySQL", e)
else:
  print("The database does not exist.")
  cursor.execute("CREATE DATABASE mydb")
  try:
      connection = mysql.connector.connect(host='127.0.0.1',
                                           port='3306',
                                           database='application',
                                           user='root',
                                           password="Ya3an3anter",
                                           auth_plugin='mysql_native_password')
      if connection.is_connected():
          db_Info = connection.get_server_info()
          print("Connected to MySQL Server version ", db_Info)
          cursor = connection.cursor(buffered=True)
          # cursor = connection.cursor()
          cursor.execute("select database();")
          record = cursor.fetchone()
          print("You're connected to database: ", record)
          cursor.execute("create table items(item_name  varchar(100) not null primary key, item_stock float(10, 3) not null,item_price int not null)")
          cursor.execute("create table supplier ( supplier_id           int          not nullprimary key,supplier_name         varchar(100) not null, supplier_phone_number varchar(11)  null  )")
          cursor.execute("create table supplier_bill (  supplier_bill_id int auto_incrementprimary key, bill_date    date null, supplier_id      int  not null, money_payed  int  not null, constraint supplier_bill_ibfk_1  foreign key (supplier_id) references supplier (supplier_id))")
          cursor.execute("create table commande_supplier ( quantiter        float(8, 3)  not null,supplier_bill_id int          not null, price            int          not null, item_name       varchar(100) not null, primary key (supplier_bill_id, item_name),  constraint commande_supplier_ibfk_1 foreign key (supplier_bill_id) references supplier_bill (supplier_bill_id), constraint commande_supplier_ibfk_2 foreign key (item_name) references items (item_name))")
          cursor.execute("create index supplier_id on supplier_bill (supplier_id)")
          cursor.execute("create index item_name on commande_supplier (item_name)")
          cursor.execute("create index supplier_id on supplier_bill (supplier_id)")
          cursor.execute("create table the_client ( cin   int          not nullprimary key,client_full_name    varchar(150) not null,client_phone_number varchar(15)  null)")
          cursor.execute("create table client_bill( client_bill_id   int auto_increment primary key,  client_bill_date date not null,  cin   int  not null, money_payed      int  not null, constraint client_bill_ibfk_1 foreign key (cin) references the_client (cin))")
          cursor.execute("create index cin on client_bill (cin)")
          cursor.execute("create table commande_client(quantiter float(8, 3)  not null, quantiter_price int   not null, client_bill_id  int   not null, item_name   varchar(100) not null, primary key (client_bill_id, item_name), constraint commande_client_ibfk_1 foreign key (client_bill_id) references client_bill (client_bill_id),  constraint commande_client_ibfk_2)  foreign key (item_name) references items (item_name))")
          cursor.execute("create index item_name on commande_client (item_name)")

  except Error as e:
      print("Error while connecting to MySQL",e)






class bill:
    def __init__(self,client_bill_id,client_bill_date,cin,money_payed):
        self.client_bill_id=client_bill_id
        self.client_bill_date=client_bill_date
        self.cin=cin
        self.money_payed=money_payed
        self.commande = []
    @classmethod
    def create_bills(cls,cin):
        cursor.execute(f"select client_bill_id,client_bill_date,money_payed from client_bill where cin={cin} order by client_bill_date")
        all_bills=[]
        for x in cursor:
            all_bills.append(bill(str(x[0]),str(x[1]),str(cin),str(x[2])))
        return all_bills
class supplier_bill:
    def __init__(self,supplier_bill_id,bill_date,supplier_id,money_payed):
        self.supplier_bill_id=supplier_bill_id
        self.bill_date=bill_date
        self.supplier_id=supplier_id
        self.money_payed=money_payed
        self.commande=[]
    @classmethod
    def create_bills(cls,cin):
        cursor.execute(f"select supplier_bill_id,bill_date,money_payed from supplier_bill where supplier_id={cin} order by bill_date")
        all_bills=[]
        for x in cursor:
            all_bills.append(supplier_bill(str(x[0]),str(x[1]),str(cin),str(x[2])))
        return all_bills
class commande_client:
    def __init__(self,quantiter,quantiter_price,client_bill_id,item_name):
        self.quantiter=quantiter
        self.quantiter_price=quantiter_price
        self.client_bill_id=client_bill_id
        self.item_name=item_name
    @classmethod
    def create_commande_client(cls,client_bill_id):
        cursor.execute(f"delete from commande_client where client_bill_id={client_bill_id} and quantiter=0")
        connection.commit()
        cursor.execute(f"select quantiter,quantiter_price,item_name from commande_client where client_bill_id={client_bill_id}")
        all_commande=[]

        for x in cursor:
           all_commande.append(commande_client(str(x[0]),str(x[1]),str(client_bill_id),str(x[2])))
        return all_commande
class commande_supplier:
    def __init__(self, quantiter,price, supplier_bill_id, item_name) :
        self.quantiter=quantiter
        self.price=price
        self.supplier_bill_id=supplier_bill_id
        self.item_name=item_name
    @classmethod
    def create_commande_supplier(cls,client_bill_id):
        cursor.execute(f"select quantiter,price,item_name from commande_supplier where supplier_bill_id={client_bill_id}")
        all_commande=[]
        for x in cursor:
           all_commande.append(commande_supplier(str(x[0]),str(x[1]),str(client_bill_id),str(x[2])))
        return all_commande
class items:
    def __init__(self,item_name,item_price,item_stocks,item_quantiter):
        self.item_name=item_name
        self.item_price=item_price
        self.item_stocks=item_stocks
        self.item_quantiter=item_quantiter
        self.price=None
    def create_item(self):
        cursor.execute(f"select count(*) from application.items where item_name='{self.item_name}'")
        for x in cursor:
            k=x[0]
        if k==1:
            return False
        else :
            ch=f"insert into items (item_name,item_stock,item_prix) values ('{self.item_name}',{str(self.item_stocks)},{str(self.item_price)})"
            print(f"insert into application.items (item_name,item_stock,item_prix) values ('{self.item_name}',{str(self.item_stocks)},{str(self.item_price)})")
            cursor.execute(f"insert into application.items (item_name,item_stock,item_price) values ('{self.item_name}',{str(self.item_stocks)},{str(self.item_price)})")
            connection.commit()
            return True
    @classmethod
    def create_items(cls):
        l=[]
        cursor.execute("select item_name,item_price,item_stock from application.items ")
        for x in cursor:
            l.append(items (str(x[0]),
                              str(x[1]),
                                str(x[2]),
                                0))
        return l


class client :
    def __init__(self,name,phone_number,cin):
        self.full_name=name
        self.phone_number=phone_number
        self.cin=cin
        self.bill=[]
        self.total_money=None
        self.money_given=None
        self.rest=None
        self.last_bill_date=None
    def create_clent_bill_commande(self,items,date,money_payed):
        cursor.execute(f"select count(cin) from the_client where cin={str(self.cin)}")
        print(money_payed,str(money_payed))
        for x in cursor:
            k=x[0]
        if k==1:
            pass
        else:
            cursor.execute(f"insert into the_client (client_full_name,client_phone_number,cin) values ('{self.full_name}','{self.phone_number}',{str(self.cin)})")
            connection.commit()
        query_create_bill=f"select count(*) from client_bill where cin={str(self.cin)} and client_bill_date='{date}'"
        cursor.execute(query_create_bill)
        for x in cursor:
            n=x[0]
        if n==0:
            query_create_bill=f"insert into client_bill (client_bill_date,cin,money_payed) values ('{date}',{self.cin},{money_payed})"
        else:
            query_create_bill=f"update client_bill set money_payed=money_payed+{str(money_payed)} where cin={str(self.cin)}  and client_bill_date='{date}'"
            print(query_create_bill)
        print(query_create_bill)
        cursor.execute(query_create_bill)
        connection.commit()
        query_commande=[]
        query_item=[]
        cursor.execute(f"select client_bill_id from client_bill where client_bill_date='{date}' and cin={self.cin}")
        for x in cursor:
            client_bill_id=x[0]
        for item in items:
            cursor.execute(f"select count(*) from commande_client where client_bill_id={client_bill_id} and item_name='{item.item_name}' ")
            for x in cursor:
                k=x[0]
            if k==0:
              if float(str(item.item_quantiter))!=0:
                    query_commande.append(f"insert into commande_client  (quantiter,quantiter_price,client_bill_id,item_name) values ({item.item_quantiter},{int(float(item.item_quantiter)*int(item.item_price))},{client_bill_id},'{item.item_name}') ")
            else:
                if float(item.item_quantiter) != 0:
                    query_commande.append(
                        f"update commande_client set quantiter=quantiter+{str(item.item_quantiter)} where client_bill_id={client_bill_id} and item_name='{item.item_name}'")
                    query_commande.append(f"update commande_client set quantiter_price=quantiter_price+{str(int(float(item.item_quantiter)*int(item.item_price)))} where client_bill_id={client_bill_id} and item_name='{item.item_name}'")
            if float(str(item.item_quantiter)) != 0:
               query_item.append(f"update items set item_stock=item_stock-{str(item.item_quantiter)}  where item_name='{item.item_name}'")
               item.item_stocks=str(float(float(item.item_stocks))-float(str(item.item_quantiter)))
               print("test")
        for i in range(len(query_commande)):
            cursor.execute(query_commande[i])
            if i>=len(query_item):
                continue
            else :
                cursor.execute(query_item[i])
            connection.commit()
        return items
    @classmethod
    def create_clients(cls):
        cursor.execute("select cin,client_full_name,client_phone_number from the_client")
        all_client=[]
        for clientt in cursor:
            all_client.append(client(str(clientt[1]),str(clientt[2]),str(clientt[0])))
        return all_client
class supplier:
    def __init__(self,id,name,phone_number):
        self.id=id
        self.name=name
        self.phone_number=phone_number
        self.bill=[]
    def create_commande(self,items,money_payed,date):
        cursor.execute(f"select count(*) from supplier where supplier_id={str(self.id)}")
        print(money_payed, str(money_payed))
        print("date " ,date)
        for x in cursor:
            k = x[0]
        if k == 1:
            pass
        else:
            cursor.execute( f"insert into supplier (supplier_name,supplier_phone_number,supplier_id) values ('{self.name}','{self.phone_number}',{str(self.id)})")
            connection.commit()
        query_create_bill = f"select count(*) from supplier_bill where supplier_id={str(self.id)} and bill_date='{date}'"
        cursor.execute(query_create_bill)
        for x in cursor:
            n = x[0]
        if n == 0:
            query_create_bill = f"insert into supplier_bill (bill_date,supplier_id,money_payed) values ('{date}',{self.id},{money_payed})"
        else:
            query_create_bill = f"update supplier_bill set money_payed=money_payed+{str(money_payed)} where supplier_id={str(self.id)}  and bill_date='{date}'"
        print(query_create_bill)
        cursor.execute(query_create_bill)
        connection.commit()
        query_commande = []
        query_item = []
        cursor.execute(f"select supplier_bill_id from supplier_bill where bill_date='{date}' and supplier_id={self.id}")
        for x in cursor:
            client_bill_id = x[0]
        for item in items:
            cursor.execute(
                f"select count(*) from commande_supplier where supplier_bill_id={client_bill_id} and item_name='{item.item_name}' ")
            for x in cursor:
                k = x[0]
            if k == 0:
                if float(item.item_quantiter) != 0:
                    query_commande.append(f"insert into commande_supplier  (quantiter,price,supplier_bill_id,item_name) values ({item.item_quantiter},{int(float(item.price))},{client_bill_id},'{item.item_name}') ")
            else:
                if float(item.item_quantiter) != 0:
                  if float(item.item_quantiter)>0:
                    query_commande.append(f"update commande_supplier set quantiter=quantiter+{str(item.item_quantiter)} where supplier_bill_id={client_bill_id} and item_name='{item.item_name}'")
                    query_commande.append(f"update commande_supplier set price=price+{str(item.price)} where supplier_bill_id={client_bill_id} and item_name='{item.item_name}'")

                  else:
                      query_commande.append(f"update commande_supplier set quantiter=quantiter-{str(int(item.item_quantiter)*-1)} where supplier_bill_id={client_bill_id} and item_name='{item.item_name}'")
            if float(item.item_quantiter) != 0:
              query_item.append(f"update items set item_stock=item_stock+{str(item.item_quantiter)}  where item_name='{item.item_name}'")
              item.item_stocks = str(float(item.item_stocks) +float(item.item_quantiter))
        for i in range(len(query_item)):
            cursor.execute(query_commande[i])
            cursor.execute(query_item[i])
            connection.commit()

    @classmethod
    def create_supplier(cls):
            cursor.execute("select supplier_id,supplier_phone_number,supplier_name from supplier")
            all_supplier = []
            for clientt in cursor:
                all_supplier.append(supplier(phone_number=str(clientt[1]),name= str(clientt[2]),id= str(clientt[0])))
            return all_supplier

def money(ch):
    p=len(ch)
    while p>3:
        print(p)
        ch=ch[0:p-3]+","+ch[p-3:len(ch)]
        p=p-3
    return ch
def see_total(items,money_payed,welcome_label,table):
        if money_payed =="" :
            money_payed="0"
        l=list(filter(lambda score: score.isalpha()==True,money_payed.split()))
        print(l)
        print(len(l))
        print(money_payed.split())
        m=money_payed.split()
        print(m[0].isalpha())
        if len(l)>=1 or len(m)>1:
            money_payed=0

        print(money_payed)
        total=0
        i=0
        for item in items:
            i = i + 1
            if str(table.item(i, 3).text()) != "" :
                if (str(table.item(i,3).text())[0]=="-" and str(table.item(i,3).text())[1:].isdigit() )or str(table.item(i,3).text()).isdigit() or str(table.item(i,3).text())[0].isdecimal() :
                  item.item_quantiter = str(table.item(i, 3).text())
                  item.item_price=str(table.item(i,1).text())
                  print(str(table.item(i, 3).text()))

        for item in items:
            if item.item_quantiter!='0':
                total=total+float(item.item_quantiter)*int(item.item_price)
        rest=total-int(money_payed)
        welcome_label.setText("total : "+money(str(int(total)))+ " rest : "+money(str(int(rest))))


def clear_widgets():
 #    hide all existing widgets and erase
  #      them from the global dictionary
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()
#all the widgets for all the window
widgets={
    "see_total":[],
    "money_entry":[],
    "search_supplier_bill":[],
    "search_client_bill":[],
   "phone_entry":[],
   "phone_label":[],
   "cin_entry":[],
    "cin_label":[],
    "stock_entry":[],
    "stock_label":[],
    "price_entry":[],
    "price_label":[],
    "Create_supplier_bill":[],
    "full_name_label":[],
    "table":[],
    "calender":[],
    "acces":[],
    "explain_label":[],
    "door_cces":[],
    "confirm":[],
    "id_entry":[],
    "full_name":[],
    "id_label":[],
    "button":[],
    "logo":[],
    "label":[],
    "create_button":[],
    "select_button":[],
    "update_button":[],
    "update_full_name":[],
    "update_acces":[],
    "update_image":[]
}

app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle("GUI")
#window.setFixedWidth(1000)
#window.setFixedHeight(700)
window.setGeometry(0,0,1000,600)
window.move(400,200)
window.setStyleSheet("background : #00000")
def create_button(text):#create buttons with the same style
    ch= "*{border : 4px solid '#5B2A86';"+ "border-radius: 45px;"+ "font-size: 35px;"+"color:'#5B2A86' ;"+"padding: 20px 0;"+"margin: 10px 10px ;}"+"*:hover{background: '#A5E6BA';}"
    create_worker_button = QPushButton(text)
    create_worker_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    create_worker_button.setStyleSheet(ch)
    return create_worker_button


grid=QGridLayout()
def confirm_create_item(item_name,item_price,item_stock):
    new_item=items(str(item_name.text()),str(item_price.text()),str(item_stock.text()),0)
    test=new_item.create_item()
    if test:
        QMessageBox.information(None, "Succes", "Item created succesfuly  ")
    else :
        QMessageBox.critical(None, 'Fail', "Item have the same name already exist ")


def confirm_item_price(item_name,item_price):
    item_name=str(item_name.text())
    item_price=str(item_price.text())
    if item_name!="":
        if item_price!="":
            cursor.execute(f"select count(*) from application.items where item_name='{item_name}'")
            for x in cursor:
                k = x[0]
            if k == 1:
             if int(item_price)>0:
                cursor.execute(f"update application.items set item_price={item_price} where item_name='{item_name}'")
                connection.commit()
                QMessageBox.information(None, "Succes", "Item price updated succesfuly   ")
             else:
                QMessageBox.critical(None, 'Fail', "Item price can't be negative !! ")
            else :
                QMessageBox.critical(None, 'Fail', "Item doesn't exist !! ")

        else:
            QMessageBox.critical(None, 'Fail', "Please enter the new item price  ")
    else :
        QMessageBox.critical(None, 'Fail', "Please enter Item name  ")
def confirm_item_stock_2(item_name,item_stock):
    item_name = str(item_name.text())
    item_stock = str(item_stock.text())
    if item_name != "":
        if item_stock != "":
            cursor.execute(f"select count(*) from application.items where item_name='{item_name}'")
            for x in cursor:
                k = x[0]
            if k == 1:
                if float(item_stock) >= 0:
                    cursor.execute(
                        f"update application.items set item_stock=item_stock-{item_stock} where item_name='{item_name}'")
                    connection.commit()
                    QMessageBox.information(None, "Succes", "Item stock updated succesfuly   ")
                else:
                    QMessageBox.critical(None, 'Fail', "Item stock can't be negative !! ")
            else:
                QMessageBox.critical(None, 'Fail', "Item doesn't exist !! ")

        else:
            QMessageBox.critical(None, 'Fail', "Please enter the new item stock  ")
    else:
        QMessageBox.critical(None, 'Fail', "Please enter Item name  ")
def confirm_item_stock(item_name,item_stock):
        item_name = str(item_name.text())
        item_stock = str(item_stock.text())
        if item_name != "":
            if item_stock != "":
                cursor.execute(f"select count(*) from application.items where item_name='{item_name}'")
                for x in cursor:
                    k = x[0]
                if k == 1:
                    if float(item_stock) >= 0:
                        cursor.execute(
                            f"update application.items set item_stock={item_stock} where item_name='{item_name}'")
                        connection.commit()
                        QMessageBox.information(None, "Succes", "Item stock updated succesfuly   ")
                    else:
                        QMessageBox.critical(None, 'Fail', "Item stock can't be negative !! ")
                else:
                    QMessageBox.critical(None, 'Fail', "Item doesn't exist !! ")

            else:
                QMessageBox.critical(None, 'Fail', "Please enter the new item stock  ")
        else:
            QMessageBox.critical(None, 'Fail', "Please enter Item name  ")
def confirm_create_client_bill(full_name,cin,phone_number,calender,table,items,money_entry):
    full_name=str(full_name.text())
    cin=str(cin.text())
    if cin=="" or  not (cin.isdigit()):
        cin="0"
    phone_number=str(phone_number.text())
    if phone_number == "" or not (phone_number.isdigit()):
        phone_number="0"
    date=str(calender.selectedDate().toString(Qt.ISODate))
    money=str(money_entry.text())
    print("money ",money )
    if money=="" :
        money="0"
    elif money[0]=="-" or (money[0]!="-" and not money.isdigit()):
        if not money[1:].isdigit():
            money="0"
    else:
        money=str(money_entry.text())
    print(money)
    i=0
    for item in items:
        i=i+1
        item_quantiter=str(table.item(i, 3).text())
        print("item quantiter", item_quantiter)
        if item_quantiter == "":
            item_quantiter = "0"
        elif item_quantiter[0] == "-" or (item_quantiter[0] != "-" and not item_quantiter.isdigit()):
            if not item_quantiter[1:].isdigit():
                item_quantiter = "0"

        item_price=str(table.item(i,1).text())
        if item_price == "":
            item_price = item.item_price
        elif item_price.isdigit():
            item_price = str(table.item(i, 1).text())
        elif item_price=="0":
            item_price = item.item_price
        else:
            item_price=item.item_price
        item.item_quantiter=item_quantiter
        item.item_price=item_price
    the_client=client(full_name,phone_number,cin)
    items=the_client.create_clent_bill_commande(items,date,money)
    QMessageBox.information(None, "Succes", "Bill created succesfuly   ")
    i=0
    for x in items:
        i=i+1
        table.setItem(i, 3, QTableWidgetItem("0"))
        table.setItem(i, 2, QTableWidgetItem(x.item_stocks))


def confirm_create_supplier_bill(full_name,cin,phone_number,calender,table,items,money_entry):
    full_name=str(full_name.text())
    cin=str(cin.text())
    if cin=="" or  not (cin.isdigit()):
        QMessageBox.critical(None, 'Fail', "Please enter supplier id !! ")
        return None
    phone_number=str(phone_number.text())
    if phone_number == "" or not (phone_number.isdigit()):
        phone_number="0"
    date=str(calender.selectedDate().toString(Qt.ISODate))
    money=str(money_entry.text())
    if money=="" or  not (money.isdigit()):
        money="0"
    i=0
    for item in items:
        i=i+1
        item_quantiter = str(table.item(i, 2).text())
        print("item quantiter", item_quantiter)
        if item_quantiter == "":
            item_quantiter = "0"
        elif item_quantiter[0] == "-" or (item_quantiter[0] != "-" and not item_quantiter.isdigit()):
            if not item_quantiter[1:].isdigit():
                item_quantiter = "0"

        item_price = str(table.item(i, 3).text())
        if item_price == "":
            item_price="0"
        elif item_price.isdigit():
            item_price = str(table.item(i, 3).text())
        else:
            item_price="0"

        item.item_quantiter = item_quantiter
        item.price = item_price

    provider=supplier(cin,full_name,phone_number)
    provider.create_commande(items,money,date)
    QMessageBox.information(None, "Succes", "Bill created succesfuly   ")
    i=0
    for item in items:
        i = i + 1
        table.setItem(i, 3, QTableWidgetItem("0"))
        table.setItem(i, 2, QTableWidgetItem("0"))


def supplier_bill_fn(all_bills,all_commande,type):
    clear_widgets()
    supplier_bills_frame(all_bills, all_commande,type)
def client_bills_fn(all_bills,all_commande,type):
    clear_widgets()
    client_bills_frame(all_bills,all_commande,type)
def update_stock_fn():
    clear_widgets()
    update_stock_frame()
def update_price_fn():
    clear_widgets()
    update_price_frame()
def create_client_bill_fn():
    clear_widgets()
    create_client_bill_frame()
def back_to_search_client():
    clear_widgets()
    search_for_client_frame()
def back_to_search_supplier():
    clear_widgets()
    search_for_supplier_frame()



def create_item_fn():#clear all the widgets from the frame then move to the create worker  frame
    clear_widgets()
    create_item_frame()
def back_to_main():
    clear_widgets()
    main_frame()
def search_for_client_fn():
    clear_widgets()
    search_for_client_frame()
def update_worker():
    clear_widgets()
    update_frame()
def select_date(type):
    clear_widgets()
    select_frame(type)
def search_name_supplier(full_name,clients,table,type):
    searched_client = []
    full_name = str(full_name.text())
    if type == "Full name":
        for clientt in clients:
            name = clientt.name
            print(name)
            print(full_name)
            if len(full_name) <= len(name):
                name = name[:len(full_name)]
                print(name)
            if name == full_name:
                searched_client.append(clientt)
    elif type == "Cin":
        for clientt in clients:
            if int(clientt.id) == int(full_name):
                searched_client.append(clientt)
    else:
        for clientt in clients:
            if str(clientt.phone_number) == full_name:
                searched_client.append(clientt)
    table.setRowCount(len(searched_client) + 1)
    i = 0
    for clientt in searched_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.id)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.name)))
        table.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
def search_name(full_name,clients,tablee,type):
    searched_client=[]
    full_name = str(full_name.text())
    table=tablee[0]
    if type=="Full name":
        for clientt in clients:
            name=clientt.full_name
            print(name)
            print(full_name)
            if len(full_name)<=len(name):
                name=name[:len(full_name)]
                print(name)
            if name==full_name:
                searched_client.append(clientt)
    elif type=="Cin":
        for clientt in clients:
            if int(clientt.cin)==int(full_name):
                searched_client.append(clientt)
    else:
        for clientt in clients:
            if str(clientt.phone_number)==full_name:
                searched_client.append(clientt)
    table.setRowCount(len(searched_client)+1)
    i=0
    for clientt in searched_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        table.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
    tablee[0]=table
def select_supplier_profile(clients,table,type):
    k = 0
    for currentQTableWidgetItem in table.selectedItems():
        print(currentQTableWidgetItem.row())
        k = currentQTableWidgetItem.row()
    cin = str(table.item(k,0).text())
    print(cin)
    all_bills = supplier_bill.create_bills(cin)
    all_commande = []
    for billl in all_bills:
        bill_id = billl.supplier_bill_id
        all_commande.append(commande_supplier.create_commande_supplier(bill_id))
    supplier_bill_fn(all_bills, all_commande,type)
def select_client_profile(clients,tablee,type):
    k = 0
    table=tablee[0]
    for currentQTableWidgetItem in table.selectedItems():
        print(currentQTableWidgetItem.row())
        k = currentQTableWidgetItem.row()
    cin = str(table.item(k,0).text())
    print(cin)
    all_bills=bill.create_bills(cin)
    all_commande=[]
    for billl in all_bills:
        bill_id=billl.client_bill_id
        all_commande.append(commande_client.create_commande_client(bill_id))
    client_bills_fn(all_bills,all_commande,type)


def conferm_full_name(name_entry,id_entry):#this function is for conferming the update of the worker full name and not allowing to update it to empty
    name=str(name_entry.text())
    k=1
    if name!="":
        id=int(str(id_entry.text()))
        cursor.execute(f"select count(user_id) from user_data where user_id={str(id)} ")
        for x in cursor:
            k=x[0]
        if k==1:
            cursor.execute(f"update user_data set full_name='{name}' where user_id={str(id)}")
            connection.commit()
            QMessageBox.information(None,"Succes","Update full name succesfuly ")
        else:
            QMessageBox.critical(None,'Fail', "Worker doesn't exist  ")

    else:
        QMessageBox.critical(None,'Fail',"Full name can't be empty ")
def create_supplier_bill_fn():
    clear_widgets()
    create_supplier_bill_frame()
def search_for_supplier_fn():
    clear_widgets()
    search_for_supplier_frame()
def select_fn(calander,type):

    selected_date =str(calander.selectedDate().toString(Qt.ISODate))
    clients=[]
    suppliers=[]
    i=0
    if type=="all":
        cursor.execute(f"select b.client_bill_id,b.money_payed,c.cin,c.client_full_name,c.client_phone_number from client_bill b,the_client c where client_bill_date= '{selected_date}' and c.cin=b.cin ")
        for x in cursor:
           clients.append(client(
               name=str(x[3]),
               phone_number=str(x[4]),
               cin=str(x[2])
           ))
           clients[i].bill.append(bill(client_bill_id=str(x[0]),
                                       client_bill_date=str(selected_date),
                                       cin=str(x[2]),
                                       money_payed=str(x[1])))
           i=i+1
        i=0
        cursor.execute(f"select b.supplier_bill_id,b.money_payed,s.supplier_id,s.supplier_name,s.supplier_phone_number from supplier_bill b,supplier s where bill_date= '{selected_date}' and s.supplier_id=b.supplier_id ")
        for x in cursor:
            suppliers.append(supplier(id=str(x[2]),
                                      name=str(x[3]),
                                      phone_number=str(x[4])))
            suppliers[i].bill.append(supplier_bill(money_payed=str(x[1]),
                                                  bill_date=selected_date,
                                                   supplier_bill_id=str(x[0]),
                                                   supplier_id=str(x[2])))
            i=i+1
        k=0
        for clientt in clients:
            client_bill_id=clientt.bill[0].client_bill_id
            cursor.execute(f"select item_name,quantiter,quantiter_price from commande_client where client_bill_id={client_bill_id}")
            print(f"select item_name,quantiter,quantiter_price from commande_client where client_bill_id={client_bill_id}")
            test=k
            for x in cursor:
                print("test",k)
                k=k+1
                clientt.bill[0].commande.append(commande_client(client_bill_id=client_bill_id,
                                                             item_name=str(x[0]),
                                                                quantiter=str(x[1]),
                                                                quantiter_price=str(x[2])))
            if test==k:
                k=k+1
            else:
                test=k
        for suplierr in suppliers:
            client_bill_id=suplierr.bill[0].supplier_bill_id
            cursor.execute(f"select item_name,quantiter,price from commande_supplier where supplier_bill_id={client_bill_id}")
            test=k
            for x in cursor:
                print("test sup",k)
                k=k+1
                suplierr.bill[0].commande.append(commande_supplier(supplier_bill_id=client_bill_id,
                                                                item_name=str(x[0]),
                                                                quantiter=str(x[1]),
                                                                price=str(x[2])))
            if test==k:
                k=k+1
            else:
                test=k
    elif type=="client":
        cursor.execute(
            f"select b.client_bill_id,b.money_payed,c.cin,c.client_full_name,c.client_phone_number from client_bill b,the_client c where client_bill_date= '{selected_date}' and c.cin=b.cin ")
        for x in cursor:
            clients.append(client(
                name=str(x[3]),
                phone_number=str(x[4]),
                cin=str(x[2])
            ))
            clients[i].bill.append(bill(client_bill_id=str(x[0]),
                                        client_bill_date=str(selected_date),
                                        cin=str(x[2]),
                                        money_payed=str(x[1])))
            i = i + 1
        k = 0
        for clientt in clients:
            client_bill_id = clientt.bill[0].client_bill_id
            cursor.execute(
                f"select item_name,quantiter,quantiter_price from commande_client where client_bill_id={client_bill_id}")
            print(
                f"select item_name,quantiter,quantiter_price from commande_client where client_bill_id={client_bill_id}")
            test = k
            for x in cursor:
                print("test", k)
                k = k + 1
                clientt.bill[0].commande.append(commande_client(client_bill_id=client_bill_id,
                                                                item_name=str(x[0]),
                                                                quantiter=str(x[1]),
                                                                quantiter_price=str(x[2])))
            if test == k:
                k = k + 1
            else:
                test = k
    else:
        i = 0
        cursor.execute(
            f"select b.supplier_bill_id,b.money_payed,s.supplier_id,s.supplier_name,s.supplier_phone_number from supplier_bill b,supplier s where bill_date= '{selected_date}' and s.supplier_id=b.supplier_id ")
        for x in cursor:
            suppliers.append(supplier(id=str(x[2]),
                                      name=str(x[3]),
                                      phone_number=str(x[4])))
            suppliers[i].bill.append(supplier_bill(money_payed=str(x[1]),
                                                   bill_date=selected_date,
                                                   supplier_bill_id=str(x[0]),
                                                   supplier_id=str(x[2])))
            i = i + 1
        k = 0
        for suplierr in suppliers:
            client_bill_id=suplierr.bill[0].supplier_bill_id
            cursor.execute(f"select item_name,quantiter,price from commande_supplier where supplier_bill_id={client_bill_id}")
            test=k
            for x in cursor:
                print("test sup",k)
                k=k+1
                suplierr.bill[0].commande.append(commande_supplier(supplier_bill_id=client_bill_id,
                                                                item_name=str(x[0]),
                                                                quantiter=str(x[1]),
                                                                price=str(x[2])))
            if test==k:
                k=k+1
            else:
                test=k


    clear_widgets()
    show_dayly_bill_frame(clients,suppliers,k)
def main_frame():#this function is for creating the main frame
    #label
    welcome_label=QLabel("Welcome to your application ")
    welcome_label.setStyleSheet("font-size: 35px;"+"color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)

    # create button

    create_worker_button=create_button("Create Client bill")
    widgets["create_button"].append(create_worker_button)
    create_worker_button.clicked.connect(create_client_bill_fn)

    create_worker_button = create_button("Search for client bill")
    widgets["search_client_bill"].append(create_worker_button)
    create_worker_button.clicked.connect(search_for_client_fn)

    create_worker_button = create_button("Search for supplier bill")
    widgets["search_supplier_bill"].append(create_worker_button)
    create_worker_button.clicked.connect(search_for_supplier_fn)

    select_button = create_button("Select date")
    widgets["door_cces"].append(select_button)
    select_button.clicked.connect(lambda : select_date("all"))

    Select_date_button=create_button("Create item")
    widgets["select_button"].append(Select_date_button)
    Select_date_button.clicked.connect(create_item_fn)


    Update_worker_button=create_button("Update item ")
    widgets["update_button"].append(Update_worker_button)
    Update_worker_button.clicked.connect(update_worker)

    Update_worker_button = create_button("Create Supplier bill ")
    widgets["Create_supplier_bill"].append(Update_worker_button)
    Update_worker_button.clicked.connect(create_supplier_bill_fn)

    grid.addWidget(widgets["label"][-1],0,0)
    grid.addWidget(widgets["create_button"][-1],1,0)
    grid.addWidget(widgets["select_button"][-1],2,0)
    grid.addWidget(widgets["door_cces"][-1], 3, 0)
    grid.addWidget(widgets["search_client_bill"][-1], 4, 0)
    grid.addWidget(widgets["search_supplier_bill"][-1], 5, 0)
    grid.addWidget(widgets["update_button"][-1],6,0)
    grid.addWidget(widgets["Create_supplier_bill"][-1],7, 0)
def select_frame(type):
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 25px 25px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    select_date_4 = QCalendarWidget()
    select_date_4.setGridVisible(True)
    select_date_4.setStyleSheet(ch)
    widgets["calender"].append(select_date_4)
    select_date_4.clicked.connect(lambda : select_fn(select_date_4,type))

    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["calender"][-1], 1, 0)
def back_to_select(type):
    clear_widgets()
    select_frame(type)
def show_dayly_bill_frame(clients,suppliers,k):
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(lambda : back_to_select(type))
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(k + 4)
    tableWidget.setColumnCount(6)
    tableWidget.setItem(0, 0, QTableWidgetItem("Phone number"))
    tableWidget.setItem(0, 1, QTableWidgetItem("client full name"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Item name"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Payment"))
    tableWidget.setItem(0, 5, QTableWidgetItem("Date"))

    i = 0
    print(k)
    if len(clients)>0:
        for clientt in clients :
            print("test")
            print(clientt.phone_number)
            tableWidget.setItem(i+1, 0, QTableWidgetItem(clientt.phone_number))
            tableWidget.setItem(i+1, 1, QTableWidgetItem(clientt.full_name))
            for x in clientt.bill[0].commande:
                i=i+1
                tableWidget.setItem(i, 2, QTableWidgetItem(str(float(x.quantiter))))
                tableWidget.setItem(i, 3, QTableWidgetItem(x.item_name))
            print(i)
            if i==0:
                i=i+1
            tableWidget.setItem(i, 5, QTableWidgetItem(clientt.bill[0].client_bill_date))
            tableWidget.setItem(i, 4, QTableWidgetItem(money(clientt.bill[0].money_payed)))
        i=i+1
    else:
        i=1
    if len(suppliers)>0:
        for supplierr in suppliers :
            tableWidget.setItem(i, 0, QTableWidgetItem(supplierr.phone_number))
            tableWidget.setItem(i, 1, QTableWidgetItem(supplierr.name))
            print(i,"date")
            for x in supplierr.bill[0].commande:
                tableWidget.setItem(i, 2, QTableWidgetItem(str(int(float(x.quantiter)))))
                tableWidget.setItem(i, 3, QTableWidgetItem(x.item_name))
                i=i+1
            print(i,"payment")
            if i-1==0:
                i=i+1
            tableWidget.setItem(i-1, 5, QTableWidgetItem(supplierr.bill[0].bill_date))
            tableWidget.setItem(i-1, 4, QTableWidgetItem(money(supplierr.bill[0].money_payed)))

    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    widgets["table"].append(tableWidget)

    grid.addWidget(widgets["table"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)
def declare_case_frame():
    clear_widgets()
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    price_label = QLabel("case quantiter: ")
    price_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(price_label)

    item_label = QLabel("item name : ")
    item_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["label"].append(item_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)

    item_entry = QLineEdit()
    item_entry.setObjectName("item_entry")
    item_entry.setStyleSheet(ch)
    widgets["id_entry"].append(item_entry)

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_item_stock_2(item_entry, stock_entry))

    grid.addWidget(widgets["label"][-1], 0, 0)
    grid.addWidget(widgets["id_entry"][-1], 0, 1)
    grid.addWidget(widgets["stock_label"][-1], 1, 0)
    grid.addWidget(widgets["stock_entry"][-1], 1, 1)
    grid.addWidget(widgets["confirm"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 3, 0)


def update_frame():#this function is for creating update frame
    update_acces=create_button("Update price ")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(update_price_fn)

    update_image=create_button("Update stock ")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(update_stock_fn)

    declace_case=create_button("Declare case ")
    widgets["door_cces"].append(declace_case)
    declace_case.clicked.connect(declare_case_frame)

    back=create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 0, 0)
    grid.addWidget(widgets["update_image"][-1], 1, 0)
    grid.addWidget(widgets["door_cces"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1],3,0)
def search_for_supplier_frame():
    update_acces = create_button("Search with full name ")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(lambda :search_name_fn("Full name"))

    update_image = create_button("Search with ID ")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(lambda :search_name_fn("Cin"))

    phone_label = create_button("Search with phone number ")
    widgets["phone_label"].append(phone_label)
    phone_label.clicked.connect(lambda: search_name_fn("Phone number"))

    select_date_2=create_button("Select Date ")
    widgets["select_button"].append(select_date_2)
    select_date_2.clicked.connect(lambda: select_date("supplier"))


    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 0, 0)
    grid.addWidget(widgets["update_image"][-1], 1, 0)
    grid.addWidget(widgets["phone_label"][-1], 2, 0)
    grid.addWidget(widgets["select_button"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 4, 0)
def search_for_client_frame():
    update_acces = create_button("Search with full name ")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(lambda :search_full_name_fn("Full name"))

    update_image = create_button("Search with CIN ")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(lambda :search_full_name_fn("Cin"))

    phone_label = create_button("Search with phone number ")
    widgets["phone_label"].append(phone_label)
    phone_label.clicked.connect(lambda: search_full_name_fn("Phone number"))

    phone_label = create_button("Search with filters ")
    widgets["search_client_bill"].append(phone_label)
    phone_label.clicked.connect(search_with_filter_fn)

    select_date_2 = create_button("Select Date ")
    widgets["select_button"].append(select_date_2)
    select_date_2.clicked.connect(lambda: select_date("client"))

    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 0, 0)
    grid.addWidget(widgets["update_image"][-1], 1, 0)
    grid.addWidget(widgets["phone_label"][-1], 2, 0)
    grid.addWidget(widgets["search_client_bill"][-1], 3, 0)
    grid.addWidget(widgets["select_button"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 5, 0)
def update_price_frame():#this function is for creating update full name frame
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    price_label=QLabel("new price: ")
    price_label.setStyleSheet("font-size: 30px;"+"color:'#5B2A86'")
    widgets["price_label"].append(price_label)

    item_label=QLabel("item name : ")
    item_label.setStyleSheet("font-size: 30px;"+"color:'#5B2A86'")
    widgets["label"].append(item_label)

    price_entry=QLineEdit()
    price_entry.setObjectName("price_entry")
    price_entry.setStyleSheet(ch)
    widgets["price_entry"].append(price_entry)

    item_entry = QLineEdit()
    item_entry.setObjectName("item_entry")
    item_entry.setStyleSheet(ch)
    widgets["id_entry"].append(item_entry)

    conferm=create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda : confirm_item_price(item_entry,price_entry))

    grid.addWidget(widgets["label"][-1], 0, 0)
    grid.addWidget(widgets["id_entry"][-1], 0, 1)
    grid.addWidget(widgets["price_label"][-1], 1, 0)
    grid.addWidget(widgets["price_entry"][-1], 1, 1)
    grid.addWidget(widgets["confirm"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 3, 0)
def search_filter_date(all_client,table):
    for clientt in all_client:
        cin = clientt.cin
        cursor.execute(f"select money_payed,client_bill_id,client_bill_date from client_bill where cin={cin} order by client_bill_date")
        l = []
        money_given = 0
        last_date=""
        for x in cursor:
            l.append(f"select quantiter_price from commande_client where client_bill_id={x[1]}")
            money_given = money_given + int(x[0])
            last_date=str(x[2])
        clientt.last_bill_date=last_date
        total = 0
        for ch in l:
            cursor.execute(ch)
            for x in cursor:
                total = total + int(x[0])
        clientt.total_money = total
        clientt.money_given = money_given
        clientt.rest = total - money_given
    all_client.sort(key=lambda x: datetime.strptime(x.last_bill_date, "%Y-%m-%d"))
    i = 0
    table.setColumnCount(7)
    table.setItem(i, 3, QTableWidgetItem("Total"))
    table.setItem(i, 4, QTableWidgetItem("Money Payed"))
    table.setItem(i, 5, QTableWidgetItem("Rest"))
    table.setItem(i, 6, QTableWidgetItem("Last bill date"))
    for clientt in all_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        table.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
        table.setItem(i, 3, QTableWidgetItem(money(str(clientt.total_money))))
        table.setItem(i, 4, QTableWidgetItem(money(str(clientt.money_given))))
        table.setItem(i, 5, QTableWidgetItem(money(str(clientt.rest))))
        table.setItem(i, 6, QTableWidgetItem(str(clientt.last_bill_date)))
    table.resizeColumnsToContents()
def search_filter_money_rest(all_client, table):
    for clientt in all_client:
        cin=clientt.cin
        cursor.execute(f"select money_payed,client_bill_id from client_bill where cin={cin}")
        l=[]
        money_given=0
        for x in cursor:
            l.append(f"select quantiter_price from commande_client where client_bill_id={x[1]}")
            money_given=money_given+int(x[0])
        total=0
        for ch in l:
            cursor.execute(ch)
            for x in cursor:
                total=total+int(x[0])
        clientt.total_money=total
        clientt.money_given=money_given
        clientt.rest=total-money_given
    all_client.sort(key=lambda x:x.rest,reverse=True)
    i=0
    table.setColumnCount(6)
    table.setItem(i, 3, QTableWidgetItem("Total"))
    table.setItem(i, 4, QTableWidgetItem("Money Payed"))
    table.setItem(i, 5, QTableWidgetItem("Rest"))
    for clientt in all_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        table.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
        table.setItem(i, 3, QTableWidgetItem(money(str(clientt.total_money))))
        table.setItem(i, 4, QTableWidgetItem(money(str(clientt.money_given))))
        table.setItem(i, 5, QTableWidgetItem(money(str(clientt.rest))))
    table.resizeColumnsToContents()
def search_with_filter_fn():
    clear_widgets()
    search_with_filter()

def search_with_filter():
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(search_for_client_fn)

    all_client = client.create_clients()

    tableWidget = QTableWidget()

    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("client cin"))
    tableWidget.setItem(0, 1, QTableWidgetItem("client name"))
    tableWidget.setItem(0, 2, QTableWidgetItem("client phone number"))
    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1600)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.doubleClicked.connect(lambda: select_client_profile(all_client, lil, "filter"))
    widgets["table"].append(tableWidget)
    lil=[tableWidget]
    filter_money = create_button("Money rest")
    widgets["confirm"].append(filter_money)
    filter_money.clicked.connect(lambda: search_filter_money_rest(all_client, tableWidget))

    filter_date = create_button("date ")
    widgets["money_entry"].append(filter_date)
    filter_date.clicked.connect(lambda: search_filter_date(all_client, tableWidget))

    grid.addWidget(widgets["table"][-1], 0, 0)
    grid.addWidget(widgets["money_entry"][-1], 1, 0)
    grid.addWidget(widgets["confirm"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 3, 0)
def  client_bills_frame(all_bills,all_commande,type):
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    if type!="filter":
      back.clicked.connect(lambda : search_full_name_fn(type))
    else:
      back.clicked.connect(search_with_filter_fn)
    nbr_rows=0
    for x in all_commande:
        nbr_rows=nbr_rows+len(x)
    nbr_rows=nbr_rows+len(all_commande)
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(nbr_rows + 4)
    tableWidget.setColumnCount(6)
    tableWidget.setItem(0, 0, QTableWidgetItem("Monton"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Price_for_unit"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Item"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Payment"))
    tableWidget.setItem(0, 5, QTableWidgetItem("Date"))

    i = 0
    j=0
    total=0
    all_money_payed=0
    for commande in all_commande:
        for x in commande:
            i=i+1
            tableWidget.setItem(i, 5, QTableWidgetItem(str(all_bills[j].client_bill_date)))
            tableWidget.setItem(i, 0, QTableWidgetItem(money(str(x.quantiter_price))))
            if int(x.quantiter_price)>0:
               item_price=int(float(x.quantiter_price)/float(x.quantiter))
            else:
                item_price=0

            tableWidget.setItem(i, 1, QTableWidgetItem(money(str(item_price))))
            tableWidget.setItem(i, 2, QTableWidgetItem(str(x.item_name)))
            tableWidget.setItem(i, 3, QTableWidgetItem(str(x.quantiter)))
            total=total+int(x.quantiter_price)
        tableWidget.setItem(i+1, 4, QTableWidgetItem(money(str(all_bills[j].money_payed))))
        tableWidget.setItem(i+1, 5, QTableWidgetItem(str(all_bills[j].client_bill_date)))
        all_money_payed=all_money_payed+int(all_bills[j].money_payed)
        i=i+1
        j=j+1
    tableWidget.setItem(i+1, 1, QTableWidgetItem("Total"))
    tableWidget.setItem(i+2, 1, QTableWidgetItem("Money payed"))
    tableWidget.setItem(i+3, 1, QTableWidgetItem("Rest"))

    tableWidget.setItem(i+1, 2, QTableWidgetItem(money(str(total))))
    tableWidget.setItem(i+2, 2, QTableWidgetItem(money(str(all_money_payed))))
    tableWidget.setItem(i+3, 2, QTableWidgetItem(money(str(total-all_money_payed))))

    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    widgets["table"].append(tableWidget)

    grid.addWidget(widgets["table"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)
def  supplier_bills_frame(all_bills,all_commande,type):
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(lambda : search_name_fn(type))
    nbr_rows=0
    for x in all_commande:
        nbr_rows=nbr_rows+len(x)
    nbr_rows=nbr_rows+len(all_commande)
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(nbr_rows + 4)
    tableWidget.setColumnCount(5)
    tableWidget.setItem(0, 0, QTableWidgetItem("Monton "))
    tableWidget.setItem(0, 1, QTableWidgetItem("Item"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Payment"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Date"))

    i = 0
    j=0
    total=0
    all_money_payed=0
    for commande in all_commande:
        for x in commande:
            i=i+1
            tableWidget.setItem(i, 4, QTableWidgetItem(str(all_bills[j].bill_date)))
            tableWidget.setItem(i, 0, QTableWidgetItem(money(str(x.price))))
            tableWidget.setItem(i, 1, QTableWidgetItem(str(x.item_name)))
            tableWidget.setItem(i, 2, QTableWidgetItem(str(x.quantiter)))
            total=total+int(x.price)
        tableWidget.setItem(i+1, 3, QTableWidgetItem(money(str(all_bills[j].money_payed))))
        tableWidget.setItem(i+1, 4, QTableWidgetItem(str(all_bills[j].bill_date)))
        all_money_payed=all_money_payed+int(all_bills[j].money_payed)
        i=i+1
        j=j+1
    tableWidget.setItem(i+1, 1, QTableWidgetItem("Total"))
    tableWidget.setItem(i+2, 1, QTableWidgetItem("Money payed"))
    tableWidget.setItem(i+3, 1, QTableWidgetItem("Rest"))

    tableWidget.setItem(i+1, 2, QTableWidgetItem(money(str(total))))
    tableWidget.setItem(i+2, 2, QTableWidgetItem(money(str(all_money_payed))))
    tableWidget.setItem(i+3, 2, QTableWidgetItem(money(str(total-all_money_payed))))




    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    widgets["table"].append(tableWidget)

    grid.addWidget(widgets["table"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)

def update_stock_frame():#this function is for creating update full name frame
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    price_label = QLabel("New stock: ")
    price_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(price_label)

    item_label = QLabel("item name : ")
    item_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["label"].append(item_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)

    item_entry = QLineEdit()
    item_entry.setObjectName("item_entry")
    item_entry.setStyleSheet(ch)
    widgets["id_entry"].append(item_entry)

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_item_stock(item_entry, stock_entry))

    grid.addWidget(widgets["label"][-1], 0, 0)
    grid.addWidget(widgets["id_entry"][-1], 0, 1)
    grid.addWidget(widgets["stock_label"][-1], 1, 0)
    grid.addWidget(widgets["stock_entry"][-1], 1, 1)
    grid.addWidget(widgets["confirm"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 3, 0)
def search_full_name_fn(type):
    clear_widgets()
    search_full_name_frame(type)
def search_name_fn(type):
    clear_widgets()
    search_name_frame(type)
def create_client_bill_frame():
    welcome_label = QLabel("Create New bill " )
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)

    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 33px;" + "color:'#5B2A86' ;" + "padding: 20px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)



    cin_entry = QLineEdit()
    cin_entry.setObjectName("cin_entry")
    cin_entry.setStyleSheet(ch)
    cin_entry.setText("CIN...")
    widgets["cin_entry"].append(cin_entry)

    welcome_label=QLabel("total :  rest : ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)



    full_name_entry = QLineEdit()
    full_name_entry.setObjectName("full_name_entry")
    full_name_entry.setStyleSheet(ch)
    full_name_entry.setText("Full name...")
    widgets["full_name"].append(full_name_entry)

    phone_entry = QLineEdit()
    phone_entry.setObjectName("phone_entry")
    phone_entry.setStyleSheet(ch)
    phone_entry.setText("Phone number...")
    widgets["phone_entry"].append(phone_entry)

    money_entry = QLineEdit()
    money_entry.setObjectName("mpney_entry")
    money_entry.setStyleSheet(ch)
    money_entry.setText("money payed...")
    widgets["money_entry"].append(money_entry)

    all_items = items.create_items()

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_create_client_bill(full_name_entry,cin_entry,phone_entry,select_date,tableWidget,all_items,money_entry))




    select_date = QCalendarWidget()
    select_date.setGridVisible(True)
    select_date.setStyleSheet(ch)
    widgets["calender"].append(select_date)

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_items)+1)
    tableWidget.setColumnCount(4)
    tableWidget.setItem(0, 0, QTableWidgetItem("Item name"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Item price"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Item stock"))
    tableWidget.setItem(0,3,QTableWidgetItem("Item quantiter"))
    i=0
    for item in all_items:
        i=i+1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(item.item_name)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(item.item_price)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(item.item_stocks)))
        tableWidget.setItem(i, 3, QTableWidgetItem(str(0)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    #print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(870)
   # tableWidget.doubleClicked.connect(lambda :select_worker(tableWidget,users,date))
    widgets["table"].append(tableWidget)

    see_total_button = create_button("Total ")
    widgets["see_total"].append(see_total_button)
    see_total_button.clicked.connect(lambda: see_total(all_items, str(money_entry.text()), welcome_label, tableWidget))
    grid.addWidget(widgets["label"][-1], 0, 0)
    grid.addWidget(widgets["full_name"][-1], 1, 0)
    grid.addWidget(widgets["phone_entry"][-1], 1, 1)
    grid.addWidget(widgets["cin_entry"][-1], 1,2)
    grid.addWidget(widgets["table"][-1], 2, 1)
    grid.addWidget(widgets["money_entry"][-1], 3, 1)
    grid.addWidget(widgets["calender"][-1], 2, 0)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["see_total"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 4, 2)
    grid.addWidget(widgets["explain_label"][-1], 4, 1)
def see_total_2(money_payed, welcome_label, table,m):
    if money_payed == "":
        money_payed = "0"
    elif money_payed[0] == "-" or (money_payed[0] != "-" and not money_payed.isdigit()):
        if not money_payed[1:].isdigit():
            money_payed = "0"
    print(money_payed)
    total = 0

    for i in range(1,m):
            if str(table.item(i, 3).text()) != "" :
                if (str(table.item(i,3).text())[0]=="-" and str(table.item(i,3).text())[1:].isdigit() )or str(table.item(i,3).text()).isdigit() or str(table.item(i,3).text())[0].isdecimal() :
                   total=total+float(str(table.item(i, 3).text()))
    rest = total - int(money_payed)
    welcome_label.setText("total : " + money(str(int(total))) + " rest : " + money(str(int(rest))))
def create_supplier_bill_frame():
    welcome_label = QLabel("Create New Supplier Bill ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 33px;" + "color:'#5B2A86' ;" + "padding: 20px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)



    cin_entry = QLineEdit()
    cin_entry.setObjectName("cin_entry")
    cin_entry.setStyleSheet(ch)
    cin_entry.setText("Supplier ID ...")
    widgets["cin_entry"].append(cin_entry)

    welcome_label=QLabel("total :  rest : ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)

    phone_entry = QLineEdit()
    phone_entry.setObjectName("phone_entry")
    phone_entry.setStyleSheet(ch)
    phone_entry.setText("Phone number...")
    widgets["phone_entry"].append(phone_entry)

    full_name_entry = QLineEdit()
    full_name_entry.setObjectName("full_name_entry")
    full_name_entry.setStyleSheet(ch)
    full_name_entry.setText("Supplier name...")
    widgets["full_name"].append(full_name_entry)

    money_entry = QLineEdit()
    money_entry.setObjectName("mpney_entry")
    money_entry.setStyleSheet(ch)
    money_entry.setText("money payed...")
    widgets["money_entry"].append(money_entry)

    all_items = items.create_items()

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_create_supplier_bill(full_name_entry,cin_entry,phone_entry,select_date,tableWidget,all_items,money_entry))

    select_date = QCalendarWidget()
    select_date.setGridVisible(True)
    select_date.setStyleSheet(ch)
    widgets["calender"].append(select_date)

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_items)+1)
    tableWidget.setColumnCount(4)
    tableWidget.setItem(0, 0, QTableWidgetItem("Item name"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Item stock"))
    tableWidget.setItem(0,2,QTableWidgetItem("Item quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Price          "))
    i=0
    for item in all_items:
        i=i+1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(item.item_name)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(item.item_stocks)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(0)))
        tableWidget.setItem(i, 3, QTableWidgetItem("0"))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    #print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(890)
   # tableWidget.doubleClicked.connect(lambda :select_worker(tableWidget,users,date))
    widgets["table"].append(tableWidget)

    see_total_button = create_button("Total ")
    widgets["see_total"].append(see_total_button)
    see_total_button.clicked.connect(lambda: see_total_2( str(money_entry.text()), welcome_label, tableWidget,len(all_items)))

    grid.addWidget(widgets["explain_label"][-1], 0, 0)
    grid.addWidget(widgets["full_name"][-1], 1, 0)
    grid.addWidget(widgets["phone_entry"][-1], 1, 1)
    grid.addWidget(widgets["cin_entry"][-1], 1,2)
    grid.addWidget(widgets["table"][-1], 2, 1)
    grid.addWidget(widgets["money_entry"][-1], 3, 1)
    grid.addWidget(widgets["calender"][-1], 2, 0)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["see_total"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 4, 2)
    grid.addWidget(widgets["label"][-1], 4, 1)
def search_full_name_frame(type):#this function is for creating update door acces  frame

    welcome_label = QLabel("Search for Clinet ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_search_client)

    id_label = QLabel(type+" : ")
    id_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["id_label"].append(id_label)

    id_entry = QLineEdit()
    id_entry.setObjectName("id_entry")
    id_entry.setStyleSheet(ch)
    widgets["id_entry"].append(id_entry)

    all_client=client.create_clients()

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("client cin"))
    tableWidget.setItem(0, 1, QTableWidgetItem("client name"))
    tableWidget.setItem(0, 2, QTableWidgetItem("client phone number"))
    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1000)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.doubleClicked.connect(lambda :select_client_profile(all_client,lil,type))
    widgets["table"].append(tableWidget)


    conferm = create_button("search")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: search_name(id_entry,all_client,lil,type))
    lil = [tableWidget]
    grid.addWidget(widgets["explain_label"][-1], 0, 0)
    grid.addWidget(widgets["id_label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["table"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 4, 0)
def search_name_frame(type):#this function is for creating update door acces  frame

    welcome_label = QLabel("Search for supplier ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 15px 15px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_search_supplier)

    id_label = QLabel(type+" : ")
    id_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["id_label"].append(id_label)

    id_entry = QLineEdit()
    id_entry.setObjectName("id_entry")
    id_entry.setStyleSheet(ch)
    widgets["id_entry"].append(id_entry)

    all_client=supplier.create_supplier()

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("Supplier ID"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Supplier name"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Supplier phone number"))
    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.id)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.name)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(clientt.phone_number)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1000)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.doubleClicked.connect(lambda :select_supplier_profile(all_client,tableWidget,type))
    widgets["table"].append(tableWidget)


    conferm = create_button("search")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: search_name_supplier(id_entry,all_client,tableWidget,type))

    grid.addWidget(widgets["explain_label"][-1],0,1)
    grid.addWidget(widgets["id_label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["table"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 4, 0)

def create_item_frame():#this function is for creating worker  frame
    welcome_label = QLabel("Create New item ")
    welcome_label.setStyleSheet("font-size: 35px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 4px solid '#5B2A86';" + "border-radius: 45px;" + "font-size: 35px;" + "color:'#5B2A86' ;" + "padding: 25px 0;" + "margin: 25px 25px ;"
    back = create_button("Back")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    full_name_label = QLabel("Item name : ")
    full_name_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["label"].append(full_name_label)

    name_entry = QLineEdit()
    name_entry.setObjectName("name_entry")
    name_entry.setStyleSheet(ch)
    widgets["full_name"].append(name_entry)

    price_label = QLabel("Item price : ")
    price_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["price_label"].append(price_label)

    price_entry = QLineEdit()
    price_entry.setObjectName("price_entry")
    price_entry.setStyleSheet(ch)
    widgets["price_entry"].append(price_entry)

    stock_label = QLabel("Item stock : ")
    stock_label.setStyleSheet("font-size: 30px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(stock_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)


    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_create_item(name_entry,price_entry,stock_entry))

    grid.addWidget(widgets["explain_label"][-1], 0, 1)
    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["full_name"][-1], 1, 1)
    grid.addWidget(widgets["price_label"][-1], 2, 0)
    grid.addWidget(widgets["price_entry"][-1], 2, 1)
    grid.addWidget(widgets["stock_label"][-1], 3, 0)
    grid.addWidget(widgets["stock_entry"][-1], 3, 1)
    grid.addWidget(widgets["confirm"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 5, 0)






main_frame()

window.setLayout(grid)
window.show()
sys.exit(app.exec())


