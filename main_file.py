import mysql.connector as sql
import getpass
dbn=dbp=cursor=connection=None
choice=0
import sys

def get_db_name():
    global dbn
    global dbp
    print("Enter Database Name: ")
    dbn=input()
    dbp=getpass.getpass(stream=None)
    access_db(dbn,dbp)

def access_db(dbn,dbp):
    global cursor
    global connection
    try:
        connection=sql.connect(host="localhost",user="root",password=dbp,database=dbn)
        if connection.is_connected():
            print("Connected to Database: ",dbn)
        else:
            print("Check credentials!")
            return get_db_name()
    except:
        print("Cannot connect to MySql Server, check configuration")
        get_db_name()
    cursor=connection.cursor()
    main_menu()

def main_menu():
    global dbn
    global choice
    print(" \t \t Options: ")
    print(" \t \t Table Management: ")
    print(" \t \t \t 1. Create table")
    print(" \t \t \t 2. View existing tables")
    print(" \t \t \t 3. Add data to table")
    print(" \t \t \t 4. Delete table")
    print(" \t \t \t 5. Show data in table")
    print(" \t \t Database Management: ")
    print(" \t \t \t 6. Change Database")
    print(" \t \t \t 7. Remove Database")
    print(" \t \t \t 8. Create Database")
    print(" \t Exit")
    choice=int(input("\n Select Option: "))

    if choice==1:
        crt_tbl()
    elif choice==2:
        view_tables()
    elif choice==3:
        insert_to_tbl()
    elif choice==4:
        del_tbl()
    elif choice==5:
        tbl_data_all()
    elif choice==6:
        connection.close()
        get_db_name()
    elif choice==7:
        rm_db()
    elif choice==8:
        mk_db()

def crt_tbl():
    global dbn
    global cursor
    lst=[]
    print("Enter table name to create: ")
    tbl_name=input("")
    n=int(input("Enter numbers of fields to create in table: "))
    while n!=0:
        col_name=input("Enter Column name: ")
        col_dtype=input("Enter Column Datatype: ")
        temp_str=col_name+"$"+col_dtype
        lst.append(temp_str)
        n-=1
    temp_split=lst[0].split("$")
    cursor.execute("create table "+tbl_name+" ("+temp_split[0]+" "+temp_split[1]+" );")
    lst.pop(0)
    for x in lst:
        print("lst= ",lst)
        index=lst.index(x)
        temp_split=x.split("$")
        cursor.execute("alter table "+tbl_name+" add ("+temp_split[0]+" "+temp_split[1]+" );")
    t=input("\n Enter to coninue")
    main_menu()

def view_tables():
    global dbn
    global cursor
    print("Tables in database:"+dbn)
    cursor.execute("show tables "+";")
    data=cursor.fetchall()
    for x in data:
        print(x[0])
    print("\n \n")
    t=input("\n Enter to coninue")
    main_menu()

def insert_to_tbl():
    global dbn
    global cursor
    tbl_name=input("Enter table name: ")
    n=int(input("Enter number of data entries: "))
    while n!=0:
        cursor.execute("describe "+tbl_name+";")
        temp_c=cursor.fetchall()
        lst=[]
        for x in temp_c:
            lst.append(x[0])
        temp_lst=[]
        for a in lst:
            print("Enter data for column ",a)
            data=input()
            temp_lst.append(data)
        fin_data="insert into "+tbl_name+" VALUES("
        count=0
        for y in temp_lst:
            if count<(len(lst)-1):
                if y.isalpha():
                    y="'"+y+"'"
                else:
                    pass
                fin_data+=y+","
                count+=1
            else:
                if y.isalpha():
                    y="'"+y+"'"
                else:
                    pass
                fin_data+=y+" "
        fin_data+=");"
        cursor.execute(fin_data)
        n-=1
    t=input("\n Enter to coninue")
    main_menu()

def del_tbl():
    cursor.execute("show tables;")
    tbls=cursor.fetchall()
    print("Tables in Current Database: ")
    for tbl in tbls:
        print(tbl[0])
    tbl_del=input("Enter table to delete: ")
    cnfrm=input("\n This is irreversable. Sure to delete "+tbl_del+" ?, (y/n)")
    if cnfrm.lower()=='y':
        cursor.execute("drop table "+tbl_del)
    else:
        print("\n Table "+tbl_del+" is not deleted")
    t=input("\n Enter to coninue")
    main_menu()

def tbl_data_all():
    print("Enter table name: ")
    tbl_name=input()
    print("All data in table: \n")
    cursor.execute("describe "+tbl_name+";")
    temp_c=cursor.fetchall()
    for a in temp_c:
        print(a[0], end=" ")
    print("\n")
    cursor.execute("select * from "+tbl_name+";")
    data=cursor.fetchall()
    for a in data:
        for b in a:
            print(b,end=" ")
        print("\n")
    print("\n END OF TABLE")
    t=input("\n Enter to coninue")
    main_menu()

def rm_db():
    print("Enter database to remove: ")
    dbn_rm=input()
    if dbn_rm==dbn:
        print("Cannot delete database! LOGGED INTO THE SAME")
        main_menu()
    else:
        cursor.execute("drop database "+dbn_rm)
    t=input("\n Enter to coninue")
    main_menu()

def mk_db():
    global dbp
    print("Enter database name to create: ")
    dbn_new=input()
    cursor.execute("create database "+dbn_new+" ;")
    print("Testing database")
    connection2=sql.connect(host="localhost",user="root",password=dbp,database=dbn_new)
    if connection2.isconnected():
        print("Database created successfully")
        connection2.close()
    else:
        print("Connection cannot be established! Try again.. ")
    t=input("\n Enter to coninue")
    main_menu()
    
get_db_name()
