#Creator : Nektarios Stylianos Karagiannis
#client :  Vasileios Karagiannis
# COMPLETED A STAGE 13 AUGUST 2022
# STARTING BETA STAGE 1/18/2023


from tkinter import *
import sqlite3
from turtle import update

root = Tk()
root.title("CPPS KARAGIANNIS VASILEIOS")
root.iconbitmap('C:\Programming\GUI')
root.geometry("400x400")
# database
conn = sqlite3.connect('address_book.db')

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()
var8 = IntVar()
var9 = IntVar()

# create cursor
c = conn.cursor()

c.execute(""" CREATE TABLE addressesF( 
          
        first_name text,
        last_name text,
        gender text,
        age integer,
        therapy integer,
        lc   integer,
        sh   integer,
        el   integer,
        wr   integer,
        fi   integer,
        kn   integer,
        hi   integer,
        toe  integer,
        ne   integer,
        r_3m text,
        r_6m text,
        r_9m text
)""")





# delete function
global editor


# delete function
def delete():
    # database
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()

    # delete a record
    c.execute("DELETE from addressesF WHERE oid= " + delete_box.get())

    # commit changes
    conn.commit()

    # close connection
    conn.close()


# submit function
def submit():
    # create or connect to a database
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    # insert into table
    c.execute(
        "INSERT INTO addressesF VALUES(:f_name, :l_name, :gender, :age, :therapy,:lc, :sh, :el, :wr, :fi, :kn, :toe, :hi, :ne,:r_3m,:r_6m,:r_9m)",
        {
            'f_name': f_name.get(),
            'l_name': l_name.get(),
            'gender': gender.get(),
            'age': age.get(),
            'therapy': therapy.get(),
            'lc': var1.get(),
            'sh': var2.get(),
            'el': var3.get(),
            'wr': var4.get(),
            'fi': var5.get(),
            'kn': var6.get(),
            'toe': var7.get(),
            'hi': var8.get(),
            'ne': var9.get(),
            'r_3m': r_3m.get(),
            'r_6m': r_6m.get(),
            'r_9m': r_9m.get()
        })

    # clear textboxes

    r_3m.delete(0, END)
    r_6m.delete(0, END)
    r_9m.delete(0, END)
    # clear textboxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    gender.delete(0, END)
    age.delete(0, END)
    therapy.delete(0, END)

    # commit changes
    conn.commit()

    # close connection
    conn.close()


# checkboxes function
# create edit function to update a record
def edit():
    global editor
    editor = Tk()
    editor.title("CPPS KARAGIANNIS VASILEIOS")
    editor.iconbitmap('C:\Programming\GUI')
    editor.geometry("400x600")
    # create or connect to a database
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()
    record_id = delete_box.get()
    # query the database
    c.execute("SELECT * ,oid FROM addressesF WHERE oid = " + record_id)
    records = c.fetchall()
    print(records)
    # loop thru results
    print_records = ''
    # global variables
    
    global f_name_editor
    global l_name_editor
    global age_editor
    global gender_editor
    global therapy_editor
    global r_6m_editor
    global r_9m_editor

    # text boxes

    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    gender_editor = Entry(editor, width=30)
    gender_editor.grid(row=2, column=1)
    age_editor = Entry(editor, width=30)
    age_editor.grid(row=3, column=1)
    therapy_editor = Entry(editor, width=30)
    therapy_editor.grid(row=4, column=1)
    r_6m_editor = Entry(editor, width=30)
    r_6m_editor.grid(row=5, column=1)
    r_9m_editor = Entry(editor, width=30)
    r_9m_editor.grid(row=6, column=1)
    # text box labels
    f_name_label = Label(editor, text="first name")
    f_name_label.grid(row=0, column=0)
    l_name_label = Label(editor, text="last  name")
    l_name_label.grid(row=1, column=0)
    gender_label = Label(editor, text="gender")
    gender_label.grid(row=2, column=0)
    age_label = Label(editor, text="date of birth")
    age_label.grid(row=3, column=0)
    therapy_label = Label(editor, text="therapy")
    therapy_label.grid(row=4, column=0)
    r_6m_label = Label(editor, text="results after 3 months")
    r_6m_label.grid(row=5, column=0)
    r_9m_label = Label(editor, text="results after 6 months")
    r_9m_label.grid(row=6, column=0)

    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        gender_editor.insert(0, record[2])
        age_editor.insert(0, record[3])
        therapy_editor.insert(0, record[4])
        r_6m_editor.insert(0, record[15])
        r_9m_editor.insert(0, record[16])

    save_btn = Button(editor, text="Update patient data", command=update)
    save_btn.grid(row=7, column=1, columnspan=2, pady=10, padx=10, ipadx=137)

    editor.destroy


# update function
def update():
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    record_id = delete_box.get()

    c.execute("""UPDATE addressesF SET
                first_name = :first,
                last_name = :last,
                gender = :gender,
                age = :age,
                therapy = :therapy,
                r_6m = :r_6m,
                r_9m = :r_9m

                WHERE oid = :oid""",
              {
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'gender': gender_editor.get(),
                  'age': age_editor.get(),
                  'therapy': therapy_editor.get(),
                  'r_6m': r_6m_editor.get(),
                  'r_9m': r_9m_editor.get(),
                  'oid': record_id
              })

    # commit changes
    conn.commit()

    # close connection
    conn.close()

    editor.destroy()


# create querry function
def query():
    # create or connect to a database
    conn = sqlite3.connect('address_book.db')

    # create cursor
    c = conn.cursor()

    # query the database
    c.execute("SELECT * ,oid FROM addressesF")
    records = c.fetchall()
    print(records)
    # loop thru results
    print_records = ''
    for record in records:
        print_records += str(record) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=1, )
    # commit changes
    conn.commit()
    # close connection
    conn.close()


# create text boxes

f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)
gender = Entry(root, width=30)
gender.grid(row=2, column=1)
age = Entry(root, width=30)
age.grid(row=3, column=1)
therapy = Entry(root, width=30)
therapy.grid(row=4, column=1)
r_3m = Entry(root, width=30)
r_3m.grid(row=5, column=1)
r_6m = Entry(root, width=30)
r_6m.grid(row=0, column=7)
r_9m = Entry(root, width=30)
r_9m.grid(row=1, column=7)
delete_box = Entry(root, width=30)
delete_box.grid(row=6, column=10, pady=5)

# create text box labels

f_name_label = Label(root, text="first name")
f_name_label.grid(row=0, column=0)
l_name_label = Label(root, text="last  name")
l_name_label.grid(row=1, column=0)
gender_label = Label(root, text="gender")
gender_label.grid(row=2, column=0)
age_label = Label(root, text="date of birth")
age_label.grid(row=3, column=0)
therapy_label = Label(root, text="therapy")
therapy_label.grid(row=4, column=0)
r_3m_label = Label(root, text="results ")
r_3m_label.grid(row=5, column=0)
r_6m_label = Label(root, text="results after 3 months")
r_6m_label.grid(row=0, column=6)
r_9m_label = Label(root, text="results after 6 months")
r_9m_label.grid(row=1, column=6)

# create submit button
submit_btn = Button(root, text="add record to database", command=submit)
submit_btn.grid(row=2, column=6, columnspan=2, pady=10, padx=10, ipadx=137)

# create a query button
query_btn = Button(root, text="show records", command=query)
query_btn.grid(row=3, column=6, columnspan=2, pady=10, padx=10, ipadx=137)

# edit button
edit_btn = Button(root, text="Edit record from database", command=edit)
edit_btn.grid(row=4, column=6, columnspan=2, pady=10, padx=10, ipadx=137)

# create a delete button
delete_btn = Button(root, text="delete record from database", command=delete)
delete_btn.grid(row=6, column=6, columnspan=2, pady=10, padx=10, ipadx=137)



# checkboxes
c = Checkbutton(root, text="Lumbar colum", variable=var1, onvalue=1, offvalue=0) 
c.deselect()
c.grid(row=8, column=0)

c = Checkbutton(root, text="shoulder", variable=var2, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=8, column=1)

c = Checkbutton(root, text="Elbow", variable=var3, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=8, column=2)

c = Checkbutton(root, text="wrist", variable=var4, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=9, column=0)

c = Checkbutton(root, text="fingers", variable=var5, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=9, column=1)

c = Checkbutton(root, text="knee", variable=var6, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=9, column=2)

c = Checkbutton(root, text="Toes", variable=var7, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=10, column=0)

c = Checkbutton(root, text="Hip", variable=var8, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=10, column=1)

c = Checkbutton(root, text="Neck", variable=var9, onvalue=1, offvalue=0)
c.deselect()
c.grid(row=10, column=2)

# commit changes
conn.commit()
# close connection
conn.close()
root.mainloop()


