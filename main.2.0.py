import datetime
import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys
listt = []
# connecting data base
try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         port='3306',
                                         database='application',
                                         user='root',
                                         password="your_database_password" ,
                                         auth_plugin='mysql_native_password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute("SELECT * FROM application.items")
        for x in cursor:
            listt.append(x)
        print(listt)
        print(listt[0][1], type(listt[0][1]))

except Error as e:
    print("Error while connecting to MySQL", e)


# creating all the class that i need for displaying result
# creating class  items that can modifie and add to it like u want
class Items:
    def __init__(self):
        self.item = {}

# creating client class that have a list of bills that each one have a date deferint from other
class client:
    def __init__(self, a, p, cin):
        self.name = a
        self.prenom = p
        self.CIN = cin
        self.bills = []

# creating bills class that have date and cin of the client and quantiter of each item
class bills:
    def __init__(self, cin, bill_date):
        self.cin = cin
        self.date = bill_date
        self.q_items={}
def money(ch):
    p=len(ch)
    while p>3:
        print(p)
        ch=ch[0:p-3]+","+ch[p-3:len(ch)]
        p=p-3
    return ch
print(money("1000"))
print(money("10000"))
print(money("100000"))
print(money("10000000"))

# this the main window that u can choise what u want to do
choise = Tk()

# this function make the window that u can modifie the price of items
def modifie():

    mod = Toplevel(choise)


   # this is the function that allow u change items
    def changee(name_prix, i):
        # so to change the price for the items i create a dictioneri that have the name of all the items and the new price of that item and if it stay 0 the price d'ont change
        for key, value in name_prix.items():
            if name_prix[key].get() == 0:
                print(key)
            else:
                print(name_prix[key].get())
                print(key)
                try:
                    j = str(name_prix[key].get())
                    print(j)
                    ch = "UPDATE items SET price=" + j + " WHERE nam=\"" + str(key) + "\""
                    print(ch)
                    cursor.execute(ch)
                    connection.commit()
                    price_confm = Label(mod, text="price change successfully : ",font="Times 23").grid(row=i + 1, column=1)
                except:
                    errlb = Label(mod, text="the price need to nmber ",font="Times 23").grid(row=i + 1, column=1)

    cursor.execute("SELECT * FROM app.items")

    nam = Label(mod, text="items name : ", font="Times 23").grid(row=0, column=0)
    prx = Label(mod, text="price : ", font="Times 23").grid(row=0, column=1)
    newpx = Label(mod, text="new price :", font="Times 23").grid(row=0, column=2)

    name_prix = {}
    i = 1

    for x in cursor:
        ln = Label(mod, text=x[0],font="Times 23").grid(row=i, column=0)
        lp = Label(mod, text=str(x[1]),font="Times 23").grid(row=i, column=1)

        print(x[0])
        ch = str(x[0])
        price_text = IntVar()
        name_prix[ch] = price_text
        en = Entry(mod, textvariable=price_text,font="Times 23")
        en.grid(row=i, column=2)
        i += 1

    chng = Button(mod, text="change ", command=lambda: changee(name_prix, i),font="Times 23").grid(row=i + 1, column=3)

    mod.mainloop()

# this is the adding function that add new items and there price to the the items table
def adding():
    add_items = Toplevel(choise)
    # Create A Main Frame
    main_frame = Frame(add_items)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    add = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=add, anchor="nw")
  # the conferm function make sure that the new items it doesn't exist before add it to the database
    def conferm(k, i):
        s = str(adding_text.get())
        if k.count(s) == 0:
            cursor.execute("INSERT INTO items value (%s,%s)", (s, int(price_text.get())))
            ch = "ALTER TABLE bill ADD" + " q_" + s + " int not null"
            cursor.execute(ch)
            adding_succefuly  = Label(add, text="the product  " + s + " succecfuly added ",font="Times 23").grid(row=i + 1, column=3)

            connection.commit()
        else:
            li = Label(add, text="this product exist ",font="Times 23").grid(row=i + 2, column=0)

    showing_exist_product = Label(add, text="the product exist : ",font="Times 23").grid(row=0, column=0)
# showing all the items and there price
    cursor.execute("SELECT * FROM app.items")
    i = 1
    k = []
    for x in cursor:
        k.append(x[0])
        product = "name : " + x[0] + " price : " + str(x[1])
        ln = Label(add, text=product,font="Times 23").grid(row=i, column=0)

        i += 1

    adding_text = StringVar()
    e2 = Entry(add, textvariable=adding_text,font="Times 23")
    e2.grid(row=i + 1, column=0)

    price_text = IntVar()
    e3 = Entry(add, textvariable=price_text,font="Times 23")
    e3.grid(row=i + 1, column=1)
    confirmation = Button(add, text="conferm", command=lambda: conferm(k, i),font="Times 23").grid(row=i + 1, column=2)


    add.mainloop()

# the window to create new bill
def new_bill():
    bill = Toplevel(choise)
    # Create A Main Frame
    main_frame = Frame(bill)
    main_frame.pack(fill=BOTH, expand=1)

    # Create A Canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Add A Scrollbar To The Canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # Configure The Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create ANOTHER Frame INSIDE the Canvas
    facteur = Frame(my_canvas)

    # Add that New frame To a Window In The Canvas
    my_canvas.create_window((0, 0), window=facteur, anchor="nw")

    x = datetime.datetime.now()
# this function show u the total price of he items that the client want to buy
    def see_total_1(quantiter):
        cursor.execute("SELECT * from items")
        it = Items()
        k = 2
        s = 0
        for x in cursor:
            it.prix[x[0]] = x[1]
            q = quantiter[x[0]].get() * it.prix[x[0]]
            s = s + q
            ln = Label(facteur, text=money(str(int(q))),font="Times 23").grid(row=k, column=2)

            k = k + 1
        ko = Label(facteur, text="total : " +money(str(int(s))),font="Times 23").grid(row=k + 1, column=1)
        s=int(s)
        s = s - int(pay_text.get())
        res = Label(facteur, text="the rest : " + money(str(s)),font="Times 23").grid(row=k + 1, column=0)

    l1 = Label(facteur, text="name : ",font="Times 23").grid(row=0, column=0)
    l2 = Label(facteur, text="prenom : ",font="Times 23").grid(row=0, column=2)
    lc = Label(facteur, text="CIN : ",font="Times 23").grid(row=0, column=4)
    l3 = Label(facteur, text="Date : year",font="Times 23").grid(row=1, column=0)
    l4 = Label(facteur, text="month",font="Times 23").grid(row=1, column=2)
    ly = Label(facteur, text="day : ",font="Times 23").grid(row=1, column=4)





    name_text = StringVar()
    e1 = Entry(facteur, textvariable=name_text,font="Times 23",width=10)
    e1.grid(row=0, column=1)


    prenom_text = StringVar()
    e2 = Entry(facteur, textvariable=prenom_text,font="Times 23",width=10)
    e2.grid(row=0, column=3)

    CIN_text = StringVar()
    eC = Entry(facteur, textvariable=CIN_text,font="Times 23",width=10)
    eC.grid(row=0, column=5)

    year_text = IntVar()
    year_text.set(x.year)
    e3 = Entry(facteur, textvariable=year_text,font="Times 23",width=5)
    e3.grid(row=1, column=1)

    month_text = IntVar()
    month_text.set(x.month)
    e4 = Entry(facteur, textvariable=month_text,font="Times 23",width=5)
    e4.grid(row=1, column=3)

    day_text = IntVar()
    day_text.set(x.day)
    e5 = Entry(facteur, textvariable=day_text,font="Times 23",width=5)
    e5.grid(row=1, column=5)

    j = 2
    cursor.execute("select nam,quantiter from items")
    quantiter = {}
    for x in cursor:
        ln = Label(facteur, text=x[0] + " : ",font="Times 23").grid(row=j, column=0)
        if (x[0] == "till"):
            items_text = DoubleVar()

        else:
            items_text = IntVar()

        quantiter[x[0]] = items_text
        ei = Entry(facteur, textvariable=items_text,font="Times 23",width=10)
        ei.grid(row=j, column=1)
        if x[1]==0:
            ln=Label(facteur,text="not on stock !",fg="red",font="times 23").grid(row=j,column=3)
        else :
            ln=Label(facteur,text="on stock ",fg="green",font="Times 23").grid(row=j,column=3)
        j = j + 1
    l_pay = Label(facteur, text="reglement : ",font="Times 23").grid(row=j, column=0)
    pay_text = IntVar()
    e_pay = Entry(facteur, textvariable=pay_text,font="Times 23",width=10).grid(row=j, column=1)

    def confirm(quantiter):
        cursor.execute("SELECT * from items")
        it = Items()
        s = 0
        for x in cursor:
            it.prix[x[0]] = x[1]
            q = quantiter[x[0]].get() * it.prix[x[0]]
            s = s + q
        print("ok")
        ch = str(name_text.get())
        print(ch)
        sh = str(prenom_text.get())
        print(sh)
        cin = str(CIN_text.get())
        sin = "\"" + cin + "\""
        cursor.execute("select CIN from the_client where CIN=" + sin)
        p=True
        for x in cursor:
            p = False
        if p :
            cursor.execute("INSERT INTO the_client(CIN,c_name,c_prenom) value(%s,%s,%s) ", (cin, ch, sh))
        year = int(year_text.get())
        month = int(month_text.get())
        day = int(day_text.get())
        bill_time = str(year) + "-" + str(month) + "-" + str(day)
        print(bill_time)
        cursor.execute("select nam from items")
        jh = "(client_cin,bill_date,reglement,total,"
        print(jh)

        for k in cursor:
            jh = jh + "q_" + k[0] + ","
            print(k[0])
            print(jh)
        jh = jh[0:len(jh) - 1] + ")"
        print(jh)
        q_items = []
        q_items.append(cin)
        q_items.append(bill_time)
        q_items.append(float(pay_text.get()))
        q_items.append(s)
        items_nam={}
        for key, value in quantiter.items():
            items_nam[key]=int(quantiter[key].get())
            q_items.append(int(quantiter[key].get()))
            if items_nam[key]!=0:
                cursor.execute("update items set quantiter=quantiter-"+str(items_nam[key])+" where nam="+"\""+key+"\"")
        lol = tuple(q_items)
        bil_cursor = "INSERT INTO bill " + jh + " value " + str(lol)
        cursor.execute(bil_cursor)
        connection.commit()
        print(bil_cursor)
        th = "at " + str(year_text.get()) + "/" + str(month_text.get()) + "/" + str(day_text.get())
        ln = Label(facteur, text="bill confirmed for  " + ch + "  " + th,font="Times 23").grid(row=j+2, column=0)
        print(j)

    see_total = Button(facteur, text="see the total", command=lambda: see_total_1(quantiter),font="Times 23").grid(row=j + 1, column=3)
    test = Button(facteur, text="confirm", command=lambda: confirm(quantiter),font="Times 23").grid(row=j +2, column=3)

    facteur.mainloop()


def search():
    def make_window(cin,client_number,top_mh,clients):

        cursor.execute("select * from items")
        item = Items()
        bill_variable_name = "bill_date,reglement,total,"
        bill_variable = ["reglement", "total"]
        for billElement in cursor:
            bill_variable_name = bill_variable_name + "q_" + billElement[0] + ","
            bill_variable.append("q_" + billElement[0])
            item.prix[billElement[0]] = billElement[1]
        # geting all the bill for the client withh that cin
        cursor.execute("select " + bill_variable_name[0:len(bill_variable_name) - 1] + " from bill where client_cin=" + "\"" + cin + "\" order by bill_date")
        datte_verification = []
        # bill_element_index  = 1 because for bill_element_index =0  we add the bill_date
        bill_element_index = 1
        for billElement  in cursor:
            if billElement[0] in datte_verification:
               verif = True
            else:
               verif = False
               datte_verification.append(billElement[0])
            bill_number  = datte_verification.index(billElement[0])
            if verif:
               for bill_element in bill_variable:
                     clients[client_number].bills[bill_number].q_items[bill_element] = billElement[bill_element_index] + clients[client_number].bills[bill_number].q_items[bill_element]
                     bill_element_index = bill_element_index + 1
               bill_element_index = 1
            else:
               clients[client_number].bills.append(bills(cin, billElement[0]))
               for bill_element in bill_variable:
                     clients[client_number].bills[bill_number].q_items[bill_element] = billElement[bill_element_index]
                     bill_element_index = bill_element_index + 1
               bill_element_index = 1
        windows = []
        total = {}
        for billElement in bill_variable:
            total[billElement] = 0
        for bill_date in range(len(datte_verification)):
            print(datte_verification)
            print(bill_date)
            windows.append("window" + str(bill_date))
            windows[bill_date] = Toplevel(top_mh)
            # Create A Main Frame
            main_frame = Frame(windows[bill_date])
            main_frame.pack(fill=BOTH, expand=1)

            # Create A Canvas
            my_canvas = Canvas(main_frame)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            # Add A Scrollbar To The Canvas
            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)

            # Configure The Canvas
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            # Create ANOTHER Frame INSIDE the Canvas
            second_frame = Frame(my_canvas)

            # Add that New frame To a Window In The Canvas
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
            windows[bill_date].title(clients[client_number].name + " " + clients[client_number].prenom + " date : " + str(datte_verification[bill_date]))
            l_nam = Label(second_frame, text="client name:     " + clients[client_number].name, font="Times 23").grid(row=0, column=0)
            l_prenom = Label(second_frame, text="    prenom :    " + clients[client_number].prenom, font="Times 23").grid(row=0, column=1)
            l_date = Label(second_frame, text="     date :    " + str(datte_verification[bill_date]), font="Times 23").grid(row=0, column=2)
            bill_element_index = 1
            for key, value in clients[client_number].bills[bill_date].q_items.items():
                print(key, value)
                total[key] = total[key] + value
                if key == "total":
                    l_items = Label(second_frame, text=key + ": ", font="Times 23").grid(row=bill_element_index, column=0)
                    l_prix = Label(second_frame, text=money(str(value)), font="Times 23").grid(row=bill_element_index, column=1)
                    l_rest = Label(second_frame, text="rest : " + money(str(clients[client_number].bills[bill_date].q_items["total"] - clients[client_number].bills[bill_date].q_items["reglement"])), font="Times 23").grid(row=bill_element_index, column=2)

                else:
                    if key=="reglement" or value!=0:
                        l_items = Label(second_frame, text=key + ": ", font="Times 23").grid(row=bill_element_index, column=0)
                        l_prix = Label(second_frame, text=money(str(value)), font="Times 23").grid(row=bill_element_index, column=1)
                bill_element_index = bill_element_index + 1

        print(total)
        the_total = Toplevel(top_mh)
        # Create A Main Frame
        main_frame = Frame(the_total)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        the_total.title("the total ")
        l_nam = Label(second_frame, text="client name:      " + clients[client_number].name, font="Times 23").grid(row=0, column=0)
        l_prenom = Label(second_frame, text="    prenom :   " + clients[client_number].prenom, font="Times 23").grid(row=0, column=1)
        bill_element_index = 1
        for key, value in total.items():
             if key == "total":
                  l_items = Label(second_frame, text=key + ": ", font="Times 23").grid(row=bill_element_index, column=0)
                  l_prix = Label(second_frame, text=money(str(value)), font="Times 23").grid(row=bill_element_index, column=1)
                  l_rest = Label(second_frame, text="rest : " +money( str(total["total"] - total["reglement"])),font="Times 23").grid(row=bill_element_index, column=2)

             else:
                if key=="reglement" or value!=0:
                    l_items = Label(second_frame, text="total " + key + ": ", font="Times 23").grid(row=bill_element_index, column=0)
                    l_prix = Label(second_frame, text=money(str(value)), font="Times 23").grid(row=bill_element_index, column=1)
             bill_element_index = bill_element_index + 1
    def get_cin(ch):
        return ch[ch.index("CIN") + 6:len(ch)]

    def verification(ch1, ch2):
        if ch1 == ch2[0:len(ch1)]:
            return True
        else:
            return False

    def search_name():
        search_nam = Toplevel(choise)


        def search_client_nam(ch, clients):
            print("size :", client_serch.size())
            i = client_serch.size()
            while i >= 0:
                print("size :", client_serch.size())
                print("i:", i)
                client_serch.delete(i)
                i = i - 1
            k = 1
            for x in range(len(clients)):
                if verification(ch, clients[x].name):
                    print("k:", k)
                    client_serch.insert(k, "name : " + clients[x].name + "      prenom : " + clients[x].prenom + "      CIN : " + clients[x].CIN)
                    k = k + 1
                else:
                    print("size :", client_serch.size())

        def select_name(th,clients):
                global Cin
                for i in th.curselection():
                    ch=str(th.get(i))
                    Cin=get_cin(ch)
                m=0
                print(Cin)
                while clients[m].CIN!=Cin and m!=len(clients):
                    print(Cin)
                    print(clients[m].CIN)
                    m=m+1
                make_window(Cin, m, search_nam, clients)


        clients = []
        cursor.execute("select CIN,c_name,c_prenom from the_client  ")
        client_serch = Listbox(search_nam, font="Times 23", height=20, width=50)
        i = 1
        client_serch.xview()
        for x in cursor:
            clients.append(client(x[1], x[2], x[0]))
            print("name :    " + x[1] + "        prenom : " + x[2] + "        CIN : " + x[0])

        l_search = Label(search_nam, text="the_name ", font="Times 23").grid(row=0, column=0)
        nam_text = StringVar()
        e_nam = Entry(search_nam, textvariable=nam_text, font="Times 23").grid(row=0, column=1)
        b_search = Button(search_nam, text="search :", font="Times 23",command=lambda: search_client_nam(str(nam_text.get()), clients)).grid(row=0, column=2)
        b_select = Button(search_nam, text="selecte", font="Times 23",command=lambda: select_name(client_serch,clients)).grid(row=0, column=3)
        client_serch.grid(row=1, column=1)

    def search_cin():
        searching = Toplevel(choise)

        def selecting(ch):
            global the_client, total
            cursor.execute("select * from items")
            item = Items()
            variable = "bill_date,reglement,total,"
            var = ["reglement","total"]
            for x in cursor:
                variable = variable + "q_" + x[0] + ","
                var.append("q_" + x[0])
                item.prix[x[0]] = x[1]
            cursor.execute("select c_name,c_prenom,CIN from the_client where CIN=" + "\"" + ch + "\"")
            for x in cursor:
                the_client = client(x[0], x[1], x[2])
            print("select " + variable[0:len(variable) - 1] + " from bill where client_cin=" + "\"" + ch + "\" order by bill_date ")
            cursor.execute("select " + variable[0:len(variable) - 1] + " from bill where client_cin=" + "\"" + ch + "\" order by bill_date")
            datte_verification = []
            j = 1

            for x in cursor:
                if x[0] in datte_verification:
                    verif = True
                else:
                    verif = False
                    datte_verification.append(x[0])
                i = datte_verification.index(x[0])
                if verif:
                    for y in var:
                        the_client.bills[i].q_items[y] = x[j] + the_client.bills[i].q_items[y]
                        j = j + 1
                    j = 1
                else:
                    the_client.bills.append(bills(ch, x[0]))
                    for y in var:
                        the_client.bills[i].q_items[y] = x[j]
                        j = j + 1
                    j = 1
            windows = []
            total = {}
            for x in var:
                total[x] = 0
            for i in range(len(datte_verification)):
                print(datte_verification)
                print(i)
                windows.append("window" + str(i))
                windows[i] = Toplevel(searching)

                l_nam=Label(windows[i],text="client name: "+the_client.name,font="Times 23").grid(row=0,column=0)
                l_prenom=Label(windows[i],text="prenom :"+the_client.prenom,font="Times 23").grid(row=0,column=1)
                l_date=Label(windows[i],text="date : "+str(datte_verification[i]),font="Times 23").grid(row=0,column=2)
                j=1
                for key,value in the_client.bills[i].q_items.items():
                    print(key,value)
                    total[key]=total[key]+value
                    if key == "total":
                        l_items = Label(windows[i], text=key + ": ",font="Times 23").grid(row=j, column=0)
                        l_prix = Label(windows[i], text=money(str(value)),font="Times 23").grid(row=j, column=1)
                        l_rest = Label(windows[i], text="rest : "+money(str(the_client.bills[i].q_items["total"] - the_client.bills[i].q_items["reglement"])),font="Times 23").grid(row=j, column=2)
                    else:
                        if key == "reglement" or value != 0:
                            l_items = Label(windows[i], text=key + ": ",font="Times 23").grid(row=j, column=0)
                            l_prix = Label(windows[i], text=money(str(value)),font="Times 23").grid(row=j, column=1)
                    j = j + 1


                print(total)
            the_total=Toplevel(searching)
            l_nam = Label(the_total, text="client name: " + the_client.name,font="Times 23").grid(row=0, column=0)
            l_prenom = Label(the_total, text="prenom :" + the_client.prenom,font="Times 23").grid(row=0, column=1)
            j=1
            for key,value in total.items():
                if key=="total":
                    l_items = Label(the_total, text= key + ": ",font="Times 23").grid(row=j, column=0)
                    l_prix = Label(the_total, text=money(str(value)),font="Times 23").grid(row=j, column=1)
                    l_rest=Label(the_total,text="rest : "+money(str(total["total"]-total["reglement"])),font="Times 23").grid(row=j,column=2)

                else:
                   if key=="reglement" or value!=0:
                       l_items=Label(the_total,text="total "+key+": ",font="Times 23").grid(row=j,column=0)
                       l_prix=Label(the_total,text=money(str(value)),font="Times 23").grid(row=j,column=1)
                j=j+1

        cin_text=StringVar()
        e_cin=Entry(searching,textvariable=cin_text,font="Times 23").grid(row=0,column=0)

        butt_cin=Button(searching,text="search",command=lambda :selecting(str(cin_text.get())),font="Times 23").grid(row=0,column=1)


        searching.mainloop()



    search_cin = Button(choise, text="searsh with CIN ", command=search_cin,font="Times 23").grid(row=1, column=1)
    search_name = Button(choise, text="searsh with name  ",font="Times 23",command=search_name).grid(row=2, column=1)
def modify_stock():
    mod_stock=Toplevel(choise)
    def change_stock(stock_quantity,j):
        for key,value in stock_quantity.items():
           try:
               if stock_quantity[key].get()==0:
                   print(key)
               else:
                   s=str(stock_quantity[key].get())
                   ch="UPDATE items set quantiter="+s+" where nam="+"\""+key+"\""
                   cursor.execute(ch)
                   print(ch)
                   connection.commit()
                   l_done=Label(mod_stock,text="modification done ",font="Times 23").grid(row=j+1,column=0)
           except:
               l_error=Label(mod_stock,text="the quantiter have to be a number !!",font="Times 23").grid(row=j+2,column=0)

    cursor.execute("select nam,quantiter from items ")
    j=0
    stock_quantity={}
    for x in cursor:
        l=Label(mod_stock,text=x[0]+" : ",font="Times 23").grid(row=j,column=0)
        l1=Label(mod_stock,text=str(x[1]),font="Times 23").grid(row=j,column=1)
        stock_quantity[x[0]]=IntVar()
        en=Entry(mod_stock,textvariable=stock_quantity[x[0]],font="Times 23")
        en.grid(row=j,column=2)
        j+=1
    b_modify=Button(mod_stock,text="modify",font="Times 23",command=lambda : change_stock(stock_quantity,j)).grid(row=j+1,column=1)


    mod_stock.mainloop()
def update_stock():
    update_stck=Toplevel(choise)
    def update():
        s=int(quantiter_int.get())
        year = int(s_year.get())
        month = int(s_month.get())
        day = int(s_day.get())
        command_date = str(year) + "-" + str(month) + "-" + str(day)
        nam=""
        for i in listbox.curselection():
            print(listbox.get(i))
            nam=listbox.get(i)
        l=[nam,s,command_date]
        lol=tuple(l)
        ch="insert into command (nam,quantiter,command_date) value "+str(lol)
        print(ch)
        cursor.execute(ch)
        cursor.execute("UPDATE items set quantiter=quantiter+"+str(s)+" where nam=""\""+nam+"\"")
        connection.commit()
        l=Label(update_stck,text="command conformed ",font="Times 20").grid(row=2,column=0)




    cursor.execute("select nam from items ")
    y = datetime.datetime.now()
    l_items=Label(update_stck,text="items : ",font="Times 20").grid(row=0,column=0)
    l_quantiter=Label(update_stck,text="the quantity",font="Times 20").grid(row=0,column=1)
    listbox=Listbox(update_stck,font="Times 20")
    j=1
    for x in cursor :
        listbox.insert(j,x[0])
    quantiter_int=IntVar()
    quantty_entry=Entry(update_stck,textvariable=quantiter_int,font="Times 20",width=10).grid(row=1,column=1)
    listbox.grid(row=1,column=0)
    l_year=Label(update_stck,text="year : ",font="Times 20").grid(row=1,column=2)
    l_month=Label(update_stck,text="month : ",font="Times 20").grid(row=1,column=4)
    l_day=Label(update_stck,text="day : ",font="Times 20").grid(row=1,column=6)

    s_year=Spinbox(update_stck,from_=2021,to=2100,font="Times 20",width=5)
    s_year.delete(0,4)
    s_year.insert(0,y.year)
    s_year.grid(row=1,column=3)
    s_month=Spinbox(update_stck,from_=1,to=12,font="times 20",width=5)
    s_month.delete(0, 1)
    s_month.insert(0, y.month)
    s_month.grid(row=1,column=5)
    s_day=Spinbox(update_stck,from_=0,to=31,font="Times 20",width=5)
    s_day.delete(0, 1)
    s_day.insert(0, y.day)
    s_day.grid(row=1,column=7)

    b_conferm=Button(update_stck,text="conferm",command=update,font="Times 23").grid(row=3,column=2)


    update_stck.mainloop()
def historique_command():
    history=Toplevel()
    cursor.execute("select nam,quantiter,command_date from command  ")
    j=0
    for x in cursor:

        l=Label(history,text=x[0]+"   quantiter=  "+str(x[1]) +"   date  "+str(x[2]),font="Times 23").grid(row=j,column=0)
        j=j+1



    history.mainloop()

ch = "making a new bill "
B1 = Button(choise, text=ch, command=new_bill,font="Times 23").grid(row=0, column=0)
b2 = Button(choise, text="search", command=search,font="Times 23").grid(row=1, column=0)
b3 = Button(choise, text="adding product", command=adding,font="Times 23").grid(row=2, column=0)
b4 = Button(choise, text="modie price ", command=modifie,font="Times 23").grid(row=3, column=0)
b5=Button(choise,text="modify stock ",font="Times 23",command=modify_stock).grid(row=4,column=0)
b6=Button(choise,text="update stock ",font="Times 23",command=update_stock).grid(row=5,column=0)
b7=Button(choise,text="see historique ",font="Times 23",command=historique_command).grid(row=6,column=0)
ch_welcome="welcome to your bill management app "

choise.mainloop()
