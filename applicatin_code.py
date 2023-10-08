import sys
import webbrowser
from datetime import date
import traceback
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton,  QWidget, QGridLayout ,QLineEdit ,QMessageBox,QCalendarWidget,QTableWidget,QTableWidgetItem,QAbstractItemView,QComboBox,QListView,QScrollArea,QDialog,QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QFont
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re


def make_windows_friendly_filename(input_string):
    # Define a regex pattern to match characters not allowed in Windows file names
    invalid_chars_pattern = r'[\/:*?"<>|]'

    # Replace invalid characters with spaces
    windows_friendly_filename = re.sub(invalid_chars_pattern, ' ', input_string)

    return windows_friendly_filename
cnx = mysql.connector.connect(user='root', password='Ya3an3anter', host='127.0.0.1')

# Check if a database exists
cursor = cnx.cursor()
cursor.execute("SHOW DATABASES LIKE 'build'")
result = cursor.fetchone()
font_size="25"
padding_size="10"
if result:
  print("The database exists.")
  try:
      connection = mysql.connector.connect(host='127.0.0.1',
                                           port='3306',
                                           database='build',
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
          cursor.execute("SELECT * FROM build.items")
  except Error as e:
      print("Error while connecting to MySQL", e)
# else:
#   print("The database does not exist.")
#   cursor.execute("CREATE DATABASE mydb")
#   try:
#       connection = mysql.connector.connect(host='127.0.0.1',
#                                            port='3306',
#                                            database='application',
#                                            user='root',
#                                            password="Ya3an3anter",
#                                            auth_plugin='mysql_native_password')
#       if connection.is_connected():
#           db_Info = connection.get_server_info()
#           print("Connected to MySQL Server version ", db_Info)
#           cursor = connection.cursor(buffered=True)
#           # cursor = connection.cursor()
#           cursor.execute("select database();")
#           record = cursor.fetchone()
#           print("You're connected to database: ", record)
#           cursor.execute("create table items(item_name  varchar(100) not null primary key, item_stock float(10, 3) not null,item_price int not null)")
#           cursor.execute("create table supplier ( supplier_id           int          not null primary key,supplier_name         varchar(100) not null )")
#           cursor.execute("create table supplier_bill (  supplier_bill_id int auto_increment primary key, bill_date    date null, supplier_id      int  not null, money_payed  int  not null, constraint supplier_bill_ibfk_1  foreign key (supplier_id) references supplier (supplier_id))")
#           cursor.execute("create table commande_supplier ( quantiter        float(8, 3)  not null,supplier_bill_id int          not null, price            int          not null, item_name       varchar(100) not null, primary key (supplier_bill_id, item_name),  constraint commande_supplier_ibfk_1 foreign key (supplier_bill_id) references supplier_bill (supplier_bill_id), constraint commande_supplier_ibfk_2 foreign key (item_name) references items (item_name))")
#           cursor.execute("create index supplier_id on supplier_bill (supplier_id)")
#           cursor.execute("create index item_name on commande_supplier (item_name)")
#           cursor.execute("create index supplier_id on supplier_bill (supplier_id)")
#           cursor.execute("create table the_client ( cin   int          not null primary key,client_full_name    varchar(150) not null)")
#           cursor.execute("create table client_bill( client_bill_id   int auto_increment primary key,  client_bill_date date not null,  cin   int  not null, money_payed      int  not null, constraint client_bill_ibfk_1 foreign key (cin) references the_client (cin))")
#           cursor.execute("create index cin on client_bill (cin)")
#           cursor.execute("create table commande_client(quantiter float(8, 3)  not null, quantiter_price int   not null, client_bill_id  int   not null, item_name   varchar(100) not null, primary key (client_bill_id, item_name), constraint commande_client_ibfk_1 foreign key (client_bill_id) references client_bill (client_bill_id),  constraint commande_client_ibfk_2)  foreign key (item_name) references items (item_name))")
#           cursor.execute("create index item_name on commande_client (item_name)")
#
#   except Error as e:
#       print("Error while connecting to MySQL",e)





# class CustomDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle('Confirm bill ')
#         self.setGeometry(100, 100, 1000, 500)  #
#
#         scroll_area = QScrollArea(self)
#         scroll_area.setWidgetResizable(True)
#         self.text_edit = QLabel()
#
#         # Set the font size to 15
#         font = QFont()
#         font.setPointSize(20)
#         self.text_edit.setFont(font)
#
#         scroll_area.setWidget(self.text_edit)
#
#         layout = QVBoxLayout()
#         layout.addWidget(scroll_area)
#
#
#
#         button_layout = QVBoxLayout()
#         confirm_button = QPushButton('Confirm', self)
#         confirm_button.setFont(font)
#         confirm_button.clicked.connect(self.accept)
#
#         cancel_button = QPushButton('Cancel', self)
#         cancel_button.setFont(font)
#         cancel_button.clicked.connect(self.reject)
#
#         button_layout.addWidget(confirm_button)
#         button_layout.addWidget(cancel_button)
#
#         layout.addLayout(button_layout)
#         self.setLayout(layout)
#
#     def setText(self, text):
#         self.text_edit.setText(text)

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Confirm bill')
        self.setGeometry(75, 75, 1100, 600)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.text_edit = QLabel()

        # Set the font size to 20
        font = QFont()
        font.setPointSize(20)
        self.text_edit.setFont(font)

        scroll_area.setWidget(self.text_edit)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Nom de l'article"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Prix unitaire"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Quantité"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem("Prix total"))
        self.tableWidget.setStyleSheet(ch)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setFixedHeight(400)
        self.tableWidget.hide()

        button_layout = QVBoxLayout()
        confirm_button = QPushButton('Confirm', self)
        confirm_button.setFont(font)
        confirm_button.clicked.connect(self.accept)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.setFont(font)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        layout.addWidget(self.tableWidget)  # Add the table to the layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def setText(self, text):
        self.text_edit.setText(text)

    def set_table(self, all_items,size,type):
        self.tableWidget.show()
        self.tableWidget.setRowCount(size + 3)
        i=1
        if type!="fournisseur":
            for item in all_items:

                if float(item.item_quantiter) != 0:
                    self.tableWidget.setItem(i,0, QTableWidgetItem(item.item_name))
                    self.tableWidget.setItem(i,1, QTableWidgetItem(str(item.item_price)))
                    self.tableWidget.setItem(i,2, QTableWidgetItem(str(item.item_quantiter)))
                    self.tableWidget.setItem(i,3, QTableWidgetItem(money(str(int(float(item.item_price)*float(item.item_quantiter))))))
                    print(int(int(item.item_price)*float(item.item_quantiter)))
                    i=i+1
            total_price = int(sum(float(item.item_price) * float(item.item_quantiter) for item in all_items))
        else:
            for item in all_items:

                if float(item.item_quantiter) != 0:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(item.item_name))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(item.item_quantiter)))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(
                        money(item.price)))

                    i = i + 1
            total_price = int(sum(int(item.price) for item in all_items))
        # Example calculation for the total price, adjust as needed
        self.tableWidget.setItem(size+2, 3, QTableWidgetItem(money(str(total_price))))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setFixedHeight(400)
class Devis:
    def __init__(self,client_bill_id,client_bill_date,cin):
        self.client_devis_id=client_bill_id
        self.client_bill_date=client_bill_date
        self.cin=cin
        self.commande = []
    @classmethod
    def create_devis(cls,cin):
        cursor.execute(f"select client_devis_id,client_bill_date from client_devis where cin={cin} order by client_bill_date")
        all_bills=[]
        for x in cursor:
            all_bills.append(Devis(str(x[0]),str(x[1]),str(cin)))
        return all_bills

    @classmethod
    def delete_corrupted_devis(cls, all_bills, all_commande):
        for j, commande in enumerate(all_commande):
            if len(commande) == 0 :
                cursor.execute(f"DELETE FROM client_devis where client_devis_id={all_bills[j].client_devis_id}")
        connection.commit()
class devis_commande:
    def __init__(self,quantiter,quantiter_price,client_bill_id,item_name):
        self.quantiter=quantiter
        self.quantiter_price=quantiter_price
        self.client_devis_id=client_bill_id
        self.item_name=item_name
    @classmethod
    def create_devis_client(cls,client_bill_id):
        cursor.execute(f"delete from devis_commande where client_devis_id={client_bill_id} and quantiter=0")
        connection.commit()
        cursor.execute(f"select quantiter,quantiter_price,item_name from devis_commande where client_devis_id={client_bill_id}")
        all_commande=[]

        for x in cursor:
           all_commande.append(devis_commande(str(x[0]),str(x[1]),str(client_bill_id),str(x[2])))
        return all_commande
class bill:
    def __init__(self,client_bill_id,client_bill_date,cin,money_payed,type):
        self.client_bill_id=client_bill_id
        self.client_bill_date=client_bill_date
        self.cin=cin
        self.money_payed=money_payed
        self.money_type=type
        self.commande = []
    @classmethod
    def create_bills(cls,cin):
        cursor.execute(f"select client_bill_id,client_bill_date,money_payed,money_type from client_bill where cin={cin} order by client_bill_date")
        all_bills=[]
        for x in cursor:
            all_bills.append(bill(str(x[0]),str(x[1]),str(cin),str(x[2]),str(x[3])))
        return all_bills
    @classmethod
    def delete_corrupted_bills(cls,all_bills,all_commande):
        for j,commande in enumerate(all_commande):
            if len(commande)==0 and int(all_bills[j].money_payed)==0:
                cursor.execute(f"DELETE FROM CLIENT_BILL where client_bill_id={all_bills[j].client_bill_id}")
        connection.commit()
class Remise:
    def __init__(self,id,quantiter,date,cin):
        self.id=id
        self.quantiter=quantiter
        self.date=date
        self.cin=cin

    @classmethod
    def get_remize(cls,cin):
        print(cin)
        cursor.execute(f"select remize_id,remize_quantiter,remize_date from remize where cin={cin} order by remize_date")
        print(f"select remize_id,remize_quantiter,remize_date from remize where cin={cin} order by remize.remize_date ; ")
        all_remize=[]

        for x in cursor:
            all_remize.append(Remise(str(x[0]),str(x[1]),str(x[2]),str(cin)))
            print(x[1])

        print(len(all_remize))
        print(all_remize)
        return all_remize



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
    def __init__(self,item_name,item_price,item_stocks,item_quantiter,id):
        self.item_id=id
        self.item_name=item_name
        self.item_price=item_price
        self.item_stocks=item_stocks
        self.item_quantiter=item_quantiter
        self.price=None
        self.id=None
    def create_item(self):
        if self.item_name!="" and  self.item_price.isdigit() and  self.item_stocks.isdigit():
            cursor.execute(f"select count(*) from items where item_name='{self.item_name}'")
            for x in cursor:
                k=x[0]
            if k==1:
                return False
            else :
                print(f"insert into items (item_name,item_stock,item_prix) values ('{self.item_name}',{str(self.item_stocks)},{str(self.item_price)})")
                cursor.execute(f"insert into items (item_name,item_stock,item_price) values ('{self.item_name}',{str(self.item_stocks)},{str(self.item_price)})")
                connection.commit()
                return True
        else:
            return False
    @classmethod
    def create_dict_items(cls):
        all_dict_items={}

        cursor.execute("select item_name,item_price,item_stock,item_id from items ")
        for x in cursor:
            all_dict_items[str(x[0])]=items(str(x[0]),str(x[1]),str(x[2]),0,str(x[3]))

        return all_dict_items


    @classmethod
    def create_items(cls):
        l=[]
        cursor.execute("select item_name,item_price,item_stock,item_id from items ")
        for x in cursor:
            l.append(items (str(x[0]),
                              str(x[1]),
                                str(x[2]),
                                0,str(x[3])))

        return l
    @classmethod
    def get_items_names(cls):
        l=[]
        cursor.execute("select item_name from items ")
        for x in cursor:
            l.append(x[0])

        return l


class client :
    def __init__(self,name,phone_number,cin):
        self.full_name=name
        self.phone_number=phone_number
        self.cin=cin
        self.bill=[]
        self.devis=[]
        self.total_money=None
        self.money_given=None
        self.rest=None
        self.last_bill_date=None
    def create_clent_bill_commande(self,items,date,money_payed,money_type):
        cursor.execute(f"select count(cin) from the_client where client_full_name='{str(self.full_name)}'")
        print(money_payed,str(money_payed))
        for x in cursor:
            k=x[0]
        print("k ",k)
        if k==1:
            pass
        else:
            cursor.execute(f"insert into the_client (client_full_name,phone_number) values ('{self.full_name}','{self.phone_number}')")
            connection.commit()
        cursor.execute(f"select cin from the_client where client_full_name='{self.full_name}'")
        for x in cursor:
            self.cin=x[0]
        print(self.cin)

        query_create_bill=f"insert into client_bill (client_bill_date,cin,money_payed,money_type) values ('{date}',{self.cin},{money_payed},'{money_type}')"

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
               query_item.append(f"update items set item_stock=item_stock-{str(item.item_quantiter)}  where item_id='{item.item_id}'")
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

    def create_client_devis_commande(self,items,date):
        cursor.execute(f"select count(cin) from the_client where client_full_name='{str(self.full_name)}'")
        for x in cursor:
            k=x[0]
        print("k ",k)
        if k==1:
            pass
        else:
            print(self.full_name)
            cursor.execute(f"insert into the_client (client_full_name,phone_number) values ('{self.full_name}','{self.phone_number}')")
            connection.commit()
        cursor.execute(f"select cin from the_client where client_full_name='{self.full_name}'")
        for x in cursor:
            self.cin=x[0]
        print(self.cin)

        query_create_bill=f"insert into client_devis (client_bill_date,cin) values ('{date}',{self.cin})"

        print(query_create_bill)
        cursor.execute(query_create_bill)
        connection.commit()
        query_commande=[]
        cursor.execute(f"select client_devis_id from client_devis where client_bill_date='{date}' and cin={self.cin}")
        for x in cursor:
            client_bill_id=x[0]
        print("test 0")
        for item in items:
            cursor.execute(f"select count(*) from devis_commande where client_devis_id={client_bill_id} and item_name='{item.item_name}' ")
            for x in cursor:
                k=x[0]
            print("test 1")
            if k==0:
              if float(str(item.item_quantiter))!=0:
                    query_commande.append(f"insert into devis_commande  (quantiter,quantiter_price,client_devis_id,item_name) values ({item.item_quantiter},{int(float(item.item_quantiter)*int(item.item_price))},{client_bill_id},'{item.item_name}') ")
            else:
                print("error happen")

        for i in range(len(query_commande)):
            cursor.execute(query_commande[i])
            connection.commit()
        print("finat test")
        return items
    @classmethod
    def create_clients(cls):
        cursor.execute("select cin,client_full_name,phone_number from the_client")
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
        cursor.execute(f"select count(*) from supplier where phone_number={str(self.phone_number)}")
        print(money_payed, str(money_payed))
        print("date " ,date)
        for x in cursor:
            k = x[0]
        if k == 1:
            pass
        else:
            cursor.execute( f"insert into supplier (supplier_name,phone_number) values ('{self.name}','{self.phone_number}')")
            connection.commit()
        cursor.execute(f"select  supplier_id from supplier where phone_number='{self.phone_number}'")
        for x in cursor:
            self.id=str(x[0])

        query_create_bill = f"insert into supplier_bill (bill_date,supplier_id,money_payed) values ('{date}',{self.id},{money_payed})"
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
              query_item.append(f"update items set item_stock=item_stock+{str(item.item_quantiter)}  where item_id='{item.item_id}'")
              item.item_stocks = str(float(item.item_stocks) +float(item.item_quantiter))
        for i in range(len(query_item)):
            cursor.execute(query_commande[i])
            cursor.execute(query_item[i])
            connection.commit()

    @classmethod
    def create_supplier(cls):
            cursor.execute("select supplier_id,phone_number,supplier_name from supplier")
            all_supplier = []
            for clientt in cursor:
                all_supplier.append(supplier(phone_number=str(clientt[1]),name= str(clientt[2]),id= str(clientt[0])))
            return all_supplier

def money(ch):
    p=len(ch)
    if ch[0]!="-":
        while p>3:
            print(p)
            ch=ch[0:p-3]+","+ch[p-3:len(ch)]
            p=p-3
        return ch
    else:
        chh=ch[1:]
        p=len(chh)
        while p>3:
            print(p)
            chh=chh[0:p-3]+","+chh[p-3:len(chh)]
            p=p-3
        return "-"+chh

def total_remize_speciale(all_remize,all_bills):
    first_bill_date=all_bills[0].client_bill_date
    last_bill_date=all_bills[-1].client_bill_date
    total=0


    date1 = datetime.strptime(first_bill_date, '%Y-%m-%d')
    date2 = datetime.strptime(last_bill_date, '%Y-%m-%d')


    for remise in all_remize:
        if date1<= datetime.strptime(remise.date, '%Y-%m-%d'):
            if date2>= datetime.strptime(remise.date, '%Y-%m-%d'):
                total=total+int(remise.quantiter)
            else:
                return total
    return total





def generate_total_bill(filename,bill_id,client_name,phone_number,all_items_total,total,remize):
    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []


    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name

    header_text = f"<font size=15> Facture N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data
    total_price = 0

    table_data = [["Nom de l'article", "Quantité", "Prix total"]]


    for key in all_items_total:

        table_data.append(
                   [str(key), str(all_items_total[key]["quantiter"]), money(str(all_items_total[key]["quantiter_price"]))]  )
        total_price=total_price+all_items_total[key]["quantiter_price"]
    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table


    # Calculate totals
    print(remize)
    if remize == 0:
        total_row = ["",f"Total: {money(str(total_price))}",  f"Total payé: {money(str(total))}"]
        table_data.append(total_row)

        # Remaining amount row
        remaining_row = ["", "", f"Reste à payer: {money(str(total_price - total))}"]
        table_data.append(remaining_row)
    else:
        total_row = ["",f"Total: {money(str(total_price))}",  f"Total payé: {money(str(total))}"]
        table_data.append(total_row)

        # Remaining amount row
        remaining_row = ["",f"Remise exceptionnelle : {money(str(remize))}",
                         f"Reste à payer: {money(str(total_price - (total + remize)))}"]
        table_data.append(remaining_row)
    # Total row

    # total_row = ["", f"Total: {money(str(total_price))}", f"Total payé: {money(str(total))}"]
    # table_data.append(total_row)
    #
    # # Remaining amount row
    # remaining_row = ["", f"Reste à payer: {money(str(total_price-total)) }", ""]
    # table_data.append(remaining_row)

    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )

    no_grid_style = TableStyle(
            [
                ("GRID", (0, -1), (-3, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
            ]
        )

    table_width = doc.width * 0.91  # Adjust as needed

    col_widths = [table_width * 0.3, table_width * 0.35, table_width * 0.3]

    table = Table(table_data, colWidths=col_widths)

    table.setStyle(table_style)
    table.setStyle(
        no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)

    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)


def generate_bill(filename,bill_id,client_name,phone_number,all_bills,all_commande,type,all_remize):
    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []

    table_width = doc.width * 0.88  # Adjust as needed
    if len(all_remize)==0:
        remize=0
    else:
        remize=total_remize_speciale(all_remize,all_bills)

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name
    if type=="bill":
        header_text = f"<font size=15> Facture détaillée N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    else:
        header_text = f"<font size=15> {type} N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data
    j = 0
    total = 0
    all_money_payed = 0
    if type=='bill':
        table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date", "Montant payé"]]

    else:
        table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date"]]

    for commande in all_commande:
        for x in commande:
            if int(x.quantiter_price)>0:
               item_price=int(float(x.quantiter_price)/float(x.quantiter))
               if type=="bill":
                   table_data.append(
                       [str(x.item_name), str(x.quantiter), money(str(item_price)), money(str(x.quantiter_price)),
                        str(all_bills[j].client_bill_date), ""]

                   )
               else:
                   table_data.append(
                       [str(x.item_name), str(x.quantiter), money(str(item_price)), money(str(x.quantiter_price)),
                        str(all_bills[j].client_bill_date)]
                   )


            else:
                item_price=int(float(x.quantiter_price)/float(x.quantiter))
                table_data.append(
                       [str(x.item_name), "reteur "+str(float(float(x.quantiter)*-1)), money(str(item_price)), money(str(x.quantiter_price)), str(all_bills[j].client_bill_date), ""]
                     )
            total = total + int(x.quantiter_price)
        if type=='bill':
            table_data.append(
                ["", "", "", "",
                 str(all_bills[j].client_bill_date),money(str(all_bills[j].money_payed)) ]
            )
            all_money_payed = all_money_payed + int(all_bills[j].money_payed)
        j = j + 1
    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table


    # Calculate totals

    print(remize)
    # Total row
    if type=="bill":
        if remize == 0:
            total_row = ["", "", "", f"Total: {money(str(total))}", "", f"Total payé: {money(str(all_money_payed))}"]
            table_data.append(total_row)
            col_widths = [table_width * 0.20,table_width * 0.15,table_width * 0.15, table_width * 0.25, table_width * 0.12,table_width * 0.25]
            # Remaining amount row
            remaining_row = ["", "", "", "","",f"Reste à payer: {money(str(total-all_money_payed)) }"]
            table_data.append(remaining_row)
        else:
            total_row = ["", "", "", f"Total: {money(str(total))}", "", f"Total payé: {money(str(all_money_payed))}"]
            table_data.append(total_row)
            col_widths = [table_width * 0.20, table_width * 0.15, table_width * 0.10, table_width * 0.35,
                          table_width * 0.12, table_width * 0.25]
            print("test wtf")
            # Remaining amount row
            remaining_row = ["", "", "", f"Remise exceptionnelle : {money(str(remize))}", "", f"Reste à payer: {money(str(total - (all_money_payed+remize)))}"]
            table_data.append(remaining_row)
    else:
        total_row = ["", "", "", f"Total: {money(str(total))}", "",]
        col_widths = [table_width * 0.25,table_width * 0.15,table_width * 0.15, table_width * 0.3, table_width * 0.15]

        table_data.append(total_row)

    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )
    if type=="bill":
        no_grid_style = TableStyle(
            [
                ("GRID", (0, -2), (-4, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
            ]
        )
    else:
        no_grid_style = TableStyle(
            [
                ("GRID", (0, -1), (-3, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
            ]
        )

    table_width = doc.width * 0.91  # Adjust as needed



    table = Table(table_data, colWidths=col_widths)
    table.setStyle(table_style)
    table.setStyle(
        no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)

    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
    if type=="devis":
        cursor.execute("UPDATE global_variable set devis_code=devis_code+1 ")
        connection.commit()
        imprimer(filename)
def generate_bill_only_take(filename,bill_id,client_name,phone_number,all_bills,all_commande):
    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name

    header_text = f"<font size=15>Facture de sortie  N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data
    j = 0
    total = 0
    all_money_payed = 0

    table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date"]]

    for commande in all_commande:
        for x in commande:
            if int(x.quantiter_price)>0:
               item_price=int(float(x.quantiter_price)/float(x.quantiter))

               table_data.append(
                       [str(x.item_name), str(x.quantiter), money(str(item_price)), money(str(x.quantiter_price)),
                        str(all_bills[j].client_bill_date)]
                   )
               total = total + int(x.quantiter_price)

        j = j + 1
    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table


    # Calculate totals


    # Total row

    total_row = ["", "", "", f"Total: {money(str(total))}", "",]
    table_data.append(total_row)

    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )


    no_grid_style = TableStyle(
        [
            ("GRID", (0, -1), (-3, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
        ]
    )

    table_width = doc.width * 0.91  # Adjust as needed
    col_widths = [table_width * 0.25, table_width * 0.15, table_width * 0.15, table_width * 0.25, table_width * 0.15]

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(table_style)
    table.setStyle(
        no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)


    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
    QMessageBox.information(None, "Success", "bill d'article créé avec succès !!")
    webbrowser.open(filename,new=2)


def add_page_numbers(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 9)
    canvas.drawString(300, 20, text)


def generate_bill_reteur(filename, bill_id, client_name, phone_number, all_bills, all_commande):

    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name
    header_text = f"<font size=15>bonde de reteur N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data
    j = 0
    total = 0
    all_money_payed = 0
    table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date"]]
    for commande in all_commande:
        for x in commande:
            if int(x.quantiter_price) < 0:
                item_price = int(float(x.quantiter_price) / float(x.quantiter))*-1

                table_data.append(
                    [str(x.item_name), str(float(float(x.quantiter)*-1)), money(str(int(int(item_price)*-1))), money(str(int(int(x.quantiter_price)*-1))),
                     str(all_bills[j].client_bill_date)]
                )
                total = total + int(int(x.quantiter_price)*-1)
        j=j+1


    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table

    # Calculate totals

    # Total row
    total_row = ["", "", "", f"Total: {money(str(total))}", ""]
    table_data.append(total_row)

    # Remaining amount row

    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )

    no_grid_style = TableStyle(
        [
            ("GRID", (0, -1), (-3, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
        ]
    )

    table_width = doc.width * 0.91  # Adjust as needed
    col_widths = [table_width * 0.25, table_width * 0.15, table_width * 0.15, table_width * 0.3, table_width * 0.15]

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(table_style)
    table.setStyle(
        no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)

    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
    cursor.execute("UPDATE global_variable set bonde_reteur=bonde_reteur+1 ")
    connection.commit()
    QMessageBox.information(None, "Success", "Bonde de reteur créer avec succes !!")
    webbrowser.open(filename, new=2)

def generate_bonde_levraison(filename,bill_id,client_name,phone_number,money_payed,date,all_items,type):
    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name
    if type=="devis":
        header_text = f"<font size=15> {type} N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    else:
        header_text = f"<font size=15>Bonde de {type} N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data

    total = 0
    if type=="sortie":
        table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date", "Montant payé"]]
    else:
        table_data = [["Nom de l'article", "Quantité", "Prix unitaire", "Prix total", "Date"]]

    for x in all_items:
        if int(x.item_quantiter)!=0:
            if type=="reteur":
                quantiter_price = int(float(x.item_quantiter) * int(x.item_price) * -1)

                table_data.append(
                    [str(x.item_name), str(int(int(x.item_quantiter) * -1)), money(str(x.item_price)),
                     money(str(quantiter_price)), str(date)]
                )
                total = total + int(quantiter_price)
            elif type=="sortie":
                quantiter_price=int(float(x.item_quantiter)*int(x.item_price))

                table_data.append(
                       [str(x.item_name), str(x.item_quantiter), money(str(x.item_price)), money(str(quantiter_price)), str(date), ""]
                     )
                total = total + int(quantiter_price)
            else:
                quantiter_price = int(float(x.item_quantiter) * int(x.item_price))

                table_data.append(
                    [str(x.item_name), str(x.item_quantiter), money(str(x.item_price)), money(str(quantiter_price)),
                     str(date)]
                )
                total = total + int(quantiter_price)
    if type == "sortie":
        table_data.append(
            ["", "", "", "",
             str(date),money(str(money_payed)) ]
        )
    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table

    table_width = doc.width * 0.91  # Adjust as needed

    # Calculate totals

    if type=="sortie":
        # Total row
        total_row = ["", "", "", f"Total: {money(str(total))}", "", f"Total payé: {money(str(money_payed))}"]
        table_data.append(total_row)
        remaining_row = ["", "", "", f"Reste à payer: {money(str(total - int(money_payed)))}", "", ""]
        table_data.append(remaining_row)
        col_widths = [table_width * 0.20,table_width * 0.15,table_width * 0.15, table_width * 0.25, table_width * 0.15,table_width*0.25]

    else:
        total_row = ["", "", "", f"Total: {money(str(total))}", ""]
        col_widths = [table_width * 0.25,table_width * 0.15,table_width * 0.15, table_width * 0.25, table_width * 0.15]

        table_data.append(total_row)


    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )
    if type=="sortie":
        no_grid_style = TableStyle(
            [
                ("GRID", (0, -2), (-4, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
            ]
        )
    else:
        no_grid_style = TableStyle(
            [
                ("GRID", (0, -1), (-3, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
            ]
        )


    table = Table(table_data, colWidths=[table_width / len(table_data[0])] * len(table_data[0]))
    table.setStyle(table_style)
    table.setStyle(
        no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)

    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
    webbrowser.open(filename, new=2)
def generate_bonde_reglemen(filename,bill_id,client_name,phone_number,all_bills):
    doc = SimpleDocTemplate(filename, pagesize=letter,leftMargin=28.35, rightMargin=28.35, topMargin=28.35, bottomMargin=28.35)
    story = []

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name
    header_text = f"<font size=15>Bonde de reglement N°: {bill_id} </font> <br/><font size=15>Client: {client_name} </font><br/> <font size=15> Tel : {phone_number} </font>"
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data

    # Calculate column widths

    total = 0

    table_data = [[ "Montant payé","Date"]]

    for x in all_bills:
       if int(x.money_payed)!=0:
                table_data.append(
                       [ money(str(x.money_payed)), str(x.client_bill_date)]
                     )
                total = total + int(x.money_payed)

    # Add item data to the table
    # for item in items:
    #     table_data.append(
    #         [item["name"], str(item["quantity"]), str(item["unit_price"]), str(item["total_price"]), "", ""]
    #     )

    # Add payment data to the table


    # Calculate totals


    # Total row
    total_row = [ f"Total payé: {money(str(total))}"," "]
    table_data.append(total_row)

    # Remaining amount row


    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last row
            ("ALIGN", (0, -1), (-1, -1), "LEFT"),  # Align the last row to the left
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -2), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add border lines to all cells
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the last row
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),  # Bold font for all rows
            ("FONTSIZE", (0, 0), (-1, -2), 14),  # Increase font size for all rows except last row
            ("BACKGROUND", (-1, 0), (-1, -1), colors.grey),  # Background color for last column header
            ("TEXTCOLOR", (-1, 0), (-1, -1), colors.whitesmoke),  # Text color for last column header
            ("ALIGN", (-1, 0), (-1, -1), "CENTER"),  # Center align the last column header and content
            ("FONTNAME", (-1, 0), (-1, -1), "Helvetica-Bold"),  # Bold font for last column header
            ("FONTSIZE", (-1, 0), (-1, -1), 16),  # Increase font size for last column header and content
            ("FONTSIZE", (0, -1), (-1, -1), 14),  # Increase font size for last row
            ("LEADING", (0, 0), (-1, -1), 18),  # Increase the row height (leading) for all rows
        ]
    )

    # Calculate column widths
    col_widths = [doc.width * 0.4, doc.width * 0.6]
    # Create the table


    # no_grid_style = TableStyle(
    #     [
    #         ("GRID", (0, -2), (-4, -1), 0, colors.white),  # Set grid line width to 0.5 (almost invisible)
    #     ]
    # )

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(table_style)
    # table.setStyle(
    #     no_grid_style)  # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)
    print("UPDATE global_variable set bonde_reglement=bonde_reglement+1 ")
    cursor.execute("UPDATE global_variable set bonde_reglement=bonde_reglement+1 ")
    connection.commit()
    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)

    QMessageBox.information(None, "Success", "Bonde de reglement créer avec succes  ")
    webbrowser.open(filename, new=2)
def see_total(all_items, money_payed, welcome_label, table):
    if money_payed == "":
        money_payed = "0"
    l = list(filter(lambda score: score.isalpha() == True, money_payed.split()))
    print(l)
    print(len(l))
    print(money_payed.split())
    m = money_payed.split()
    print(m[0].isalpha())
    if len(l) >= 1 or len(m) > 1:
        money_payed = 0

    print(money_payed)
    total = 0
    print("testing quantiter and price")
    try:
        for i in range(1, table.rowCount()):
            print("test0")
            lineEdit = table.cellWidget(i, 3)
            if isinstance(lineEdit, QLineEdit):
                print("test1")
                quantiter_text = lineEdit.text()
                print(quantiter_text)
                all_items[str(table.item(i, 0).text())].id=i
                if quantiter_text == "":
                    print("test")
                    all_items[str(table.item(i, 0).text())].item_quantiter = "0"
                elif (quantiter_text.isdecimal()):
                    all_items[str(table.item(i, 0).text())].item_quantiter = quantiter_text
                else:
                    all_items[str(table.item(i, 0).text())].item_quantiter="0"


            item_price = str(table.item(i, 1).text())
            if item_price == "" or item_price == "0":
                item_price = all_items[str(table.item(i, 0).text())].item_price
            elif item_price.isdigit():
                item_price = str(table.item(i, 1).text())
            else:
                item_price = all_items[str(table.item(i, 0).text())].item_price
            all_items[str(table.item(i, 0).text())].item_price = item_price
            # print(item.item_price, item.item_name)
    except Exception as e:
        print(e)
    all_items=list(all_items.values())
    for i, item in enumerate(all_items, start=1):
        if str(item.item_quantiter)!="0" :
            total = total + float(item.item_quantiter) * int(item.item_price)
            table.setItem(item.id, 4, QTableWidgetItem(money(str(int(float(item.item_quantiter) * int(item.item_price))))))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()

    rest = total - int(money_payed)
    welcome_label.setText("total : " + money(str(int(total))) + " remain : " + money(str(int(rest))))

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
    "back":[],
    "back_to_main":[],
    "scroll":[],
    "phone_list_view":[],
    "name_list_view":[],
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

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("GUI")

# Get the screen size
screen_width = app.desktop().screenGeometry().width()
screen_height = app.desktop().screenGeometry().height()

# Set the window size to the screen size
window.setFixedWidth(screen_width)
window.setFixedHeight(screen_height-50)
grid=QGridLayout()
ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"


def create_button(text):#create buttons with the same style
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    create_worker_button = QPushButton(text)
    create_worker_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    create_worker_button.setStyleSheet(ch)
    return create_worker_button
def test_time(test_str):
    format = "%Y-%m-%d"

    # checking if format matches the date
    res = True

    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(test_str, format))
    except ValueError:
        res = False
    return res
def confirm_update_items_date(old_date,commande_dict_date,new_date,all_dates,cin,index,type,phone_number,name,reteur_type):
    print(old_date.currentText(),commande_dict_date,new_date,all_dates,cin,index, "test \n 0 \n test2")
    old_client_bill_id = commande_dict_date[old_date.currentText()]["id"]
    old_commande_info = commande_dict_date[old_date.currentText()]["tuple"]
    if type=="date":
        test=test_time(new_date)
        if test==False :
            QMessageBox.critical(None, 'Fail',"the date is not valid ")
        else:
            try:
                # if new_date in all_dates:
                #     client_bill_id = commande_dict_date[new_date]['id']
                #     print(client_bill_id)
                #     all_items_names=[x[0] for x in commande_dict_date[new_date]["tuple"]]
                #     print(all_items_names)
                #     cursor.execute(f"DELETE FROM commande_client where client_bill_id={old_client_bill_id} and item_name='{old_commande_info[index][0]}' ;")
                #     if old_commande_info[index][0] not in all_items_names:
                #         cursor.execute(f"INSERT INTO commande_client (quantiter,quantiter_price,client_bill_id,item_name) values ({old_commande_info[index][1]},{old_commande_info[index][2]},{client_bill_id},'{old_commande_info[index][0]}')")
                #     else:
                #         cursor.execute(f"UPDATE commande_client set quantiter =quantiter +{old_commande_info[index][1]} where client_bill_id={client_bill_id} and item_name='{old_commande_info[index][0]}'")
                #         cursor.execute(f"UPDATE commande_client set quantiter_price =quantiter_price +{old_commande_info[index][2]} where client_bill_id={client_bill_id} and item_name='{old_commande_info[index][0]}'")
                #
                #     connection.commit()
                # else:
                cursor.execute(
                   f"DELETE FROM commande_client where client_bill_id={old_client_bill_id} and item_name='{old_commande_info[index][0]}' ;")
                cursor.execute(f"insert into client_bill (client_bill_date,cin,money_payed) values ('{new_date}',{cin},{0}) ")
                cursor.execute(f"SELECT client_bill_id from client_bill where cin={cin} and client_bill_date='{new_date}'")
                for x in cursor:
                    client_bill_id=x[0]
                print(client_bill_id)
                cursor.execute(f"INSERT INTO commande_client (quantiter,quantiter_price,client_bill_id,item_name) values ({old_commande_info[index][1]},{old_commande_info[index][2]},{client_bill_id},'{old_commande_info[index][0]}')")
                connection.commit()
                QMessageBox.information(None, "Success", "l'article date modifier avec succées ")
                select_client_profile(None, reteur_type, int(cin), name, phone_number)




            except Exception as e:
                print(e)
                print(traceback.format_exc())
    else:
        if new_date.isdecimal() or (new_date[0]=="-" and new_date[1:].isdecimal()==True):
            cursor.execute(
                f"UPDATE COMMANDE_CLIENT set quantiter={new_date} where client_bill_id={old_client_bill_id} and item_name='{old_commande_info[index][0]}'")
            price = int(int(old_commande_info[index][2]) / float(old_commande_info[index][1]))
            new_price = int(price * float(new_date))
            cursor.execute(
                f"Update commande_client set quantiter_price={new_price} where client_bill_id={old_client_bill_id} and item_name='{old_commande_info[index][0]}'")
            connection.commit()
            QMessageBox.information(None, "Success", "l'article quantiter modifier avec succées ")
            select_client_profile(None, reteur_type, int(cin), name, phone_number)


        else:
            QMessageBox.critical(None, 'Fail', "give a valid quantiter")



def update_item_date_fn(existing_date,commande_dict,cin,name,phone_number,type,reteur_type):
    clear_widgets()
    update_item_date_frame(existing_date,commande_dict,cin,name,phone_number,type,reteur_type)
def update_item_date_frame(existing_date,commande_dict,cin,name,phone_number,type,reteur_type):
    def event():
        commande_list.clear()
        print(str(old_date_list.currentText()))
        commande_list.addItems(commande_dict[str(old_date_list.currentText())]["list"])

    print(commande_dict)
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : select_client_profile(None,reteur_type,int(cin),name,phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("Old date")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)

    try:
        old_date_list = QComboBox()
        old_date_list.setStyleSheet(ch)
        old_date_list.addItems(existing_date)
        old_date_list.currentIndexChanged.connect(event)
        widgets["door_cces"].append(old_date_list)
    except Exception as e:
        print(e)

    commande = QLabel("Commande : ")
    commande.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["update_acces"].append(commande)

    commande_list = QComboBox()
    commande_list.setStyleSheet(ch)
    commande_list.addItems(commande_dict[str(old_date_list.currentText())]["list"])
    widgets["full_name"].append(commande_list)

    print(commande_dict[str(old_date_list.currentText())]["list"])
    if type=="date":
        new_date_label = QLabel("New date : ")
        new_date_entry = QLineEdit(str(date.today()))
    else:
        new_date_label=QLabel("New quantiter : ")
        new_date_entry = QLineEdit(str(0))

    new_date_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["money_entry"].append(new_date_label)

    new_date_entry.setStyleSheet(ch)
    widgets["calender"].append(new_date_entry)


    confirm=create_button("Confirm ")
    widgets["confirm"].append(confirm)
    confirm.clicked.connect(lambda : confirm_update_items_date(old_date_list,commande_dict,new_date_entry.text(),existing_date,cin,commande_list.currentIndex(),type,phone_number,name,reteur_type))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["door_cces"][-1], 1, 1)
    grid.addWidget(widgets["update_acces"][-1], 2, 0)

    grid.addWidget(widgets["full_name"][-1], 2, 1)
    grid.addWidget(widgets["money_entry"][-1], 3, 0)
    grid.addWidget(widgets["calender"][-1], 3, 1)
    grid.addWidget(widgets["confirm"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 5, 0)


def confirm_update_money_date(old_date,new_money,cin,name,phone_number,type):
    if str(new_money).isdigit():
        print(old_date,new_money,cin)
        all_information=old_date.split(" : ")
        print(f"UPDATE client_bill set money_payed={str(new_money).replace(',','')} where client_bill_id={all_information[1]}")
        cursor.execute(f"UPDATE client_bill set money_payed={str(new_money)} where client_bill_id={all_information[1]}")
        connection.commit()
        QMessageBox.information(None,"Success",f"New regelement {money(new_money)} in {all_information[0]} ")
        select_client_profile(None, type, int(cin), name, phone_number)
    else:
        QMessageBox.critical(None, 'Fail', f"money need to be degit")

def confirm_update_money_type(old_date,new_money,cin,name,phone_number,type):
    if str(new_money)!="":
        print(old_date,new_money,cin)
        all_information=old_date.split(" : ")
        print(f"UPDATE client_bill set money_type='{new_money}' where client_bill_id={all_information[1]}")
        cursor.execute(f"UPDATE client_bill set money_type='{str(new_money)}' where client_bill_id={all_information[1]}")
        connection.commit()
        QMessageBox.information(None,"Success",f"New regelement {new_money} in {all_information[0]} ")
        select_client_profile(None, type, int(cin), name, phone_number)
    else:
        QMessageBox.critical(None, 'Fail', f"money need to be degit")

def imprimer_facture_detailler(all_bills,all_commande,name,phone_number,remize_money,first_date,second_date,all_dates):
    date1, date2 = 0, 1
    test = True
    try:
        date1 = datetime.strptime(first_date.split(" : ")[0], '%Y-%m-%d')
        date2 = datetime.strptime(second_date.split(" : ")[0], '%Y-%m-%d')
    except:
        QMessageBox.critical(None, 'Fail', "the dates are not correct ")
        test = False
    if test:

        if date2 < date1:
            QMessageBox.critical(None, 'Fail', "Second date need to be later than first date")
        else:
            all_dates_clean = [datetime.strptime(date.split(" : ")[0], '%Y-%m-%d') for date in all_dates]
            all_bills = all_bills[
                        find_occurrence(all_dates_clean, date1, find_last=False):find_occurrence(all_dates_clean, date2,
                                                                                                 find_last=True) + 1]
            all_commande = all_commande[
                           find_occurrence(all_dates_clean, date1, find_last=False):find_occurrence(all_dates_clean, date2,
                                                                                                    find_last=True) + 1]
            generate_bill("facture_detaillee\\facture de date specifique" + make_windows_friendly_filename(name) + ".pdf",
                          str(all_bills[0].client_bill_id), name, phone_number, all_bills, all_commande, "bill", remize_money)
            imprimer("facture_detaillee\\facture de date specifique" + make_windows_friendly_filename(name) + ".pdf")


def find_occurrence(numbers, target, find_last=False):
    left, right = 0, len(numbers) - 1
    closest_before, closest_after = None, None
    target_index = None

    while left <= right:
        mid = left + (right - left) // 2

        if numbers[mid] == target:
            target_index = mid

            if find_last:
                left = mid + 1
            else:
                right = mid - 1
        elif numbers[mid] < target:
            left = mid + 1
            closest_before = mid
        else:
            right = mid - 1
            closest_after = mid

    if target_index is not None:
        return target_index
    elif find_last:
        return closest_before
    else:
        return closest_after
def imprimer_facture(all_bills,all_commande,name,phone_number,all_remize,first_date,second_date,all_dates):
    date1,date2=0,1
    test=True
    try:
        date1 = datetime.strptime(first_date.split(" : ")[0], '%Y-%m-%d')
        date2 = datetime.strptime(second_date.split(" : ")[0], '%Y-%m-%d')
    except:
        QMessageBox.critical(None, 'Fail', "the dates are not correct ")
        test=False
    if test:
        if date2<date1:
            QMessageBox.critical(None, 'Fail', "Second date need to be later than first date")
        else:
            all_dates_clean=[datetime.strptime(date.split(" : ")[0], '%Y-%m-%d') for date in all_dates]
            all_bills = all_bills[find_occurrence(all_dates_clean, date1, find_last=False):find_occurrence(all_dates_clean, date2, find_last=True) + 1]
            remize_total=total_remize_speciale(all_remize,all_bills)
            all_commande = all_commande[find_occurrence(all_dates_clean, date1, find_last=False):find_occurrence(all_dates_clean, date2, find_last=True) + 1]
            all_items_total_quantiter={}
            all_money_payed = 0
            j=0
            for commande in all_commande:
                all_money_payed = all_money_payed + int(all_bills[j].money_payed)
                j=j+1
                for x in commande:

                    if str(x.item_name) not in all_items_total_quantiter:
                        all_items_total_quantiter[str(x.item_name)]={"quantiter":float(x.quantiter),"quantiter_price":int(x.quantiter_price)}
                    else:
                        all_items_total_quantiter[str(x.item_name)]["quantiter"] +=float(x.quantiter)
                        all_items_total_quantiter[str(x.item_name)]["quantiter_price"]+=int(x.quantiter_price)


            generate_total_bill(
                f"facture\\facture de date speciphique{all_bills[0].client_bill_id} " + make_windows_friendly_filename(name) + ".pdf",
                all_bills[0].client_bill_id, name, phone_number,
                all_items_total_quantiter, all_money_payed, remize_total)
            imprimer( f"facture\\facture de date speciphique{all_bills[0].client_bill_id} " + make_windows_friendly_filename(name) + ".pdf")

def chosing_date_for_facture_fn(existing_date,all_bills,all_commande,cin,name,phone_number,remize_money,reteur_type):
    clear_widgets()
    chosing_date_for_facture_frame(existing_date,all_bills,all_commande,cin,name,phone_number,remize_money,reteur_type)

def chosing_date_for_facture_frame(existing_date,all_bills,all_commande,cin,name,phone_number,remize_money,reteur_type):

    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : select_client_profile(None,reteur_type,int(cin),name,phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("premier date")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)

    old_date_list = QLineEdit(existing_date[0].split(" : ")[0])
    old_date_list.setStyleSheet(ch)

    widgets["door_cces"].append(old_date_list)

    second_date = QLabel("second date")
    second_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["explain_label"].append(second_date)

    second_date_list = QLineEdit(existing_date[-1].split(" : ")[0])
    second_date_list.setStyleSheet(ch)
    widgets["calender"].append(second_date_list)

    imprimer_facure_detailler=create_button("imprimer facture detaillée ")
    imprimer_facure_detailler.clicked.connect(
        lambda: imprimer_facture_detailler(all_bills, all_commande, name, phone_number, remize_money,old_date_list.text(),second_date_list.text(),existing_date))
    widgets["money_entry"].append(imprimer_facure_detailler)

    imprimer_facure = create_button("imprimer facture")
    imprimer_facure.clicked.connect(
        lambda: imprimer_facture(all_bills, all_commande, name, phone_number, remize_money,old_date_list.text(),second_date_list.text(),existing_date))

    widgets["phone_entry"].append(imprimer_facure)




    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["door_cces"][-1], 1, 1)
    grid.addWidget(widgets["explain_label"][-1], 2, 0)

    grid.addWidget(widgets["calender"][-1], 2, 1)
    grid.addWidget(widgets["money_entry"][-1], 4, 0)
    grid.addWidget(widgets["phone_entry"][-1], 4, 1)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 5, 0)

def update_item_money_fn(existing_date,cin,name,phone_number,reteur_type):
    clear_widgets()
    update_item_money_frame(existing_date,cin,name,phone_number,reteur_type)

def update_item_money_type_fn(existing_date,cin,name,phone_number,reteur_type):
    clear_widgets()
    update_item_money_type_frame(existing_date,cin,name,phone_number,reteur_type)

def update_item_money_type_frame(existing_date,cin,name,phone_number,reteur_type):
    # def event():
    #     commande_list.clear()
    #     commande_list.addItems(commande_dict[str(old_date_list.currentText())]["list"])

    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : select_client_profile(None,reteur_type,int(cin),name,phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("Old regelement ")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)


    old_date_list = QComboBox()
    old_date_list.setStyleSheet(ch)
    old_date_list.addItems(existing_date)
    # old_date_list.currentIndexChanged.connect(event)
    widgets["door_cces"].append(old_date_list)


    commande = QLabel("New reglement : ")
    commande.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["update_acces"].append(commande)



    new_date_entry = QLineEdit("0")
    new_date_entry.setStyleSheet(ch)
    widgets["calender"].append(new_date_entry)


    confirm=create_button("Confirm ")
    widgets["confirm"].append(confirm)
    confirm.clicked.connect(lambda : confirm_update_money_type(old_date_list.currentText(),new_date_entry.text(),cin,name,phone_number,reteur_type))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["door_cces"][-1], 1, 1)
    grid.addWidget(widgets["update_acces"][-1], 2, 0)
    grid.addWidget(widgets["calender"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)
def update_item_money_frame(existing_date,cin,name,phone_number,reteur_type):
    # def event():
    #     commande_list.clear()
    #     commande_list.addItems(commande_dict[str(old_date_list.currentText())]["list"])

    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : select_client_profile(None,reteur_type,int(cin),name,phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("Old regelement ")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)


    old_date_list = QComboBox()
    old_date_list.setStyleSheet(ch)
    old_date_list.addItems(existing_date)
    # old_date_list.currentIndexChanged.connect(event)
    widgets["door_cces"].append(old_date_list)


    commande = QLabel("New reglement : ")
    commande.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["update_acces"].append(commande)



    new_date_entry = QLineEdit("0")
    new_date_entry.setStyleSheet(ch)
    widgets["calender"].append(new_date_entry)


    confirm=create_button("Confirm ")
    widgets["confirm"].append(confirm)
    confirm.clicked.connect(lambda : confirm_update_money_date(old_date_list.currentText(),new_date_entry.text(),cin,name,phone_number,reteur_type))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["door_cces"][-1], 1, 1)
    grid.addWidget(widgets["update_acces"][-1], 2, 0)
    grid.addWidget(widgets["calender"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)

def update_client_fn(cin, name, phone_number,reteur_type):
    clear_widgets()
    update_client_frame(cin,name,phone_number,reteur_type)
def update_client_frame(cin,name,phone_number,reteur_type):
    def update_name(old_name,ch,scroll_grid,confirm):
        old_name[0]=QLineEdit(name)
        old_name[0].setStyleSheet(ch)
        scroll_grid.addWidget(old_name[0],2,0,1,2)
        confirm.show()
    def update_tel(old_tel,ch,scroll_grid,confirm):
        old_tel[0] = QLineEdit(phone_number)
        old_tel[0].setStyleSheet(ch)
        scroll_grid.addWidget(old_tel[0],4,0,1,2)

        confirm.show()

    def confirm_fn(old_name,name,old_tel,phone_number):
        if type(old_name[0])!=int:
            if str(old_name[0].text())!=name:
                print(f"update the_client set client_full_name='{str(old_name[0].text())}' where cin={cin}")
                cursor.execute(f"update the_client set client_full_name='{str(old_name[0].text())}' where cin={cin}")
                connection.commit()
        if type(old_tel[0])!=int :
            if str(old_tel[0].text())!=phone_number :
                print(f"update the_client set phone_number={str(old_tel[0].text())} where cin={cin}")
                cursor.execute(f"update the_client set phone_number={str(old_tel[0].text())} where cin={cin}")
                connection.commit()
        QMessageBox.information(None,"Success","le donner de client est changer avec succer ")
    old_name=[0]
    old_tel=[0]
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda: select_client_profile(None, reteur_type, int(cin), name, phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    update_client_name=create_button("changer le nom ")
    update_client_name.clicked.connect(lambda : update_name(old_name,ch,scroll_grid,confirm))

    update_client_phone_number = create_button("changer le Tel ")
    update_client_phone_number.clicked.connect(lambda : update_tel(old_tel,ch,scroll_grid,confirm))

    confirm=create_button("Confirm")
    confirm.clicked.connect(lambda : confirm_fn(old_name,name,old_tel,phone_number))

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content_widget = QWidget()
    scroll_area.setWidget(scroll_content_widget)
    widgets["scroll"].append(scroll_area)

    scroll_grid = QGridLayout(scroll_content_widget)
    scroll_grid.addWidget(update_client_name, 1, 0, 1, 2)
    scroll_grid.addWidget(update_client_phone_number, 3, 0, 1, 2)
    scroll_grid.addWidget(confirm,5,0)
    scroll_grid.addWidget(back, 0, 0,1,2)
    scroll_grid.addWidget(back_main, 6, 0)

    grid.addWidget(widgets["scroll"][-1],0,0)

    confirm.hide()



def confirm_change_client_commande_date(first_date,new_date,ids,cin,name,phone_number,reteur_type):
    id='id'
    test = test_time(new_date)
    if test == False:
        QMessageBox.critical(None, 'Fail', "the date is not valid ")
    else:
        cursor.execute(f"update client_bill set client_bill_date='{new_date}' where client_bill_id={ids[first_date][id]};")
        connection.commit()
        QMessageBox.information(None, "Success", "commande date chenged succsefuly ")
        select_client_profile(None, reteur_type, int(cin), name, phone_number)
def confirm_annuler(date_to_delete,cin,name,phone_number,type):
    dialog = CustomDialog()
    long_text = "are you sure to delete this commande  ?\n" + str(date_to_delete)
    dialog.setText(long_text)

    if dialog.exec_() == QDialog.Accepted:
        code=date_to_delete.split(" : ")[1]
        cursor.execute(f"select item_name,quantiter from commande_client where client_bill_id={code}")
        l=[]
        items_info={}
        for x in cursor:
            items_info[str(x[0])]=float(x[1])
        for item_name,value in items_info.items():
            if value>0:
                cursor.execute(f"update items set item_stock=item_stock+{value} where item_name='{item_name}'")
            else:
                print(f"update items set item_stock=item_stock-{str(value)[1:]} where item_name='{item_name}'")
                cursor.execute(f"update items set item_stock=item_stock-{str(value)[1:]} where item_name='{item_name}'")

        cursor.execute(f"delete from commande_client where client_bill_id={code} ")
        cursor.execute(f"delete from client_bill where client_bill_id={code}")
        connection.commit()
        QMessageBox.information(None, "Success", "commande annuler avec succer ")
        select_client_profile(None, type, int(cin), name, phone_number)
    else:
        print("canceled")


def annuler_commande_fn(all_dates,cin,name,phone_number,reteur_type):
    clear_widgets()
    annuler_commande_frame(all_dates,cin,name,phone_number,reteur_type)
def annuler_commande_frame(all_dates,cin,name,phone_number,reteur_type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda: select_client_profile(None, reteur_type, int(cin), name, phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("chose date to annuler le commande")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)

    old_date_list = QComboBox()
    old_date_list.setStyleSheet(ch)
    old_date_list.addItems(all_dates)
    # old_date_list.currentIndexChanged.connect(event)
    widgets["door_cces"].append(old_date_list)

    confirm=create_button("Confirm")
    confirm.clicked.connect(lambda : confirm_annuler(old_date_list.currentText(),cin,name,phone_number,reteur_type))
    widgets["confirm"].append(confirm)

    grid.addWidget(widgets["label"][-1],1,0)
    grid.addWidget(widgets["door_cces"][-1],2,0)
    grid.addWidget(widgets["confirm"][-1],3,0)
    grid.addWidget(widgets["button"][-1],0,0)
    grid.addWidget(widgets["back_to_main"][-1],4,0)

def show_remize_fn(all_remize,cin,name,phone_number,reteur_type):
    clear_widgets()
    show_remize_frame(all_remize,cin,name,phone_number,reteur_type)
def show_remize_frame(all_remize,cin,name,phone_number,reteur_type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda: select_client_profile(None, reteur_type, int(cin), name, phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(len(all_remize)+3)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("code"))
    tableWidget.setItem(0, 1, QTableWidgetItem("mantant"))
    tableWidget.setItem(0, 2, QTableWidgetItem("date"))


    i = 0

    total = 0
    for remize in all_remize:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(remize.id)))
        tableWidget.setItem(i, 1, QTableWidgetItem(money(str(remize.quantiter))))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(remize.date)))
        total=total+int(remize.quantiter)
    tableWidget.setItem(i+1, 1, QTableWidgetItem("total remize"))
    tableWidget.setItem(i+1, 2, QTableWidgetItem(money(str(total))))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()

    widgets["table"].append(tableWidget)
    grid.addWidget(widgets["table"][-1],1,0)

    grid.addWidget(widgets["button"][-1],0,0)
    grid.addWidget(widgets["back_to_main"][-1],2,0)

def confirm_remise(remise, remize_date,cin, name, phone_number,all_bills,all_commande,type):
    if str(remise).isdigit() and test_time(remize_date):
        cursor.execute(f"SELECT * FROM REMIZE WHERE cin={cin} and remize_date='{remize_date}'")
        if cursor.rowcount == 0:
            cursor.execute(f"insert into remize (remize_quantiter,remize_date,cin) values ({remise},'{remize_date}',{cin})")
            connection.commit()
        else:
            cursor.execute(
                f"update remize set remize_quantiter={remise} where cin={cin} and remize_date='{remize_date}'")
            connection.commit()

        QMessageBox.information(None, "Success", "remize est confirmer")
        clear_widgets()
        client_bills_frame(all_bills,all_commande,type,name,phone_number,cin)

    else :
        QMessageBox.critical(None, 'Fail', "remize have to be digit ")
def remise_fn(cin,name,phone_number,all_bills,all_commande,type):
    clear_widgets()
    remise_frame(cin,name,phone_number,all_bills,all_commande,type)
def remise_frame(cin,name,phone_number,all_bills,all_commande,type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda: select_client_profile(None, type, int(cin), name, phone_number))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    old_date = QLabel("Remise exceptionnelle : ")
    old_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["label"].append(old_date)

    remise = QLineEdit("0")
    remise.setStyleSheet(ch)
    # old_date_list.currentIndexChanged.connect(event)
    widgets["door_cces"].append(remise)

    remize_date = QLabel("Remise exceptionnelle date : ")
    remize_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    widgets["explain_label"].append(remize_date)

    remise_date_entry = QLineEdit(all_bills[-1].client_bill_date)
    remise_date_entry.setStyleSheet(ch)
    # old_date_list.currentIndexChanged.connect(event)
    widgets["money_entry"].append(remise_date_entry)

    confirm=create_button("Confirm")
    confirm.clicked.connect(lambda : confirm_remise(remise.text(),remise_date_entry.text(),int(cin), name, phone_number,all_bills,all_commande,type))
    widgets["confirm"].append(confirm)

    grid.addWidget(widgets["label"][-1],1,0)
    grid.addWidget(widgets["door_cces"][-1],2,0)
    grid.addWidget(widgets["explain_label"][-1], 3, 0)
    grid.addWidget(widgets["money_entry"][-1], 4, 0)
    grid.addWidget(widgets["confirm"][-1],5,0)
    grid.addWidget(widgets["button"][-1],0,0)
    grid.addWidget(widgets["back_to_main"][-1],6,0)



def confirm_create_item(item_name,item_price,item_stock):
    if str(item_price.text()).isdigit() and (str(item_stock.text()).isdigit() or str(item_stock.text()).isdecimal()) and (str(item_name.text())!=""):
        if int(item_price.text())>0 and int(item_stock.text())>0:
            new_item=items(str(item_name.text()),str(item_price.text()),str(item_stock.text()),0,0)
            test=new_item.create_item()
            if test:
                QMessageBox.information(None, "Success", "L'article a été créé avec succès  ")
                item_name.setText("")
                item_price.setText("")
                item_stock.setText("")
            else :
                QMessageBox.critical(None, 'Fail', "L'article existe déjà avec le même nom orL'un des champs est de type incorrect")
        else:
            QMessageBox.critical(None, 'Fail',
                                 "le prix de l'article et le stock de l'article doivent être des nombres positives ")

    else:
        QMessageBox.critical(None, 'Fail', "le prix de l'article et le stock de l'article doivent être des nombres positives sans caractères et le nom de l'article n'est pas vide ")


def confirm_item_price(item_name,item_price):
    item_name=str(item_name)
    item_pricee=str(item_price.text())
    print(item_name)
    if item_name!="":
        if item_pricee.isdigit():
            cursor.execute(f"select count(*) from items where item_name='{item_name}'")
            for x in cursor:
                k = x[0]
            if k == 1:
             if int(item_pricee)>0:
                cursor.execute(f"update items set item_price={item_pricee} where item_name='{item_name}'")
                connection.commit()
                QMessageBox.information(None, "Succes", "Le prix de l'article a été mis à jour avec succès   ")
                item_price.setText("")
             else:
                QMessageBox.critical(None, 'Fail', "Le prix de l'article ne peut pas être négatif ! ")
            else :
                QMessageBox.critical(None, 'Fail', "L'article n'existe pas ! ")

        else:
            QMessageBox.critical(None, 'Fail', "Please enter the new item price  ")
    else :
        QMessageBox.critical(None, 'Fail', "Please enter Item name  ")

def confirm_item_name(item_name,item_price):
    item_name=str(item_name)
    item_pricee=str(item_price.text())
    print(item_name)
    if item_name!="":
        if item_pricee!="":
            cursor.execute(f"select item_id from items where item_name='{item_name}'")
            id=0
            for x in cursor:
                id=x[0]
            if id==0:
                print("errror happen ")
            else:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                cursor.execute(f"update items set item_name='{item_pricee}' where item_id={id}")
                cursor.execute(f"update commande_client set item_name='{item_pricee}' where item_name='{item_name}'  ")
                cursor.execute(f"update devis_commande set item_name='{item_pricee}' where item_name='{item_name}'  ")
                cursor.execute(f"update commande_supplier set item_name='{item_pricee}' where item_name='{item_name}'")
                connection.commit()
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

                QMessageBox.information(None, "Succes", "Le nom de l'article a été mis à jour avec succès")


def confirm_item_stock_2(item_name,item_stock):
    item_name = str(item_name)
    item_stockk = str(item_stock.text())
    if item_name != "":
        if item_stockk.isdecimal():
            cursor.execute(f"select count(*) from items where item_name='{item_name}'")
            for x in cursor:
                k = x[0]
            if k == 1:
                if float(item_stockk) >= 0:
                    cursor.execute(
                        f"update items set item_stock=item_stock-{item_stockk} where item_name='{item_name}'")
                    connection.commit()
                    QMessageBox.information(None, "Succes", "Le stock d'articles a été mis à jour avec succès ")
                    item_stock.setText("")
                else:
                    QMessageBox.critical(None, 'Fail', "Le stock de l'article ne peut pas être négatif !")
            else:
                QMessageBox.critical(None, 'Fail', "Item doesn't exist !! ")

        else:
            QMessageBox.critical(None, 'Fail', "Veuillez entrer le nouveau stock d'articles ")
    else:
        QMessageBox.critical(None, 'Fail', "Please enter Item name  ")
def confirm_item_stock(item_name,item_stock):
        item_name = str(item_name)
        item_stockk = str(item_stock.text())
        if item_name != "":
            if item_stockk.isdecimal():
                cursor.execute(f"select count(*) from items where item_name='{item_name}'")
                for x in cursor:
                    k = x[0]
                if k == 1:
                    if float(item_stockk) >= 0:
                        cursor.execute(
                            f"update items set item_stock={item_stockk} where item_name='{item_name}'")
                        connection.commit()
                        QMessageBox.information(None, "Succes", "Le stock d'articles a été mis à jour avec succès  ")
                        item_stock.setText("")
                    else:
                        QMessageBox.critical(None, 'Fail', "Le stock de l'article ne peut pas être négatif ! ")
                else:
                    QMessageBox.critical(None, 'Fail', "Item doesn't exist !! ")

            else:
                QMessageBox.critical(None, 'Fail', "Veuillez entrer le nouveau stock d'articles")
        else:
            QMessageBox.critical(None, 'Fail', "Please enter Item name  ")
def confirm_create_client_bill(full_name,cin,date_entry,table,all_items,money_entry,welcome_label,type,money_type):
    print(all_items)
    full_name=str(full_name.text())
    cin=str(cin.text())
    if cin=="" or  not (cin.isdigit()):
        cin="1"
    date=str(date_entry)
    if type=="reteur":
        moneyy=str(money_entry)
        money_typee=""

    else:
        moneyy=str(money_entry.text())
        print(money_type)
        money_typee=str(money_type.text())
    print("money ", moneyy)
    if moneyy== "" :
        moneyy= "0"
    elif moneyy[0]== "-" or (moneyy[0] != "-" and not moneyy.isdigit()):
        if not moneyy[1:].isdigit():
            moneyy= "0"
    print(moneyy)
    text=f"client : {full_name} Tel: {cin} reglement : {money(moneyy)} type : {money_typee} date : {date} \n"
    size=0
    print(text)
    test_2=False
    test = test_time(date)
    if test==False:
        QMessageBox.critical(None, 'Fail', "the date is not valid ")
    elif cin=='1':
        QMessageBox.critical(None, 'Fail', "tel n'est pas valable ")
    else:
        try:
            for i in range(1,table.rowCount()):
                print("test0")
                lineEdit = table.cellWidget(i, 3)
                if isinstance(lineEdit, QLineEdit):
                    print("test1")
                    quantiter_text = lineEdit.text()
                    print(quantiter_text)
                    if quantiter_text == "":
                        print("test")
                        all_items[str(table.item(i , 0).text())].item_quantiter="0"
                    elif quantiter_text.isdecimal() or (quantiter_text[0]=="-" and quantiter_text[1:].isdecimal() ):

                        if type=="reteur" and quantiter_text[0]!="-":
                            all_items[str(table.item(i, 0).text())].item_quantiter = "-"+quantiter_text
                        else:
                            all_items[str(table.item(i, 0).text())].item_quantiter = quantiter_text
                        if quantiter_text!="0":
                            size=size+1
                            test_2 = True
                        print(quantiter_text)
                    else:
                        all_items[str(table.item(i, 0).text())].item_quantiter = "0"

                item_price = str(table.item(i , 1).text())
                if item_price == "" or item_price == "0":
                    item_price = all_items[str(table.item(i, 0).text())].item_price
                elif item_price.isdigit():
                    item_price = str(table.item(i , 1).text())
                else:
                    item_price = all_items[str(table.item(i, 0).text())].item_price
                all_items[str(table.item(i , 0).text())].item_price = item_price
                # print(item.item_price, item.item_name)
        except Exception as e:
            print(e)
        dialog = CustomDialog()
        if type=="devis":
            long_text = "confirmer devis ?\n" + text
        elif type=='bill':
            long_text = "confirmer facture  ?\n"+text
        else:
            long_text = "confirmer bonde de reteur  ?\n" + text
        dialog.setText(long_text)
        dialog.set_table(list(all_items.values()),size,"bill")

        if int(moneyy)!=0:
            test_2=True
        if dialog.exec_() == QDialog.Accepted:
            the_client = client(full_name, cin,0)
            if test_2:
                if type!="devis":
                    items = the_client.create_clent_bill_commande(list(all_items.values()), date, moneyy,money_typee)
                else:
                    items=the_client.create_client_devis_commande(list(all_items.values()), date)
                print(text)
                new_dialog = CustomDialog()
                if type=="bill":
                    long_text = "Do you want to get bon de sortie  ?\n" + text
                    new_dialog.setText(long_text)
                    if new_dialog.exec_() == QDialog.Accepted:
                        try:
                            cursor.execute("select bonde_levraison from global_variable ")
                            id=1
                            for x in cursor:
                                id=int(x[0])
                            generate_bonde_levraison("levraison\\bonde_de_levraison"+str(id)+make_windows_friendly_filename(full_name)+".pdf",id,full_name,cin,moneyy,date,list(all_items.values()),"sortie")
                            cursor.execute("UPDATE global_variable set bonde_levraison=bonde_levraison+1 ")
                            connection.commit()
                        except Exception as e:
                            print(e)
                            print(traceback.format_exc())
                    else:
                        pass
                    money_entry.setText("0")
                elif type=="reteur":
                    long_text = "Do you want to get bon de reteur  ?\n" + text
                    new_dialog.setText(long_text)
                    if new_dialog.exec_() == QDialog.Accepted:
                        try:
                            cursor.execute("select bonde_reteur from global_variable ")
                            id = 1
                            for x in cursor:
                                id = int(x[0])
                            generate_bonde_levraison("reteur\\bonde_de_reteur" +str(id)+make_windows_friendly_filename(full_name) + ".pdf", id, full_name, cin, moneyy, date,
                                                     list(all_items.values()),"reteur")
                            cursor.execute("UPDATE global_variable set bonde_reteur=bonde_reteur+1 ")
                            connection.commit()


                        except Exception as e:
                            print(e)
                            print(traceback.format_exc())
                    else:
                        pass
                else:
                    long_text = "Do you want to get  devis paper  ?\n" + text
                    new_dialog.setText(long_text)
                    if new_dialog.exec_() == QDialog.Accepted:
                        try:
                            cursor.execute("select devis_code from global_variable ")
                            id = 1
                            for x in cursor:
                                id = int(x[0])
                            generate_bonde_levraison("devis\\devis" + make_windows_friendly_filename(full_name) +str(id)+ ".pdf", id, full_name, cin,
                                                     moneyy, date,
                                                     list(all_items.values()), "devis")
                            cursor.execute("UPDATE global_variable set devis_code=devis_code+1 ")
                            connection.commit()


                        except Exception as e:
                            print(e)
                            print(traceback.format_exc())
                    else:
                        pass
                if type=="devis":
                    QMessageBox.information(None, "Succes", "Devis créée avec succès  ")
                else:
                    QMessageBox.information(None, "Succes", "Facture créée avec succès  ")
                i = 0
                for x in items:
                    i = i + 1
                    lineEdit = QLineEdit(str(0))
                    table.setCellWidget(i, 3, lineEdit)
                    table.setItem(i, 2, QTableWidgetItem(x.item_stocks))
                    table.setItem(i, 4, QTableWidgetItem("0"))

                welcome_label.setText(" Total : remain : ")
                if type=="bill":
                    money_type.setText("")
            else:
                QMessageBox.critical(None, 'Fail', "You need to add items ")
        else:
            print("Cancelled")

def confirm_create_supplier_bill(full_name,cin,calender,table,all_items,money_entry,welcome_entry):
    full_name=str(full_name.text())
    cin=str(cin.text())
    if cin=="" or  not (cin.isdigit()):
        QMessageBox.critical(None, 'Fail', "Veuillez saisir le numéro de téléphone du fournisseur ! ")
        return None
    else:
        date=str(calender)
        money=str(money_entry.text())
        if money=="" or  not (money.isdigit()):
            money="0"
        test = test_time(calender)
        test_2 = False
        size=0
        if test == False:
            QMessageBox.critical(None, 'Fail', "the date is not valid ")

        else :
            try:
                for i in range(1, table.rowCount()):
                    print("test0")
                    lineEdit = table.cellWidget(i, 2)
                    if isinstance(lineEdit, QLineEdit):
                        print("test1")
                        quantiter_text = lineEdit.text()
                        print(quantiter_text)
                        if quantiter_text == "":
                            print("test")
                            all_items[str(table.item(i, 0).text())].item_quantiter = "0"
                        elif quantiter_text.isdecimal() :
                            all_items[str(table.item(i, 0).text())].item_quantiter = quantiter_text
                            if quantiter_text != "0":
                                size = size + 1
                                test_2 = True
                            print(quantiter_text)
                        else:
                            all_items[str(table.item(i, 0).text())].item_quantiter = "0"

                    lineEdit = table.cellWidget(i, 3)
                    if isinstance(lineEdit, QLineEdit):
                        print("test1")
                        item_price = str(lineEdit.text())
                    else :
                        item_price="0"
                    if item_price == "" or item_price == "0":
                        item_pricee = "0"
                    elif item_price.isdigit():
                        item_pricee=item_price
                    else:
                        item_pricee = "0"
                    all_items[str(table.item(i, 0).text())].price = item_pricee
                    # print(item.item_price, item.item_name)
            except Exception as e:
                print(e)
            if test_2 or  money!="0":
                itemss=list(all_items.values())

                dialog = CustomDialog()
                dialog.setText("confirm fournisseur facture")
                dialog.set_table(list(all_items.values()), size,"fournisseur")


                if dialog.exec_() == QDialog.Accepted:
                    provider=supplier(0,full_name,cin)
                    provider.create_commande(itemss,money,date)
                    QMessageBox.information(None, "Succes", "Facture créée avec succès  ")


                    for i in range(1,len(itemss)):

                        lineEdit = QLineEdit(str(0))
                        table.setCellWidget(i, 2, lineEdit)
                        lineEdit = QLineEdit(str(0))
                        table.setCellWidget(i, 3, lineEdit)
                    money_entry.setText("0")
                    welcome_entry.setText("total :  remain : ")
            else:
                QMessageBox.critical(None,'Fail', "vous devez ajouter des articles ou de l'argent payé")



def supplier_bill_fn(all_bills,all_commande,type,name):
    clear_widgets()
    supplier_bills_frame(all_bills, all_commande,type,name)
def client_devis_fn(all_bills,all_commande,type,name,phone_number):
    clear_widgets()
    print("test")
    client_devis_frame(all_bills, all_commande, type, name, phone_number)


def client_bills_fn(all_bills,all_commande,type,name,phone_number,cin):
    clear_widgets()
    client_bills_frame(all_bills,all_commande,type,name,phone_number,cin)
def update_stock_fn():
    clear_widgets()
    update_stock_frame()
def update_price_fn():
    clear_widgets()
    update_price_frame()
def update_item_name_fn():
    clear_widgets()
    update_item_name_frame()
def create_client_bill_fn(type):
    clear_widgets()
    try:
        create_client_bill_frame(type)
    except Exception as e:
        print(e)
def back_to_search_client(type):
    clear_widgets()
    search_for_client_frame(type)
def back_to_search_supplier():
    clear_widgets()
    search_for_supplier_frame()



def create_item_fn():#clear all the widgets from the frame then move to the create worker  frame
    clear_widgets()
    create_item_frame()
def back_to_main():
    clear_widgets()
    main_frame()


def search_for_client_fn(type):
    clear_widgets()
    search_for_client_frame(type)
def update_worker():
    clear_widgets()
    update_frame()
def select_date(type):
    clear_widgets()
    select_frame(type)
def search_name_supplier(full_name,clients,table,type):
    searched_client = []
    full_name = str(full_name.text())
    if full_name == "":
        searched_client=clients
    else:
        if type=="Full name":
            for clientt in clients:
                name=clientt.name
                print(name)
                print(full_name)
                if full_name.lower() in name.lower():
                    searched_client.append(clientt)
        elif type=="Cin":
            for clientt in clients:
                cin=str(clientt.phone_number)
                print(full_name,cin)
                if len(full_name)<=len(cin):
                    cin=cin[:len(full_name)]
                    print(cin)
                if cin==full_name:
                    searched_client.append(clientt)

    table.setRowCount(len(searched_client) + 1)
    i = 0
    for clientt in searched_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.phone_number)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.name)))
def search_name(full_name,clients,tablee,type):
    searched_client=[]
    full_name = str(full_name.text())
    table=tablee[0]
    print(full_name,clients[0].full_name,type)
    if full_name == "":
        searched_client=clients
    else:
        if type=="Full name":
            for clientt in clients:
                name=clientt.full_name
                print(name)
                print(full_name)
                print(full_name.lower() in name.lower())
                if full_name.lower() in name.lower():
                    searched_client.append(clientt)
                # if len(full_name)<=len(name):
                #     name=name[:len(full_name)]
                #     print(name)
                # if name == full_name:
                #     searched_client.append(clientt)


        elif type=="Cin":
            for clientt in clients:
                cin=str(clientt.phone_number)
                print(full_name,cin)
                if len(full_name)<=len(cin):
                    cin=cin[:len(full_name)]
                    print(cin)
                if cin==full_name:
                    searched_client.append(clientt)

    table.setRowCount(len(searched_client)+1)
    i=0
    for clientt in searched_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.phone_number)))
        table.setItem(i, 2, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))

    tablee[0]=table
def select_supplier_profile(table,type):
    k = 0
    for currentQTableWidgetItem in table.selectedItems():
        print(currentQTableWidgetItem.row())
        k = currentQTableWidgetItem.row()
    cin = str(table.item(k,2).text())
    name=str(table.item(k,1).text())
    print(cin)
    all_bills = supplier_bill.create_bills(cin)
    all_commande = []
    for billl in all_bills:
        bill_id = billl.supplier_bill_id
        all_commande.append(commande_supplier.create_commande_supplier(bill_id))
    supplier_bill_fn(all_bills, all_commande,type,name)
def select_client_profile(tablee,type,cinn,name,phone_number):
    if cinn>0:
        cin=str(cinn)
    else:
        k = 0
        table=tablee[0]
        for currentQTableWidgetItem in table.selectedItems():
            print(currentQTableWidgetItem.row())
            k = currentQTableWidgetItem.row()
        cin = str(table.item(k,2).text())
        name=str(table.item(k,1).text())
        phone_number=str(table.item(k,0).text())
    print(cin)
    all_bills=bill.create_bills(cin)
    all_commande=[]
    for billl in all_bills:
        bill_id=billl.client_bill_id
        all_commande.append(commande_client.create_commande_client(bill_id))
    bill.delete_corrupted_bills(all_bills,all_commande)
    client_bills_fn(all_bills,all_commande,type,name,phone_number,cin)



def select_client_devis(tablee,type,cinn,name,phone_number):
    if cinn>0:
        cin=str(cinn)
    else:
        k = 0
        table=tablee[0]
        for currentQTableWidgetItem in table.selectedItems():
            print(currentQTableWidgetItem.row())
            k = currentQTableWidgetItem.row()
        cin = str(table.item(k,2).text())
        name=str(table.item(k,1).text())
        phone_number=str(table.item(k,0).text())
    print(cin)
    all_bills=Devis.create_devis(cin)
    all_commande=[]
    for billl in all_bills:
        bill_id=billl.client_devis_id
        all_commande.append(devis_commande.create_devis_client(bill_id))
    Devis.delete_corrupted_devis(all_bills,all_commande)
    client_devis_fn(all_bills,all_commande,type,name,phone_number)

# def conferm_full_name(name_entry,id_entry):#this function is for conferming the update of the worker full name and not allowing to update it to empty
#     name=str(name_entry.text())
#     k=1
#     if name!="":
#         id=int(str(id_entry.text()))
#         cursor.execute(f"select count(user_id) from user_data where user_id={str(id)} ")
#         for x in cursor:
#             k=x[0]
#         if k==1:
#             cursor.execute(f"update user_data set full_name='{name}' where user_id={str(id)}")
#             connection.commit()
#             QMessageBox.information(None,"Succes","Update full name succesfuly ")
#         else:
#             QMessageBox.critical(None,'Fail', "Worker doesn't exist  ")
#
#     else:
#         QMessageBox.critical(None,'Fail',"Full name can't be empty ")
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
        cursor.execute(f"select b.client_bill_id,b.money_payed,c.cin,c.client_full_name,c.phone_number,b.money_type from client_bill b,the_client c where client_bill_date= '{selected_date}' and c.cin=b.cin ")
        for x in cursor:
           clients.append(client(
               name=str(x[3]),
               cin=str(x[2]),
               phone_number=str(x[-2])
           ))
           print(x[3])
           clients[i].bill.append(bill(client_bill_id=str(x[0]),
                                       client_bill_date=str(selected_date),
                                       cin=str(x[2]),
                                       money_payed=str(x[1]),type=str(x[-1])))
           i=i+1
        i=0
        cursor.execute(f"select b.supplier_bill_id,b.money_payed,s.supplier_id,s.supplier_name,s.phone_number from supplier_bill b,supplier s where bill_date= '{selected_date}' and s.supplier_id=b.supplier_id ")
        for x in cursor:
            suppliers.append(supplier(id=str(x[2]),name=str(x[3]),phone_number=str(x[-1])))
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
            f"select b.client_bill_id,b.money_payed,c.cin,c.client_full_name,c.phone_number from client_bill b,the_client c where client_bill_date= '{selected_date}' and c.cin=b.cin ")
        for x in cursor:
            clients.append(client(
                name=str(x[3]),
                cin=str(x[2]),phone_number=str(x[-1])
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
            f"select b.supplier_bill_id,b.money_payed,s.supplier_id,s.supplier_name,s.phone_number from supplier_bill b,supplier s where bill_date= '{selected_date}' and s.supplier_id=b.supplier_id ")
        for x in cursor:
            suppliers.append(supplier(id=str(x[2]),
                                      name=str(x[3]),
                                      phone_number=str(x[-1])
                                     ))
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
    show_dayly_bill_frame(clients,suppliers,k,type)
def main_frame():#this function is for creating the main frame
    #label
    # welcome_label=QLabel("Welcome to your application ")
    # welcome_label.setStyleSheet("font-size: 15px;"+"color:'#5B2A86'")
    # welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    # widgets["label"].append(welcome_label)

    # create button

    create_worker_button=create_button("Créer une facture client")
    widgets["create_button"].append(create_worker_button)
    create_worker_button.clicked.connect(lambda : create_client_bill_fn("bill"))

    create_devis_button = create_button("Créer une devis client")
    widgets["money_entry"].append(create_devis_button)
    create_devis_button.clicked.connect(lambda: create_client_bill_fn("devis"))

    create_reteur_bill_button = create_button("Créer une facteur de reteur")
    widgets["update_full_name"].append(create_reteur_bill_button)
    create_reteur_bill_button.clicked.connect(lambda: create_client_bill_fn("reteur"))

    create_worker_button = create_button("Recherche d'une facture client")
    widgets["search_client_bill"].append(create_worker_button)
    create_worker_button.clicked.connect(lambda :search_for_client_fn("bill"))

    recherche_devis_button = create_button("Recherche d'une devis client")
    widgets["full_name"].append(recherche_devis_button)
    recherche_devis_button.clicked.connect(lambda : search_for_client_fn("devis"))

    create_worker_button = create_button("Recherche d'une facture fournisseuse")
    widgets["search_supplier_bill"].append(create_worker_button)
    create_worker_button.clicked.connect(search_for_supplier_fn)

    select_button = create_button("Sélectionner la date")
    widgets["door_cces"].append(select_button)
    select_button.clicked.connect(lambda : select_date("all"))

    Select_date_button=create_button("Créer un article")
    widgets["select_button"].append(Select_date_button)
    Select_date_button.clicked.connect(create_item_fn)


    Update_worker_button=create_button("Mise à jour de l'article")
    widgets["update_button"].append(Update_worker_button)
    Update_worker_button.clicked.connect(update_worker)

    Update_worker_button = create_button("Créer une facture fournisseur ")
    widgets["Create_supplier_bill"].append(Update_worker_button)
    Update_worker_button.clicked.connect(create_supplier_bill_fn)

    # grid.addWidget(widgets["label"][-1],0,0)
    grid.addWidget(widgets["create_button"][-1],0,0)
    grid.addWidget(widgets["update_full_name"][-1],0,1)
    grid.addWidget(widgets["money_entry"][-1],0,2)

    grid.addWidget(widgets["select_button"][-1],1,0)
    grid.addWidget(widgets["door_cces"][-1],2 , 0)
    grid.addWidget(widgets["search_client_bill"][-1], 3, 0)
    grid.addWidget(widgets["full_name"][-1], 3, 1)

    grid.addWidget(widgets["search_supplier_bill"][-1], 4, 1)
    grid.addWidget(widgets["update_button"][-1],1,1)
    grid.addWidget(widgets["Create_supplier_bill"][-1],4, 0)
def back_to_select_2(type):
    clear_widgets()
    if type=="all":
        back_to_main()
    elif type=="client":
        back_to_search_client("bill")
    else:
        back_to_search_supplier()
def select_frame(type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    welcome_label=QLabel("Sélectionner la date "+type)
    welcome_label.setStyleSheet("font-size: "+font_size +"px;"+"color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : back_to_select_2(type))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    select_date_4 = QCalendarWidget()
    select_date_4.setGridVisible(True)
    select_date_4.setStyleSheet(ch)
    widgets["calender"].append(select_date_4)
    select_date_4.clicked.connect(lambda : select_fn(select_date_4,type))

    grid.addWidget(widgets["label"][-1],0,0)
    if type!="all":
        grid.addWidget(widgets["back_to_main"][-1],1,0)
    grid.addWidget(widgets["button"][-1], 2, 0)
    grid.addWidget(widgets["calender"][-1], 3, 0)
def back_to_select(type):
    clear_widgets()
    select_frame(type)
def imprimer_daily_bill(clients,suppliers,total_reglement,items_total,date_now):
    doc = SimpleDocTemplate("daily.pdf", pagesize=letter, leftMargin=28.35, rightMargin=28.35, topMargin=28.35,bottomMargin=28.35)
    story = []
    table_width = doc.width * 0.88  # Adjust as needed

    # Company information
    company_info = f"najib sghaier<br/>M.S: 267943/s<br/>TEL: 25 105 888"
    company_paragraph = Paragraph(company_info, getSampleStyleSheet()["Normal"])
    story.append(company_paragraph)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space

    # Facture and Client name

    header_text = f"<font size=15> date {date_now} </font> "
    header_style = ParagraphStyle("HeaderStyle", parent=getSampleStyleSheet()["Normal"], fontSize=12, alignment=0)
    header = Paragraph(header_text, header_style)
    story.append(header)
    story.append(Spacer(1, 0.2 * inch))  # Add a 2-inch space
    # Table data
    j = 0
    total = 0
    all_money_payed = 0
    col_widths = [doc.width * 0.2, doc.width * 0.2,doc.width * 0.17, doc.width * 0.22,doc.width * 0.15, doc.width * 0.15]
    table_data = [["Numéro de téléphone", "Nom complet", "Quantiter", "Nom de l'article", "Règlement", "Date"]]

    if len(clients) > 0:
        i=1
        for clientt in clients:
            table_data.append([str(clientt.phone_number),str(clientt.full_name),"","",money(clientt.bill[0].money_payed),clientt.bill[0].client_bill_date])
            j=0
            for x in clientt.bill[0].commande:
                if j==0:
                    table_data[i][2]=str(x.quantiter)
                    table_data[i][3] =str(x.item_name)
                    j=j+1
                else:
                    table_data.append(["","",str(x.quantiter),str(x.item_name),"",""])
            i=i+1
        table_data.append(["","","","",f"total reglement : {money(str(total_reglement))}",""])

        for item, value in items_total.items():
            table_data.append(["","",str(value),"total "+str(item),"",""])
        table_data.append(["","","","","","fournissours : "])
        i=i+2+len(list(items_total.values()))
        if len(suppliers) > 0:
            for supplierr in suppliers:
                table_data.append(
                    [str(supplierr.id), str(supplierr.name), "", "", money(supplierr.bill[0].money_payed),
                     clientt.bill[0].client_bill_date])
                j=0
                for x in supplierr.bill[0].commande:
                    if j == 0:
                        table_data[i][2] = str(x.quantiter)
                        table_data[i][3] = str(x.item_name)
                        j = j + 1
                    else:
                        table_data.append(["", "", str(x.quantiter), str(x.item_name), "", ""])
                i=i+1







    # Table style for all cells except last two rows and last three columns
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ("ALIGN", (0, 0), (-1, -2), "CENTER"),  # Center align all cells except last 3 rows
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold font for header row
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Add padding to the header row
            ("BACKGROUND", (0, 1), (-1, -3), colors.beige),  # Row background color
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            # Add border lines to all cells except last 3 rows and last 3 columns
            ("LINEBELOW", (0, -2), (-1, -2), 2, colors.black),  # Add a thicker line below the total row
            ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),  # Add a thicker line below the remaining amount row
        ]
    )


    table_width = doc.width * 0.91  # Adjust as needed

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(table_style)
    # Apply the no_grid_style to remove grid lines for the last two rows and last three columns
    story.append(table)

    # Build the document and save the PDF file
    doc.build(story, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)

    imprimer("daily.pdf")
    pass
def show_dayly_bill_frame(clients,suppliers,k,type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : back_to_select(type))

    imprimer = create_button("imprimer")
    widgets["button"].append(back)
    back.clicked.connect(lambda: back_to_select(type))

    if type!="all":
        back_main = create_button("Retour à l'accueil")
        widgets["back_to_main"].append(back_main)
        back_main.clicked.connect(back_to_main)
    else:
        imprimer = create_button("imprimer")
        widgets["back_to_main"].append(imprimer)
        imprimer.clicked.connect(lambda: imprimer_daily_bill(clients,suppliers,total_reglement,items_total,clients[0].bill[0].client_bill_date))
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(k + 6)
    row_cownt=k + 6
    tableWidget.setColumnCount(7)
    tableWidget.setItem(0, 0, QTableWidgetItem("Numéro de téléphone"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Nom complet"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Nom de l'article"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Règlement"))
    tableWidget.setItem(0, 6, QTableWidgetItem("Règlement type"))
    tableWidget.setItem(0, 5, QTableWidgetItem("Date"))
    items_total={}
    i = 1
    print(k)
    total_reglement=0
    if len(clients)>0:
        for clientt in clients :
            print("test",i)
            print(clientt.full_name,(money(clientt.bill[0].money_payed)))
            print(clientt.cin)
            tableWidget.setItem(i, 0, QTableWidgetItem(clientt.phone_number))
            tableWidget.setItem(i, 1, QTableWidgetItem(clientt.full_name))
            tableWidget.setItem(i, 5, QTableWidgetItem(clientt.bill[0].client_bill_date))
            tableWidget.setItem(i, 4, QTableWidgetItem(money(clientt.bill[0].money_payed)))
            tableWidget.setItem(i, 6, QTableWidgetItem(clientt.bill[0].money_type))
            total_reglement=total_reglement+int(clientt.bill[0].money_payed)
            test_t=i
            for x in clientt.bill[0].commande:

                if float(x.quantiter)>0:
                    tableWidget.setItem(i, 2, QTableWidgetItem(str(float(x.quantiter))))
                else :
                    tableWidget.setItem(i, 2, QTableWidgetItem("reteur "+str(float(float(x.quantiter)*-1))))
                tableWidget.setItem(i, 3, QTableWidgetItem(x.item_name))
                if x.item_name not in items_total :
                    items_total[x.item_name]=float(x.quantiter)
                else:
                    items_total[x.item_name]=items_total[x.item_name]+float(x.quantiter)

                i = i + 1
            if test_t==i:
                i=i+1
            print(i)
            if i==0:
                i=i+1

        i=i+1
    else:
        i=1
    if type=="all":
        tableWidget.setRowCount(row_cownt+len(list(items_total.values())))

        tableWidget.setItem(i, 3, QTableWidgetItem(f"total reglement : {money(str(total_reglement))}"))
        j=1
        for item,value in items_total.items():
            tableWidget.setItem(i+j, 2, QTableWidgetItem(item))
            tableWidget.setItem(i+j, 3, QTableWidgetItem(str(value)))
            j=j+1
        tableWidget.setItem(i+j, 5, QTableWidgetItem("Fournisseurs : "))
        i=i+2+j
    if len(suppliers)>0:
        for supplierr in suppliers :
            tableWidget.setItem(i, 0, QTableWidgetItem(supplierr.id))
            tableWidget.setItem(i, 1, QTableWidgetItem(supplierr.name))
            tableWidget.setItem(i , 5, QTableWidgetItem(supplierr.bill[0].bill_date))
            tableWidget.setItem(i , 4, QTableWidgetItem(money(supplierr.bill[0].money_payed)))
            test_s=i
            print(i,"date")
            for x in supplierr.bill[0].commande:
                tableWidget.setItem(i, 2, QTableWidgetItem(str(int(float(x.quantiter)))))
                tableWidget.setItem(i, 3, QTableWidgetItem(x.item_name))
                i=i+1
            print(i,"payment")
            if i-1==0:
                i=i+1
            if test_s==i:
                i=i+1


    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    widgets["table"].append(tableWidget)

    grid.addWidget(widgets["table"][-1], 1, 0)
    grid.addWidget(widgets["back_to_main"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
def declare_case_frame():
    clear_widgets()
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    price_label = QLabel("perte quantiter: ")
    price_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(price_label)

    item_label = QLabel("Nom de l'article : ")
    item_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["label"].append(item_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)

    items_name = items.get_items_names()
    item_entry = QComboBox()
    item_entry.setStyleSheet(ch)
    item_entry.addItems(items_name)
    widgets["id_entry"].append(item_entry)

    conferm = create_button("Valider ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_item_stock_2(item_entry.currentText(), stock_entry))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["stock_label"][-1], 2, 0)
    grid.addWidget(widgets["stock_entry"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)

def show_items_frame():
    clear_widgets()
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)
    all_items=items.create_items()

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_items) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("Nom de l'article"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Prix"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Stock"))


    for i, item in enumerate(all_items, start=1):
        tableWidget.setItem(i, 0, QTableWidgetItem(item.item_name))
        tableWidget.setItem(i, 1, QTableWidgetItem(money(str(item.item_price))))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(item.item_stocks)))

    ch = "border: 1px solid '#5B2A86';" \
         "border-radius: 15px;" \
         "font-size: " + font_size + "px;" \
                                     "color: '#5B2A86';" \
                                     "padding: 10px 0;" \
                                     "margin: 10px 10px ;" \
                                     "selection-background-color: '#5B2A86';" \
                                     "selection-color: white;"
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    widgets["table"].append(tableWidget)


    grid.addWidget(widgets["table"][-1], 1, 0)

    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 2, 0)

def update_frame():#this function is for creating update frame
    update_acces=create_button("Mise à jour du prix ")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(update_price_fn)

    update_image=create_button("Mise à jour du stock ")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(update_stock_fn)

    declace_case=create_button("Déclarer perte ")
    widgets["door_cces"].append(declace_case)
    declace_case.clicked.connect(declare_case_frame)

    show_items = create_button("tous les articles informations  ")
    widgets["explain_label"].append(show_items)
    show_items.clicked.connect(show_items_frame)

    update_name = create_button("Mise a jour name ")
    widgets["full_name"].append(update_name)
    update_name.clicked.connect(update_item_name_fn)

    back=create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 1, 0)
    grid.addWidget(widgets["update_image"][-1], 2, 0)
    grid.addWidget(widgets["door_cces"][-1], 3, 0)
    grid.addWidget(widgets["full_name"][-1], 4, 0)
    grid.addWidget(widgets["explain_label"][-1], 5, 0)
    grid.addWidget(widgets["button"][-1],0,0)
def search_for_supplier_frame():



    update_acces = create_button("Recherche par nom complet")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(lambda :search_name_fn("Full name"))

    update_image = create_button("Recherche par numéro de téléphone ")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(lambda :search_name_fn("Cin"))


    select_date_2=create_button("Sélectionner la date ")
    widgets["select_button"].append(select_date_2)
    select_date_2.clicked.connect(lambda: select_date("supplier"))


    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 1, 0)
    grid.addWidget(widgets["update_image"][-1], 2, 0)
    grid.addWidget(widgets["select_button"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
def search_for_client_frame(type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    welcome = QLabel("welcome to search for client " + type)
    welcome.setStyleSheet(ch)
    widgets["explain_label"].append(welcome)


    update_acces = create_button("Recherche par nom complet ")
    widgets["update_acces"].append(update_acces)
    update_acces.clicked.connect(lambda :search_full_name_fn("Full name",type))

    update_image = create_button("Recherche par numéro de téléphone")
    widgets["update_image"].append(update_image)
    update_image.clicked.connect(lambda :search_full_name_fn("Cin",type))



    phone_label = create_button("Recherche avec filtres")
    widgets["search_client_bill"].append(phone_label)
    phone_label.clicked.connect(search_with_filter_fn)

    select_date_2 = create_button("Sélectionner la date ")
    widgets["select_button"].append(select_date_2)
    select_date_2.clicked.connect(lambda: select_date("client"))

    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    grid.addWidget(widgets["update_acces"][-1], 1, 0)
    grid.addWidget(widgets["update_image"][-1], 2, 0)
    if type=="bill":
        grid.addWidget(widgets["search_client_bill"][-1], 3, 0)
        grid.addWidget(widgets["select_button"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
def update_price_frame():#this function is for creating update full name frame
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)


    price_label=QLabel("nouveau prix: ")
    price_label.setStyleSheet("font-size: "+font_size+"px;"+"color:'#5B2A86'")
    widgets["price_label"].append(price_label)

    item_label=QLabel("nom de l'article: ")
    item_label.setStyleSheet("font-size: "+font_size+"px;"+"color:'#5B2A86'")
    widgets["label"].append(item_label)

    price_entry=QLineEdit()
    price_entry.setObjectName("price_entry")
    price_entry.setStyleSheet(ch)
    widgets["price_entry"].append(price_entry)

    items_name = items.get_items_names()
    item_entry =QComboBox()
    item_entry.setStyleSheet(ch)
    item_entry.addItems(items_name)

    widgets["id_entry"].append(item_entry)

    conferm=create_button("Valider ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda : confirm_item_price(item_entry.currentText(),price_entry))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["price_label"][-1], 2, 0)
    grid.addWidget(widgets["price_entry"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)

def update_item_name_frame():#this function is for creating update full name frame
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)


    price_label=QLabel("nouveau nom: ")
    price_label.setStyleSheet("font-size: "+font_size+"px;"+"color:'#5B2A86'")
    widgets["price_label"].append(price_label)

    item_label=QLabel("nom de l'article: ")
    item_label.setStyleSheet("font-size: "+font_size+"px;"+"color:'#5B2A86'")
    widgets["label"].append(item_label)

    price_entry=QLineEdit()
    price_entry.setObjectName("price_entry")
    price_entry.setStyleSheet(ch)
    widgets["price_entry"].append(price_entry)

    items_name = items.get_items_names()
    item_entry =QComboBox()
    item_entry.setStyleSheet(ch)
    item_entry.addItems(items_name)

    widgets["id_entry"].append(item_entry)

    conferm=create_button("Valider ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda : confirm_item_name(item_entry.currentText(),price_entry))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["price_label"][-1], 2, 0)
    grid.addWidget(widgets["price_entry"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)
def search_filter_date(all_client,table):
    for clientt in all_client:
        cin = clientt.cin
        cursor.execute(f"select money_payed,client_bill_id,client_bill_date from client_bill where cin={cin} order by client_bill_date")
        print(f"select money_payed,client_bill_id,client_bill_date from client_bill where cin={cin} order by client_bill_date")
        l = []
        money_given = 0
        last_date=""
        for x in cursor:
            l.append(f"select quantiter_price from commande_client where client_bill_id={x[1]}")
            money_given = money_given + int(x[0])
            last_date=str(x[2])
        print(last_date)
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
    table.setColumnCount(6)
    table.setItem(i, 2, QTableWidgetItem("Total"))
    table.setItem(i, 3, QTableWidgetItem("Règlement"))
    table.setItem(i, 4, QTableWidgetItem("remain"))
    table.setItem(i, 5, QTableWidgetItem("Date de la dernière facture"))
    for clientt in all_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))

        table.setItem(i, 2, QTableWidgetItem(money(str(clientt.total_money))))
        table.setItem(i, 3, QTableWidgetItem(money(str(clientt.money_given))))
        table.setItem(i, 4, QTableWidgetItem(money(str(clientt.rest))))
        table.setItem(i, 5, QTableWidgetItem(str(clientt.last_bill_date)))
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
    table.setItem(i, 2, QTableWidgetItem("Total"))
    table.setItem(i, 3, QTableWidgetItem("Règlement"))
    table.setItem(i, 4, QTableWidgetItem("remain"))
    for clientt in all_client:
        i = i + 1
        table.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        table.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))

        table.setItem(i, 2, QTableWidgetItem(money(str(clientt.total_money))))
        table.setItem(i, 3, QTableWidgetItem(money(str(clientt.money_given))))
        table.setItem(i, 4, QTableWidgetItem(money(str(clientt.rest))))
    table.resizeColumnsToContents()
def search_with_filter_fn():
    clear_widgets()
    search_with_filter()

def search_with_filter():
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda  : search_for_client_fn('bill'))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    all_client = client.create_clients()

    tableWidget = QTableWidget()

    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(2)
    tableWidget.setItem(0, 0, QTableWidgetItem("Numéro de téléphone du client"))
    tableWidget.setItem(0, 1, QTableWidgetItem("nom complet du client"))
    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.cin)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1600)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.doubleClicked.connect(lambda: select_client_profile( lil, "filter",-1,"",""))
    widgets["table"].append(tableWidget)
    lil=[tableWidget]
    filter_money = create_button("Money remain")
    widgets["confirm"].append(filter_money)
    filter_money.clicked.connect(lambda: search_filter_money_rest(all_client, tableWidget))

    filter_date = create_button("date ")
    widgets["money_entry"].append(filter_date)
    filter_date.clicked.connect(lambda: search_filter_date(all_client, tableWidget))

    grid.addWidget(widgets["table"][-1], 1, 0)
    grid.addWidget(widgets["money_entry"][-1], 2, 0)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)
def client_devis_frame(all_bills,all_commande,type,name,phone_number):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)



    back.clicked.connect(lambda: search_full_name_fn(type, 'devis'))


    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)
    welcome_label = QLabel(name)
    welcome_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)
    nbr_rows = 0
    for x in all_commande:
        nbr_rows = nbr_rows + len(x)
    nbr_rows = nbr_rows + len(all_commande)
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(nbr_rows + 4)
    tableWidget.setColumnCount(6)
    tableWidget.setItem(0, 0, QTableWidgetItem("Montant"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Prix de l'unité"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Article"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Quantiter"))

    tableWidget.setItem(0, 4, QTableWidgetItem("Date"))
    tableWidget.setItem(0, 5, QTableWidgetItem("Commande code "))

    i = 0
    j = 0
    total = 0
    for commande in all_commande:
        for x in commande:
            i = i + 1
            tableWidget.setItem(i, 5, QTableWidgetItem(str(all_bills[j].client_devis_id)))
            tableWidget.setItem(i, 4, QTableWidgetItem(str(all_bills[j].client_bill_date)))
            tableWidget.setItem(i, 0, QTableWidgetItem(money(str(x.quantiter_price))))
            if int(x.quantiter_price) > 0:
                item_price = int(float(x.quantiter_price) / float(x.quantiter))
            else:
                item_price = 0

            tableWidget.setItem(i, 1, QTableWidgetItem(money(str(item_price))))
            tableWidget.setItem(i, 2, QTableWidgetItem(str(x.item_name)))
            if float(x.quantiter) < 0:
                tableWidget.setItem(i, 3, QTableWidgetItem("reteur " + str(float(float(x.quantiter) * -1))))
            else:
                tableWidget.setItem(i, 3, QTableWidgetItem(str(x.quantiter)))

            total = total + int(x.quantiter_price)


        i = i + 1
        j = j + 1
    tableWidget.setItem(i + 1, 1, QTableWidgetItem("Total"))
    print("test 1")

    tableWidget.setItem(i + 1, 2, QTableWidgetItem(money(str(total))))

    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.setFixedHeight(500)
    # tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    cursor.execute("select devis_code from global_variable ")
    id = 1
    for x in cursor:
        id = int(x[0])
    # generate_bill("devis\\devis " + make_windows_friendly_filename(name) +str(id) +".pdf", str(id), name, phone_number, all_bills,
    #                   all_commande,'devis',0)
    # cursor.execute("UPDATE global_variable set devis_code=devis_code+1 ")
    # connection.commit()

    imprimer_devis = create_button("imprimer devis")
    imprimer_devis.clicked.connect(lambda : generate_bill("devis\\devis " + make_windows_friendly_filename(name) +str(id) +".pdf", str(id), name, phone_number, all_bills,
                      all_commande,'devis',[]))


    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content_widget = QWidget()
    scroll_area.setWidget(scroll_content_widget)
    widgets["scroll"].append(scroll_area)

    widgets["table"].append(tableWidget)
    scroll_grid = QGridLayout(scroll_content_widget)
    scroll_grid.addWidget(widgets["label"][-1], 1, 0, 1, 3)
    scroll_grid.addWidget(widgets["table"][-1], 2, 0, 1, 3)
    scroll_grid.addWidget(imprimer_devis,3,1)


    scroll_grid.addWidget(widgets["button"][-1], 0, 0)
    scroll_grid.addWidget(widgets["back_to_main"][-1], 3, 0)


    grid.addWidget(widgets["scroll"][-1], 0, 0)
def get_variable(cin,type):
    all_bills=bill.create_bills(cin)
    all_commande = []
    all_dates_money = []
    all_dates_with_code = []
    for billl in all_bills:
        bill_id = billl.client_bill_id
        all_commande.append(commande_client.create_commande_client(bill_id))
        all_dates_money.append(
            str(billl.client_bill_date) + " : " + str(billl.client_bill_id) + " : " + str(money(billl.money_payed)))
        all_dates_with_code.append(str(billl.client_bill_date) + " : " + str(billl.client_bill_id))
    if type=="money":
        return all_dates_money
    else:
        all_commande_by_date = {}
        j = 0
        for commande in all_commande:
            commande_list = []
            commande_tupple = []
            for x in commande:
                commande_list.append(str(x.item_name) + "  :  " + str(x.quantiter))
                commande_tupple.append((str(x.item_name), str(x.quantiter), str(x.quantiter_price)))
            all_commande_by_date[str(all_bills[j].client_bill_date) + " : " + str(all_bills[j].client_bill_id)] = {
                "list": commande_list, "tuple": commande_tupple, "id": all_bills[j].client_bill_id}
        return all_commande_by_date,all_dates_with_code
def imprimer(file):
    webbrowser.open(file,new=2)
def get_remize_total(all_remize):
    remize_total=0
    for remize in all_remize:
        remize_total=remize_total+ int(remize.quantiter)
    return remize_total
def client_bills_frame(all_bills,all_commande,type,name,phone_number,cin):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    all_remize=Remise.get_remize(str(cin))
    remize_total=get_remize_total(all_remize)

    all_dates_money = []
    all_dates_with_code=[]
    all_dates_money_type=[]
    for billl in all_bills:
        all_dates_money.append(str(billl.client_bill_date)+" : "+str(billl.client_bill_id)+" : "+str(money(billl.money_payed)))
        all_dates_with_code.append(str(billl.client_bill_date)+" : "+str(billl.client_bill_id))
        all_dates_money_type.append(str(billl.client_bill_date)+" : "+str(billl.client_bill_id)+" : "+str(money(billl.money_payed))+" : "+str(billl.money_type))


    if type!="filter":
      back.clicked.connect(lambda : search_full_name_fn(type,'bill'))
    else:
      back.clicked.connect(search_with_filter_fn)


    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)
    welcome_label = QLabel(name)
    welcome_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)
    nbr_rows=0
    for x in all_commande:
        nbr_rows=nbr_rows+len(x)
    nbr_rows=nbr_rows+len(all_commande)
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(nbr_rows + 6)
    tableWidget.setColumnCount(7)
    tableWidget.setItem(0, 0, QTableWidgetItem("Montant"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Prix de l'unité"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Article"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Règlement"))
    tableWidget.setItem(0, 5, QTableWidgetItem("Date"))
    tableWidget.setItem(0,7,QTableWidgetItem("Commande code "))
    tableWidget.setItem(0, 6, QTableWidgetItem("reglement type"))


    i = 0
    get_remize = [0]
    j=0
    total=0
    all_money_payed=0
    all_commande_by_date={}
    all_items_total_quantiter={}
    for commande in all_commande:
        commande_list=[]
        commande_tupple=[]
        for x in commande:
            i=i+1
            tableWidget.setItem(i,7,QTableWidgetItem(str(all_bills[j].client_bill_id)))
            tableWidget.setItem(i, 5, QTableWidgetItem(str(all_bills[j].client_bill_date)))
            tableWidget.setItem(i, 0, QTableWidgetItem(money(str(x.quantiter_price))))
            if int(x.quantiter_price)!=0:
               item_price=int(float(x.quantiter_price)/float(x.quantiter))
            else:
                item_price=0

            tableWidget.setItem(i, 1, QTableWidgetItem(money(str(item_price))))
            tableWidget.setItem(i, 2, QTableWidgetItem(str(x.item_name)))
            if str(x.item_name) not in all_items_total_quantiter:
                all_items_total_quantiter[str(x.item_name)]={"quantiter":float(x.quantiter),"quantiter_price":int(x.quantiter_price)}
            else:
                all_items_total_quantiter[str(x.item_name)]["quantiter"] +=float(x.quantiter)
                all_items_total_quantiter[str(x.item_name)]["quantiter_price"]+=int(x.quantiter_price)
            if float(x.quantiter)<0:
                tableWidget.setItem(i, 3, QTableWidgetItem("reteur "+str(float(float(x.quantiter)*-1))))
            else:
                tableWidget.setItem(i, 3, QTableWidgetItem(str(x.quantiter)))
            commande_list.append(str(x.item_name)+"  :  "+str(x.quantiter))
            commande_tupple.append((str(x.item_name),str(x.quantiter),str(x.quantiter_price)))
            total=total+int(x.quantiter_price)
        all_commande_by_date[str(all_bills[j].client_bill_date)+" : "+str(all_bills[j].client_bill_id)]={"list":commande_list,"tuple":commande_tupple,"id":all_bills[j].client_bill_id}
        tableWidget.setItem(i+1, 4, QTableWidgetItem(money(str(all_bills[j].money_payed))))
        tableWidget.setItem(i + 1, 6, QTableWidgetItem(str(all_bills[j].money_type)))
        tableWidget.setItem(i+1, 5, QTableWidgetItem(str(all_bills[j].client_bill_date)))
        tableWidget.setItem(i+1, 7, QTableWidgetItem(str(all_bills[j].client_bill_id)))
        all_money_payed=all_money_payed+int(all_bills[j].money_payed)
        i=i+1
        j=j+1
    tableWidget.setItem(i+1, 1, QTableWidgetItem("Total"))
    tableWidget.setItem(i+2, 1, QTableWidgetItem("total Règlement"))
    tableWidget.setItem(i + 3, 1, QTableWidgetItem("remize"))
    tableWidget.setItem(i+4, 1, QTableWidgetItem("remain"))

    tableWidget.setItem(i+1, 2, QTableWidgetItem(money(str(total))))
    tableWidget.setItem(i+2, 2, QTableWidgetItem(money(str(all_money_payed))))
    tableWidget.setItem(i+3, 2, QTableWidgetItem(money(str(remize_total))))
    tableWidget.setItem(i+4, 2, QTableWidgetItem(money(str(total-(all_money_payed+remize_total)))))

    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.setFixedHeight(500)
    #tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    try:
        generate_bill("facture_detaillee\\facture "+make_windows_friendly_filename(name)+".pdf", str(all_bills[0].client_bill_id), name, phone_number, all_bills, all_commande,"bill",all_remize)
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    update_item_date = create_button("change l'article date")
    widgets["door_cces"].append(update_item_date)
    update_item_date.clicked.connect(lambda : update_item_date_fn(all_dates_with_code,all_commande_by_date,cin,name,phone_number,"date",type))

    choosing_date = create_button("choose date for facture")

    choosing_date.clicked.connect(
        lambda: chosing_date_for_facture_fn(all_dates_with_code, all_bills,all_commande, cin, name, phone_number,all_remize,type))

    update_item_quantieter = create_button("change l'article quantiter")
    update_item_quantieter.clicked.connect(
        lambda: update_item_date_fn(all_dates_with_code, all_commande_by_date, cin, name, phone_number,"quantier",type))

    change_date = create_button("modifier date")
    change_date.clicked.connect(lambda: change_date_fn(name, all_dates_with_code, cin,all_commande_by_date,phone_number,type))
    widgets["Create_supplier_bill"].append(change_date)

    change_money=create_button("Update Reglement")
    change_money.clicked.connect(lambda : update_item_money_fn(all_dates_money,cin,name,phone_number,type))
    widgets["phone_entry"].append(change_money)

    change_money_type = create_button("Update Reglement Type")
    change_money_type.clicked.connect(lambda: update_item_money_type_fn(all_dates_money_type, cin, name, phone_number, type))
    widgets["logo"].append(change_money_type)

    update_client = create_button("Changer client information")
    update_client.clicked.connect(lambda: update_client_fn(cin, name, phone_number,type))
    widgets["search_client_bill"].append(update_client)

    annuler_commande = create_button("Annuler commande")
    annuler_commande.clicked.connect(lambda: annuler_commande_fn(all_dates_with_code,cin,name,phone_number,type))

    show_remize = create_button("Show all remize")
    show_remize.clicked.connect(lambda: show_remize_fn(all_remize, cin, name, phone_number, type))

    remize = create_button("Remise exceptionnelle")
    remize.clicked.connect(lambda: remise_fn(cin, name, phone_number,all_bills,all_commande,type))

    bonde_reglement = create_button("Get bonde de reglement")
    cursor.execute("select bonde_reglement from global_variable ")
    id = 1
    for x in cursor:
        id = int(x[0])
    print(id)

    bonde_reglement.clicked.connect(lambda: generate_bonde_reglemen(f"reglement\\bonde_de_reglment {id} "+make_windows_friendly_filename(name)+".pdf",id,name,phone_number,all_bills))
    widgets["update_button"].append(bonde_reglement)
    try:
        generate_total_bill(f"facture\\facture {all_bills[0].client_bill_id} " + make_windows_friendly_filename(name) + ".pdf", all_bills[0].client_bill_id, name, phone_number,
                                            all_items_total_quantiter,all_money_payed,remize_total)

    except Exception as e :
        print(e)

    print(get_remize)
    cursor.execute("select bonde_reteur from global_variable ")
    id = 1
    for x in cursor:
        id = int(x[0])
    print(id)
    bonde_reteur = create_button("Bonde de reteur")
    bonde_reteur.clicked.connect(lambda: generate_bill_reteur("reteur\\bonde_de_reteur_id "+str(id)+"  client "+make_windows_friendly_filename(name)+".pdf", str(id), name, phone_number, all_bills, all_commande))


    bonde_sortie = create_button("Bonde de sortie")
    bonde_sortie.clicked.connect(
        lambda: generate_bill_only_take("sortie\\bonde_de_sortie_id " + str(all_bills[-1].client_bill_id) + "  client " + make_windows_friendly_filename(name) + ".pdf",all_bills[-1].client_bill_id,name,phone_number,all_bills,all_commande))

    facture = create_button("imprimer facture")
    facture.clicked.connect(lambda : imprimer(f"facture\\facture {all_bills[0].client_bill_id} " + make_windows_friendly_filename(name) + ".pdf"))

    facture_detaillee = create_button("imprimer facture detaillée")
    facture_detaillee.clicked.connect(lambda : imprimer("facture_detaillee\\facture "+make_windows_friendly_filename(name)+".pdf"))

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content_widget = QWidget()
    scroll_area.setWidget(scroll_content_widget)
    widgets["scroll"].append(scroll_area)

    widgets["table"].append(tableWidget)
    scroll_grid = QGridLayout(scroll_content_widget)
    scroll_grid.addWidget(widgets["label"][-1],1,0,1,3)
    scroll_grid.addWidget(widgets["table"][-1],2,0,1,3)
    scroll_grid.addWidget(widgets["Create_supplier_bill"][-1],3,0)
    scroll_grid.addWidget(widgets["door_cces"][-1],3,1)
    scroll_grid.addWidget(widgets["phone_entry"][-1],3,2)
    scroll_grid.addWidget(update_client,4,2)
    scroll_grid.addWidget(widgets["button"][-1],0,0,1,3)
    scroll_grid .addWidget(widgets["back_to_main"][-1],7,0)
    scroll_grid.addWidget(widgets["logo"][-1], 7, 2)
    scroll_grid.addWidget(remize,6,0)
    scroll_grid.addWidget(facture,6,1)
    scroll_grid.addWidget(facture_detaillee,6,2)
    scroll_grid.addWidget(bonde_reglement,5,0)
    scroll_grid.addWidget(annuler_commande,4,1)
    scroll_grid.addWidget(bonde_reteur,5,1)
    scroll_grid.addWidget(bonde_sortie, 5, 2)
    scroll_grid.addWidget(update_item_quantieter,4,0)
    scroll_grid.addWidget(choosing_date, 7,1)
    scroll_grid.addWidget(show_remize, 8,0)

    grid.addWidget(widgets["scroll"][-1],0,0)


def supplier_bills_frame(all_bills,all_commande,type,name):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : search_name_fn(type))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)
    nbr_rows=0
    welcome_label = QLabel(name)
    welcome_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)
    for x in all_commande:
        nbr_rows=nbr_rows+len(x)
    nbr_rows=nbr_rows+len(all_commande)
    tableWidget = QTableWidget()
    tableWidget.resizeColumnsToContents()
    tableWidget.setRowCount(nbr_rows + 4)
    tableWidget.setColumnCount(5)
    tableWidget.setItem(0, 0, QTableWidgetItem("Montant "))
    tableWidget.setItem(0, 1, QTableWidgetItem("Article"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Règlement"))
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
    tableWidget.setItem(i+2, 1, QTableWidgetItem("total Règlement"))
    tableWidget.setItem(i+3, 1, QTableWidgetItem("remain"))

    tableWidget.setItem(i+1, 2, QTableWidgetItem(money(str(total))))
    tableWidget.setItem(i+2, 2, QTableWidgetItem(money(str(all_money_payed))))
    tableWidget.setItem(i+3, 2, QTableWidgetItem(money(str(total-all_money_payed))))




    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #tableWidget.doubleClicked.connect(lambda: select_worker(tableWidget, users, date))
    widgets["table"].append(tableWidget)

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["table"][-1], 2, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 3, 0)

def update_stock_frame():#this function is for creating update full name frame
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(update_worker)

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    price_label = QLabel("Nouveau stock : ")
    price_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(price_label)

    item_label = QLabel("nom de l'article : ")
    item_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["label"].append(item_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)

    items_name = items.get_items_names()
    item_entry = QComboBox()
    item_entry.setEditable(True)
    item_entry.setStyleSheet(ch)
    item_entry.addItems(items_name)
    widgets["id_entry"].append(item_entry)

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_item_stock(item_entry.currentText(), stock_entry))

    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["id_entry"][-1], 1, 1)
    grid.addWidget(widgets["stock_label"][-1], 2, 0)
    grid.addWidget(widgets["stock_entry"][-1], 2, 1)
    grid.addWidget(widgets["confirm"][-1], 3, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)
def search_full_name_fn(type,type_2):
    clear_widgets()
    search_full_name_frame(type,type_2)
def search_name_fn(type):
    clear_widgets()
    search_name_frame(type)


def change_date_fn(name,all_dates,cin,ids,phone_number,reteur_type):
    clear_widgets()
    change_date_frame(name,all_dates,cin,ids,phone_number,reteur_type)
def change_date_frame(name,all_dates,cin,ids,phone_number,reteur_type):
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;" + "selection-background-color: #5B2A86;" + "selection-color: white;"

    back_to_mainn=create_button("Reteur au accuer")

    back_to_mainn.clicked.connect(back_to_main)
    widgets["back_to_main"].append(back_to_mainn)

    back=create_button("Retour")
    back.clicked.connect(lambda : select_client_profile(None,reteur_type,int(cin),name,phone_number))
    widgets["back"].append(back)
    welcome_label = QLabel("modifier commande date pour client "+name)
    welcome_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)

    welcome_date = QLabel("old date ")
    welcome_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    welcome_date.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_date)

    old_date = QComboBox()
    old_date.setStyleSheet(ch)
    old_date.addItems(all_dates)
    widgets["id_entry"].append(old_date)

    new_date = QLabel("New date ")
    new_date.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
    new_date.setAlignment(QtCore.Qt.AlignCenter)
    widgets["select_button"].append(new_date)

    new_date_entry = QLineEdit(str(date.today()))
    new_date_entry.setStyleSheet(ch)
    widgets["calender"].append(new_date_entry)

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(
        lambda: confirm_change_client_commande_date(old_date.currentText(),new_date_entry.text(),ids,cin,name,phone_number,reteur_type))
    grid.addWidget(widgets["label"][-1], 1, 0)
    grid.addWidget(widgets["explain_label"][-1], 2, 0)
    grid.addWidget(widgets["id_entry"][-1], 3,0 )
    grid.addWidget(widgets["select_button"][-1], 4, 0)
    grid.addWidget(widgets["calender"][-1], 5, 0)
    grid.addWidget(widgets["confirm"][-1], 6, 0)
    grid.addWidget(widgets["back"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 7, 0)


def create_client_bill_frame(type):
    def filterNames(text):
        name_model.clear()

        if text:
            matching_items = [thing.full_name for thing in all_client if text.lower() in thing.full_name.lower() or text==""]

            for item in matching_items:
                name_model.appendRow(QStandardItem(item))

            name_list_view.show()
            if len(matching_items) == 0:
                name_list_view.hide()
        else:
            matching_items=[thing.full_name for thing in all_client]
            for item in matching_items:
                name_model.appendRow(QStandardItem(item))

            name_list_view.show()
            if len(matching_items) == 0:
                name_list_view.hide()
            # name_list_view.hide()
            # full_name_entry.clear()

        name_list_view.setCurrentIndex(name_model.index(0, 0))

    def filterPhoneNumbers(text):
        phone_model.clear()

        if text:
            matching_items = [thing.phone_number for thing in all_client if text in thing.phone_number or text==""]

            for item in matching_items:
                phone_model.appendRow(QStandardItem(item))

            phone_list_view.show()
            if len(matching_items) == 0:
                phone_list_view.hide()
        else:
            phone_list_view.hide()
            full_name_entry.clear()

        phone_list_view.setCurrentIndex(phone_model.index(0, 0))

    def updateInputsFromName(index):
        selected_name = name_model.data(index, Qt.DisplayRole)
        full_name_entry.setText(selected_name)

        for thing in all_client:
            if thing.full_name == selected_name:
                cin_entry.setText(str(thing.phone_number))

        name_list_view.hide()
        phone_list_view.hide()

    def updateInputsFromPhone(index):
        selected_phone = phone_model.data(index, Qt.DisplayRole)
        cin_entry.setText(selected_phone)

        for thing in all_client:
            if thing.phone_number == selected_phone:
                full_name_entry.setText(thing.full_name)

        phone_list_view.hide()
        name_list_view.hide()

    def sortTableByName(tablewidget):
        # Get the search term from the QLineEdit
        search_term = search_line_edit.text().strip()

        # Create a list to store rows matching the search term
        matching_rows = []

        # Iterate through all rows in the table
        for row in range(1, tableWidget.rowCount()):
            name_item = tableWidget.item(row, 0)  # Assuming the name is in the first column (column index 0)
            name = name_item.text()

            # Check if the name contains the search term (case-insensitive)
            if search_term.lower() in name.lower():
                matching_rows.append((name, row))
        print(matching_rows)
        try:
            # Rearrange rows in the QTableWidget
            for i, (name, newRow) in enumerate(matching_rows):
                # Remove row from its current position and reinsert it at the desired position
                print(newRow)
                row_data = [tableWidget.item(newRow, col).text() for col in range(tableWidget.columnCount() - 2)]
                lineEdit = tableWidget.cellWidget(newRow, 3)
                if isinstance(lineEdit, QLineEdit):
                    quantiter_text = lineEdit.text()
                else:
                    quantiter_text = "0"
                price = tableWidget.item(newRow, 4).text()
                tableWidget.removeRow(newRow)
                tableWidget.insertRow(i + 1)
                lineEditt = QLineEdit(str(quantiter_text))
                tableWidget.setCellWidget(i + 1, 3, lineEditt)

                for col, itemData in enumerate(row_data):
                    tableWidget.setItem(i + 1, col, QTableWidgetItem(str(itemData)))
                print("quantiter_text", quantiter_text)
                # tableWidget.setItem(i + 1, 3, QTableWidgetItem(str(quantiter_text)))

                tableWidget.setItem(i + 1, 4, QTableWidgetItem(str(price)))
            ch = "border: 1px solid '#5B2A86';" \
                 "border-radius: 15px;" \
                 "font-size: " + font_size + "px;" \
                                             "color: '#5B2A86';" \
                                             "padding: 10px 0;" \
                                             "margin: 10px 10px ;" \
                                             "selection-background-color: '#5B2A86';" \
                                             "selection-color: white;"
            tableWidget.setStyleSheet(ch)
            tableWidget.resizeColumnsToContents()
            tableWidget.resizeRowsToContents()
            tableWidget.setFixedHeight(400)




        except Exception as e:
            print(e)

        print('test')
    if type=="reteur":
        welcome_label = QLabel("Créer une nouvelle facture de reteur")
    elif type=="bill":
        welcome_label = QLabel("Créer une nouvelle facture " )
    else:
        welcome_label = QLabel("Créer un nouveau devis" )
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)

    # ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: " + font_size + "px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;" + "selection-background-color: #5B2A86;" + "selection-color: white;"

    all_client=client.create_clients()

    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    name_list_view = QListView()
    name_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
    name_list_view.setStyleSheet(ch)
    name_list_view.setFixedHeight(200)
    widgets["name_list_view"].append(name_list_view)

    name_model = QStandardItemModel()
    name_list_view.setModel(name_model)

    date_entry = QLineEdit()
    date_entry.setStyleSheet(ch)
    date_entry.setText(str(date.today()))

    cin_entry = QLineEdit()
    full_name_entry = QLineEdit()
    cin_entry.setObjectName("Numéro de téléphone")
    cin_entry.setStyleSheet(ch)
    cin_entry.setPlaceholderText("Numéro de téléphone")

    cin_entry.textChanged.connect(filterPhoneNumbers)
    widgets["cin_entry"].append(cin_entry)

    phone_list_view = QListView()
    full_name_entry.setObjectName("full_name_entry")
    full_name_entry.setStyleSheet(ch)
    full_name_entry.setPlaceholderText("full name")
    full_name_entry.textChanged.connect(filterNames)
    widgets["full_name"].append(full_name_entry)

    phone_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
    phone_list_view.setStyleSheet(ch)
    phone_list_view.setFixedHeight(200)
    widgets["phone_list_view"].append(phone_list_view)

    # Create a QStandardItemModel to hold the items for phone numbers
    phone_model = QStandardItemModel()
    phone_list_view.setModel(phone_model)

    matching_items = [thing.full_name for thing in all_client]
    for item in matching_items:
        name_model.appendRow(QStandardItem(item))

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content_widget = QWidget()
    scroll_area.setWidget(scroll_content_widget)
    widgets["scroll"].append(scroll_area)

    welcome_label=QLabel("total :  remain : ")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)

    search_line_edit = QLineEdit()
    search_line_edit.setStyleSheet(ch)
    search_line_edit.setPlaceholderText("Rechercher ..")
    try:
        search_line_edit.textEdited.connect(lambda : sortTableByName(tableWidget))
    except Exception as e:
        print(e)





    money_entry = QLineEdit()
    money_entry.setObjectName("mpney_entry")
    money_entry.setStyleSheet(ch)
    money_entry.setPlaceholderText("Règlement")
    widgets["money_entry"].append(money_entry)

    money_type = QLineEdit()
    money_type.setStyleSheet(ch)
    money_type.setPlaceholderText("Règlement type..")
    widgets["price_entry"].append(money_type)

    all_items = items.create_items()

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    all_items_dict=items.create_dict_items()
    if type!="reteur":
        conferm.clicked.connect(lambda: confirm_create_client_bill(full_name_entry,cin_entry,date_entry.text(),tableWidget,all_items_dict,money_entry,welcome_label,type,money_type))
    else:
        try:
            conferm.clicked.connect(lambda: confirm_create_client_bill(full_name_entry,cin_entry,date_entry.text(),tableWidget,all_items_dict,"0",welcome_label,type,""))
        except Exception as e:
            print(e)
            print(traceback.format_exc())




    # select_date = QCalendarWidget()
    # select_date.setGridVisible(True)
    # select_date.setStyleSheet(ch)
    # widgets["calender"].append(select_date)

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_items)+1)
    tableWidget.setColumnCount(5)
    tableWidget.setItem(0, 0, QTableWidgetItem("Nom de l'article"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Prix"))
    tableWidget.setItem(0, 2, QTableWidgetItem("Stock"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Quantité"))
    tableWidget.setItem(0, 4, QTableWidgetItem("Prix              "))


    for i, item in enumerate(all_items, start=1):
        tableWidget.setItem(i, 0, QTableWidgetItem(item.item_name))
        tableWidget.setItem(i, 1, QTableWidgetItem(money(str(item.item_price))))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(item.item_stocks)))
        tableWidget.setItem(i, 4, QTableWidgetItem("0"))

        # tableWidget.setItem(i, 3, QTableWidgetItem("0"))

        lineEdit = QLineEdit("")
        tableWidget.setCellWidget(i, 3, lineEdit)
    ch = "border: 1px solid '#5B2A86';" \
         "border-radius: 15px;" \
         "font-size: " + font_size + "px;" \
                                     "color: '#5B2A86';" \
                                     "padding: 10px 0;" \
                                     "margin: 10px 10px ;" \
                                     "selection-background-color: '#5B2A86';" \
                                     "selection-color: white;"
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedHeight(400)



    # Set the stylesheet

   # tableWidget.doubleClicked.connect(lambda :select_worker(tableWidget,users,date))
    widgets["table"].append(tableWidget)

    see_total_button = create_button("Total ")
    widgets["see_total"].append(see_total_button)
    if type=="bill":
        see_total_button.clicked.connect(lambda: see_total(all_items_dict, str(money_entry.text()), welcome_label, tableWidget))
        scroll_grid = QGridLayout(scroll_content_widget)
        scroll_grid.addWidget(widgets["label"][-1], 1, 0)
        scroll_grid.addWidget(full_name_entry, 2, 0)
        scroll_grid.addWidget(cin_entry, 2, 1, 1, 3)
        scroll_grid.addWidget(phone_list_view, 3, 1, 1, 3)
        scroll_grid.addWidget(name_list_view, 3, 0)
        scroll_grid.addWidget(date_entry, 1, 1, 1, 3)
        scroll_grid.addWidget(search_line_edit, 4, 0, 1, 3)

        scroll_grid.addWidget(widgets["table"][-1], 5, 0, 1, 2)

        scroll_grid.addWidget(widgets["money_entry"][-1], 6, 1)
        scroll_grid.addWidget(money_type, 6, 2)

        scroll_grid.addWidget(widgets["confirm"][-1], 6, 0)
        scroll_grid.addWidget(widgets["see_total"][-1], 7, 0)
        scroll_grid.addWidget(widgets["button"][-1], 0, 0)
        scroll_grid.addWidget(widgets["explain_label"][-1], 7, 1, 1, 3)
        grid.addWidget(widgets["scroll"][-1], 0, 0)
    else:
        see_total_button.clicked.connect(lambda: see_total(all_items_dict, str(0), welcome_label, tableWidget))
        scroll_grid = QGridLayout(scroll_content_widget)
        scroll_grid.addWidget(widgets["label"][-1], 1, 0)
        scroll_grid.addWidget(full_name_entry, 2, 0)
        scroll_grid.addWidget(cin_entry, 2, 1)
        scroll_grid.addWidget(phone_list_view, 3, 1)
        scroll_grid.addWidget(name_list_view, 3, 0)
        scroll_grid.addWidget(date_entry, 1, 1)
        scroll_grid.addWidget(search_line_edit, 4, 0, 1, 3)

        scroll_grid.addWidget(widgets["table"][-1], 5, 0, 1, 3)
        scroll_grid.addWidget(widgets["confirm"][-1], 6, 0)
        scroll_grid.addWidget(widgets["see_total"][-1], 7, 0)
        scroll_grid.addWidget(widgets["button"][-1], 0, 0)
        scroll_grid.addWidget(widgets["explain_label"][-1], 7, 1)
        grid.addWidget(widgets["scroll"][-1], 0, 0)



    name_list_view.clicked.connect(updateInputsFromName)
    phone_list_view.clicked.connect(updateInputsFromPhone)
    # # grid.addWidget(widgets["label"][-1], 0, 0)
    # grid.addWidget(widgets["full_name"][-1], 0, 0)
    #
    # grid.addWidget(widgets["cin_entry"][-1], 0,1)
    # grid.addWidget(widgets["phone_list_view"][-1],1,0)
    # grid.addWidget(widgets["name_list_view"][-1], 1, 1)
    # grid.addWidget(widgets["table"][-1], 2, 1)
    # grid.addWidget(widgets["money_entry"][-1], 3, 1)
    # grid.addWidget(widgets["calender"][-1], 2, 0)
    # grid.addWidget(widgets["confirm"][-1], 3, 0)
    # grid.addWidget(widgets["see_total"][-1], 4, 0)
    # grid.addWidget(widgets["button"][-1], 4, 2)
    # grid.addWidget(widgets["explain_label"][-1], 4, 1)

def see_total_2(money_payed, welcome_label, table,m):
    if money_payed == "":
        money_payed = "0"
    elif money_payed[0] == "-" or (money_payed[0] != "-" and not money_payed.isdigit()):
        if not money_payed[1:].isdigit():
            money_payed = "0"
    print(money_payed)
    total = 0

    for i in range(1,m+1):
        lineEdit = table.cellWidget(i, 3)
        if isinstance(lineEdit, QLineEdit):
            item_price=str(lineEdit.text())
            if item_price.isdigit():
                total=total+float(item_price)
    rest = total - int(money_payed)
    welcome_label.setText("total : " + money(str(int(total))) + " remain : " + money(str(int(rest))))
def create_supplier_bill_frame():
    def filterNames(text):
        name_model.clear()

        if text:
            matching_items = [thing.name for thing in all_client if text.lower() in thing.name.lower()]

            for item in matching_items:
                name_model.appendRow(QStandardItem(item))

            name_list_view.show()
            if len(matching_items) == 0:
                name_list_view.hide()
        else:
            name_list_view.hide()
            full_name_entry.clear()

        name_list_view.setCurrentIndex(name_model.index(0, 0))

    def filterPhoneNumbers(text):
        phone_model.clear()

        if text:
            matching_items = [thing.phone_number for thing in all_client if text in thing.phone_number]

            for item in matching_items:
                phone_model.appendRow(QStandardItem(item))

            phone_list_view.show()
            if len(matching_items) == 0:
                phone_list_view.hide()
        else:
            phone_list_view.hide()
            full_name_entry.clear()

        phone_list_view.setCurrentIndex(phone_model.index(0, 0))

    def updateInputsFromName(index):
        selected_name = name_model.data(index, Qt.DisplayRole)
        full_name_entry.setText(selected_name)

        for thing in all_client:
            if thing.name == selected_name:
                cin_entry.setText(str(thing.phone_number))

        name_list_view.hide()
        phone_list_view.hide()

    def updateInputsFromPhone(index):
        selected_phone = phone_model.data(index, Qt.DisplayRole)
        cin_entry.setText(selected_phone)

        for thing in all_client:
            if thing.phone_number == selected_phone:
                full_name_entry.setText(thing.name)

        phone_list_view.hide()
        name_list_view.hide()

    def sortTableByName(tablewidget):
        # Get the search term from the QLineEdit
        search_term = search_line_edit.text().strip()

        # Create a list to store rows matching the search term
        matching_rows = []

        # Iterate through all rows in the table
        for row in range(1, tableWidget.rowCount()):
            name_item = tableWidget.item(row, 0)  # Assuming the name is in the first column (column index 0)
            name = name_item.text()

            # Check if the name contains the search term (case-insensitive)
            if search_term.lower() in name.lower():
                matching_rows.append((name, row))
        print(matching_rows)
        try:
            # Rearrange rows in the QTableWidget
            for i, (name, newRow) in enumerate(matching_rows):
                # Remove row from its current position and reinsert it at the desired position
                print(newRow)
                row_data = [tableWidget.item(newRow, col).text() for col in range(tableWidget.columnCount() - 2)]
                lineEdit = tableWidget.cellWidget(newRow, 2)
                if isinstance(lineEdit, QLineEdit):
                    quantiter_text = lineEdit.text()
                else:
                    quantiter_text = "0"
                lineEdit = tableWidget.cellWidget(newRow, 3)
                if isinstance(lineEdit, QLineEdit):
                    price = lineEdit.text()
                else:
                    price = "0"
                tableWidget.removeRow(newRow)
                tableWidget.insertRow(i + 1)
                lineEditt = QLineEdit(str(quantiter_text))
                tableWidget.setCellWidget(i + 1, 2, lineEditt)
                lineEditt = QLineEdit(str(price))
                tableWidget.setCellWidget(i + 1, 3, lineEditt)
                for col, itemData in enumerate(row_data):
                    tableWidget.setItem(i + 1, col, QTableWidgetItem(str(itemData)))
                print("quantiter_text", quantiter_text)
                # tableWidget.setItem(i + 1, 3, QTableWidgetItem(str(quantiter_text)))


            ch = "border: 1px solid '#5B2A86';" \
                 "border-radius: 15px;" \
                 "font-size: " + font_size + "px;" \
                                             "color: '#5B2A86';" \
                                             "padding: 10px 0;" \
                                             "margin: 10px 10px ;" \
                                             "selection-background-color: '#5B2A86';" \
                                             "selection-color: white;"
            tableWidget.setStyleSheet(ch)
            tableWidget.resizeColumnsToContents()
            tableWidget.resizeRowsToContents()
            tableWidget.setFixedHeight(400)




        except Exception as e:
            print(e)

        print('test')
    all_client=supplier.create_supplier()
    welcome_label = QLabel("Créer une nouvelle facture fournisseur")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    name_list_view = QListView()
    name_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
    name_list_view.setStyleSheet(ch)
    name_list_view.setFixedHeight(200)
    widgets["name_list_view"].append(name_list_view)

    name_model = QStandardItemModel()
    name_list_view.setModel(name_model)

    cin_entry = QLineEdit()
    full_name_entry = QLineEdit()
    cin_entry.setObjectName("Numéro de téléphone")
    cin_entry.setStyleSheet(ch)
    cin_entry.setPlaceholderText("Numéro de téléphone")

    cin_entry.textChanged.connect(filterPhoneNumbers)
    widgets["cin_entry"].append(cin_entry)

    phone_list_view = QListView()
    full_name_entry.setObjectName("full_name_entry")
    full_name_entry.setStyleSheet(ch)
    full_name_entry.setPlaceholderText("full name")
    full_name_entry.textChanged.connect(filterNames)
    widgets["full_name"].append(full_name_entry)

    phone_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
    phone_list_view.setStyleSheet(ch)

    widgets["phone_list_view"].append(phone_list_view)

    matching_items = [thing.name for thing in all_client]
    for item in matching_items:
        name_model.appendRow(QStandardItem(item))

    # Create a QStandardItemModel to hold the items for phone numbers
    phone_model = QStandardItemModel()
    phone_list_view.setModel(phone_model)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content_widget = QWidget()
    scroll_area.setWidget(scroll_content_widget)
    widgets["scroll"].append(scroll_area)


    welcome_label=QLabel("total :  remain : ")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["label"].append(welcome_label)


    money_entry = QLineEdit()
    money_entry.setObjectName("mpney_entry")
    money_entry.setStyleSheet(ch)
    money_entry.setPlaceholderText("Règlement")
    widgets["money_entry"].append(money_entry)

    date_entry = QLineEdit()
    date_entry.setStyleSheet(ch)
    date_entry.setText(str(date.today()))
    widgets["door_cces"].append(date_entry)

    all_items = items.create_items()
    all_items_dict=items.create_dict_items()

    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_create_supplier_bill(full_name_entry,cin_entry,date_entry.text(),tableWidget,all_items_dict,money_entry,welcome_label))

    search_line_edit = QLineEdit()
    search_line_edit.setStyleSheet(ch)
    search_line_edit.setPlaceholderText("Rechercher ..")
    try:
        search_line_edit.textEdited.connect(lambda: sortTableByName(tableWidget))
    except Exception as e:
        print(e)

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_items)+1)
    tableWidget.setColumnCount(4)
    tableWidget.setItem(0, 0, QTableWidgetItem("      l'article"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Stock"))
    tableWidget.setItem(0,2,QTableWidgetItem("quantiter"))
    tableWidget.setItem(0, 3, QTableWidgetItem("Prix            "))
    i=0
    for item in all_items:
        i=i+1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(item.item_name)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(item.item_stocks)))
        lineEdit = QLineEdit("")
        tableWidget.setCellWidget(i, 2, lineEdit)
        lineEdit = QLineEdit("")
        tableWidget.setCellWidget(i, 3, lineEdit)
    ch = "border: 1px solid '#5B2A86';" \
         "border-radius: 15px;" \
         "font-size: " + font_size + "px;" \
                                     "color: '#5B2A86';" \
                                     "padding: 10px 0;" \
                                     "margin: 10px 10px ;" \
                                     "selection-background-color: '#5B2A86';" \
                                     "selection-color: white;"
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedHeight(400)
   # tableWidget.doubleClicked.connect(lambda :select_worker(tableWidget,users,date))
    widgets["table"].append(tableWidget)

    see_total_button = create_button("Total ")
    widgets["see_total"].append(see_total_button)
    see_total_button.clicked.connect(lambda: see_total_2( str(money_entry.text()), welcome_label, tableWidget,len(all_items)))

    scroll_grid = QGridLayout(scroll_content_widget)
    # scroll_grid.addWidget(widgets["explain_label"][-1], 0, 0)
    scroll_grid.addWidget(widgets["door_cces"][-1], 0, 1)

    scroll_grid.addWidget(full_name_entry, 1, 0)
    scroll_grid.addWidget(cin_entry, 1, 1)
    scroll_grid.addWidget(phone_list_view, 2, 1)
    scroll_grid.addWidget(name_list_view, 2, 0)
    scroll_grid.addWidget(search_line_edit, 3, 0,1,2)

    scroll_grid.addWidget(widgets["table"][-1], 4, 0,1,2)
    scroll_grid.addWidget(widgets["money_entry"][-1], 5, 1)
    scroll_grid.addWidget(widgets["confirm"][-1], 5, 0)
    scroll_grid.addWidget(widgets["see_total"][-1], 6, 0)
    scroll_grid.addWidget(widgets["button"][-1], 0, 0)
    scroll_grid.addWidget(widgets["label"][-1], 6, 1)
    grid.addWidget(widgets["scroll"][-1], 0, 0)

    name_list_view.clicked.connect(updateInputsFromName)
    phone_list_view.clicked.connect(updateInputsFromPhone)

    # grid.addWidget(widgets["explain_label"][-1], 0, 0)
    # grid.addWidget(widgets["full_name"][-1], 1, 0)
    # grid.addWidget(widgets["cin_entry"][-1], 1,1)
    # grid.addWidget(widgets["table"][-1], 2, 1)
    # grid.addWidget(widgets["money_entry"][-1], 3, 1)
    # grid.addWidget(widgets["calender"][-1], 2, 0)
    # grid.addWidget(widgets["confirm"][-1], 3, 0)
    # grid.addWidget(widgets["see_total"][-1], 4, 0)
    # grid.addWidget(widgets["button"][-1], 4, 2)
    # grid.addWidget(widgets["label"][-1], 4, 1)
def search_full_name_frame(type,type_2):#this function is for creating update door acces  frame

    welcome_label = QLabel("Recherche d'un client")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(lambda : back_to_search_client(type_2))

    back_main = create_button("Retour à l'accueil")
    widgets["back_to_main"].append(back_main)
    back_main.clicked.connect(back_to_main)

    if type=="Cin":
        id_label = QLabel("Numéro de téléphone: ")
        id_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
        widgets["id_label"].append(id_label)
    else:
        id_label = QLabel("Nom complet: ")
        id_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
        widgets["id_label"].append(id_label)



    all_client=client.create_clients()

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("Numéro de téléphone du client"))
    tableWidget.setItem(0, 1, QTableWidgetItem("nom du client"))
    tableWidget.setItem(0, 2, QTableWidgetItem("code :"))

    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.phone_number)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.full_name)))
        tableWidget.setItem(i,2,QTableWidgetItem(str(clientt.cin)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1000)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    if type_2=="bill":
        tableWidget.doubleClicked.connect(lambda :select_client_profile(lil,type,-1,"",""))
    else:
        tableWidget.doubleClicked.connect(lambda :select_client_devis(lil,type,-1,"",""))
    widgets["table"].append(tableWidget)



    lil = [tableWidget]
    id_entry = QLineEdit()
    id_entry.setObjectName("id_entry")
    id_entry.setStyleSheet(ch)
    id_entry.textEdited.connect(lambda: search_name(id_entry, all_client, lil, type))
    widgets["id_entry"].append(id_entry)
    grid.addWidget(widgets["explain_label"][-1], 1, 0)
    grid.addWidget(widgets["id_label"][-1], 2, 0)
    grid.addWidget(widgets["id_entry"][-1], 2, 1)
    grid.addWidget(widgets["table"][-1], 3, 1)
    grid.addWidget(widgets["button"][-1], 0, 0)
    grid.addWidget(widgets["back_to_main"][-1], 4, 0)
def search_name_frame(type):#this function is for creating update door acces  frame

    welcome_label = QLabel("Recherche de fournisseurs")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_search_supplier)
    if type=="Cin":
        id_label = QLabel("Numéro de téléphone : ")
        id_label.setStyleSheet("font-size: "+font_size+"px;"+ "color:'#5B2A86'")
        widgets["id_label"].append(id_label)
    else:
        id_label = QLabel(type+" : ")
        id_label.setStyleSheet("font-size: " + font_size + "px;" + "color:'#5B2A86'")
        widgets["id_label"].append(id_label)

    id_entry = QLineEdit()
    id_entry.setObjectName("id_entry")
    id_entry.setStyleSheet(ch)
    widgets["id_entry"].append(id_entry)

    all_client=supplier.create_supplier()

    tableWidget = QTableWidget()
    tableWidget.setRowCount(len(all_client) + 1)
    tableWidget.setColumnCount(3)
    tableWidget.setItem(0, 0, QTableWidgetItem("Numéro de téléphone du fournisseur"))
    tableWidget.setItem(0, 1, QTableWidgetItem("Fournisseur Nom complet"))
    tableWidget.setItem(0, 2, QTableWidgetItem("code "))



    i = 0
    for clientt in all_client:
        i = i + 1
        tableWidget.setItem(i, 0, QTableWidgetItem(str(clientt.phone_number)))
        tableWidget.setItem(i, 1, QTableWidgetItem(str(clientt.name)))
        tableWidget.setItem(i, 2, QTableWidgetItem(str(clientt.id)))
    tableWidget.setStyleSheet(ch)
    tableWidget.resizeColumnsToContents()
    # print(tableWidget.item(2,2).text())
    tableWidget.resizeRowsToContents()
    tableWidget.setFixedWidth(1000)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.doubleClicked.connect(lambda :select_supplier_profile(tableWidget,type))
    widgets["table"].append(tableWidget)


    conferm = create_button("Rechercher")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: search_name_supplier(id_entry,all_client,tableWidget,type))

    grid.addWidget(widgets["explain_label"][-1],1,1)
    grid.addWidget(widgets["id_label"][-1], 2, 0)
    grid.addWidget(widgets["id_entry"][-1], 2, 1)
    grid.addWidget(widgets["table"][-1], 3, 1)
    grid.addWidget(widgets["confirm"][-1], 4, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)

def create_item_frame():#this function is for creating worker  frame
    welcome_label = QLabel("Créer un nouvel article ")
    welcome_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    welcome_label.setAlignment(QtCore.Qt.AlignCenter)
    widgets["explain_label"].append(welcome_label)
    ch = "border : 1px solid '#5B2A86';" + "border-radius: 15px;" + "font-size: "+font_size+"px;" + "color:'#5B2A86' ;" + "padding: 10px 0;" + "margin: 10px 10px ;"
    back = create_button("Retour")
    widgets["button"].append(back)
    back.clicked.connect(back_to_main)

    full_name_label = QLabel("Nom de l'article : ")
    full_name_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["label"].append(full_name_label)

    name_entry = QLineEdit()
    name_entry.setObjectName("name_entry")
    name_entry.setStyleSheet(ch)
    widgets["full_name"].append(name_entry)

    price_label = QLabel("Prix de l'article : ")
    price_label.setStyleSheet("font-size: "+font_size+"px;"+ "color:'#5B2A86'")
    widgets["price_label"].append(price_label)

    price_entry = QLineEdit()
    price_entry.setObjectName("price_entry")
    price_entry.setStyleSheet(ch)
    widgets["price_entry"].append(price_entry)

    stock_label = QLabel("Item stock : ")
    stock_label.setStyleSheet("font-size: "+font_size+"px;" + "color:'#5B2A86'")
    widgets["stock_label"].append(stock_label)

    stock_entry = QLineEdit()
    stock_entry.setObjectName("stock_entry")
    stock_entry.setStyleSheet(ch)
    widgets["stock_entry"].append(stock_entry)


    conferm = create_button("Confirm ")
    widgets["confirm"].append(conferm)
    conferm.clicked.connect(lambda: confirm_create_item(name_entry,price_entry,stock_entry))

    grid.addWidget(widgets["explain_label"][-1], 0, 1)
    grid.addWidget(widgets["label"][-1], 2, 0)
    grid.addWidget(widgets["full_name"][-1], 2, 1)
    grid.addWidget(widgets["price_label"][-1], 3, 0)
    grid.addWidget(widgets["price_entry"][-1], 3, 1)
    grid.addWidget(widgets["stock_label"][-1], 4, 0)
    grid.addWidget(widgets["stock_entry"][-1], 4, 1)
    grid.addWidget(widgets["confirm"][-1], 5, 0)
    grid.addWidget(widgets["button"][-1], 0, 0)






main_frame()

window.setLayout(grid)
window.setWindowIcon(QtGui.QIcon('logo.png'))
window.show()
sys.exit(app.exec())