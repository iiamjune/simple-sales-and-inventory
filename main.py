from cgitb import text
from email import message
from select import select
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import dot, width
from wsgiref import validate
import os.path

window = Tk()
window.title("Sales and Inventory")
window.geometry("800x600")
window.resizable(False, False)
global items_dict

style = ttk.Style()
style.theme_use("clam")

total = StringVar()
balance = IntVar()
addinput_itemname = StringVar()
addinput_price = StringVar()
addinput_quantity = StringVar()
editinput_itemname = StringVar()
editinput_price = StringVar()
editinput_quantity = StringVar()

def only_numbersdecimal(char):
    return char.isdigit() or char == '.'

def only_numbers(char):
    return char.isdigit()

price_validation = window.register(only_numbersdecimal)
quantity_validation = window.register(only_numbers)

def add_back():
    main_window()
    addinput_itemname.set('')
    addinput_price.set('')
    addinput_quantity.set('')

def add_items():
    itemname_iscorrect = False
    price_iscorrect = False
    quantity_iscorrect = False
    items_dict = {}

    if not addinput_itemname.get() or len(addinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('Error', 'Please enter item name')
    else:
        if ' ' in addinput_itemname.get():
            messagebox.showerror('Warning', 'Item name cannot contain spaces.\nUse "-" to separate item names with more than one word')
        else:
            itemname_iscorrect = True
            item_name = addinput_itemname.get().strip().title()

    if not addinput_price.get() or addinput_price.get() == '.' or float(addinput_price.get()) == 0:
        price_iscorrect = False
        messagebox.showerror('Error', 'Please enter item price')
    else:
        price_iscorrect = True
        item_price = float(addinput_price.get())
    
    if not addinput_quantity.get() or float(addinput_quantity.get()) == 0:
        quantity_iscorrect = False
        messagebox.showerror('Error', 'Please enter item quantity')
    else:
        quantity_iscorrect = True
        item_quantity = int(addinput_quantity.get())
    
    if itemname_iscorrect and price_iscorrect and quantity_iscorrect:
        invItems = getInvItems()
        if item_name in invItems.keys():
            messagebox.showerror('Error', 'Item already exists')
        else:
            items_dict[item_name] = [{"quantity":item_quantity}, {"price":item_price}]
            add_back()
            addinput_itemname.set('')
            addinput_price.set('')
            addinput_quantity.set('')
            add_items_to_file(items_dict, clear=False)

def add_items_to_file(items_dict: dict, clear: bool):
    if clear:
        f = open('inventory.txt', 'w')
        f.close()
        with open('inventory.txt', 'a') as file:
            for item in items_dict:
                file.write(f"{item}: {items_dict[item]}")
                file.write('\n')
        return
    invItems = getInvItems()

    for item in invItems:
        if item in items_dict:
            items_dict[item] += invItems[item]
    with open('inventory.txt', 'a') as file:
        for item in items_dict:
            file.write(f"{item}: {items_dict[item]}")
            file.write('\n')
        messagebox.showinfo("Success", "Item added")

def getInvItems():
    invItems = {}

    if os.path.exists('inventory.txt') == False:
        f = open('inventory.txt', 'w')
        f.close()
    else:
        with open('inventory.txt', 'r') as file:
            for line in file:
                line = line.replace('\n','').split(' ')
                item_name, item_quantity, item_price = line[0].replace(':',''), line[2].replace('},',''), line[4].replace('}]','')
                invItems.update({item_name: [{'quantity':int(item_quantity)}, {'price':float(item_price)}]})
    
    return invItems

def add_window():
    add_frame = Frame(window, width=800, height=600)
    add_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
    add_frame.grid(row=0, column=0, sticky=NW)
    add_frame.propagate(0)
    add_frame.update()

    Label(
        add_frame,
        text='Add Item(s)',
        font='Arial 18 bold').place(
            relx=.5,
            y=40,
            anchor=CENTER)
    Button(
        add_frame,
        text='Back',
        command=add_back,
        height=2,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.04,
            y=40,
            anchor=CENTER)
    Label(
        add_frame,
        text='Item Name',
        font='Arial 14 bold').place(
            x=60,
            y=160)
    Entry(
        add_frame,
        width=30,
        textvariable=addinput_itemname,
        font='Arial 14',
        foreground='black',
        highlightthickness=1,
        highlightbackground='#2C4C71',
        highlightcolor='#2C4C71').place(
            x=60,
            y=200)
    Label(
        add_frame,
        text='Price',
        font='Arial 14 bold').place(
            x=450,
            y=160)
    Entry(
        add_frame,
        width=25,
        textvariable=addinput_price,
        font='Arial 14',
        foreground='black',
        highlightthickness=1,
        highlightbackground='#2C4C71',
        highlightcolor='#2C4C71',
        validate='key',
        validatecommand=(price_validation, '%S')).place(
            x=450,
            y=200)
    Label(
        add_frame,
        text='Quantity',
        font='Arial 14 bold').place(
            x=450,
            y=250)
    Entry(
        add_frame,
        width=10,
        textvariable=addinput_quantity,
        font='Arial 14',
        foreground='black',
        highlightthickness=1,
        highlightbackground='#2C4C71',
        highlightcolor='#2C4C71',
        validate='key',
        validatecommand=(quantity_validation, '%S')).place(
            x=450,
            y=290)
    Button(
        add_frame,
        text='ADD',
        command=add_items,
        height=8,
        width=30,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.5,
            y=490,
            anchor=CENTER)

def view_back():
    main_window()

def bind_item(e):
    value_list = []
    selected_item = view_treeview.focus()
    for value in view_treeview.item(selected_item)['values']:
        value_list.append(value)
    editinput_itemname.set('')
    editinput_itemname.set(str(value_list[0]))
    editinput_quantity.set('')
    editinput_quantity.set(str(value_list[1]))
    editinput_price.set('')
    editinput_price.set(str(value_list[2]))

def delete_item():
    pass

def save_item():
    pass

def view_window():
    global view_treeview

    view_frame = Frame(window, width=800, height=600)
    view_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
    view_frame.grid(row=0, column=0, sticky=NW)
    view_frame.propagate(0)
    view_frame.update()

    Label(
        view_frame,
        text='View Item(s)',
        font='Arial 18 bold').place(
            relx=.5,
            y=40,
            anchor=CENTER)
    Button(
        view_frame,
        text='Back',
        command=view_back,
        height=2,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.04,
            y=40,
            anchor=CENTER)
    
    cols = ('Item Name', 'Quantity', 'Price')
    view_treeview = ttk.Treeview(view_frame, columns=cols, show='headings')
    view_treeview.bind('<ButtonRelease-1>', bind_item)
    
    for col in cols:
        view_treeview.heading(col, text=col)
        view_treeview.grid(row=1, column=0, columnspan=2)
        view_treeview.place(relx=.5, rely=.4, anchor=CENTER)
    
    tempInvList = []
    for key, value in getInvItems().items():
        tempInvList.append([key,value[0]['quantity'],value[1]['price']])
    tempInvList.sort(key=lambda x: x[2])
    for i in enumerate(tempInvList, start=1):
        view_treeview.insert('', 'end', values=(i[1][0],i[1][1],i[1][2]))
    
    
    Label(view_frame, text='Item Name', font='Arial 8').place(x=150, y=360)
    Entry(view_frame, width=30, textvariable=editinput_itemname, font='Arial 8').place(x=150, y=380)
    Label(view_frame, text='Quantity', font='Arial 8').place(x=390, y=360)
    Entry(view_frame, width=10, textvariable=editinput_quantity, font='Arial 8').place(x=390, y=380)
    Label(view_frame, text='Price', font='Arial 8').place(x=500, y=360)
    Entry(view_frame, width=25, textvariable=editinput_price, font='Arial 8').place(x=500, y=380)
    
    # Button(
    #     view_frame,
    #     text='EDIT',
    #     command=edit_item,
    #     height=8,
    #     width=30,
    #     background='#2C4C71',
    #     foreground='#E9EEF3').place(
    #         relx=.2,
    #         y=500,
    #         anchor=CENTER)
    
    Button(
        view_frame,
        text='SAVE',
        command=save_item,
        height=8,
        width=30,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.3,
            y=500,
            anchor=CENTER)
    
    Button(
        view_frame,
        text='DELETE',
        command=delete_item,
        height=8,
        width=30,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.7,
            y=500,
            anchor=CENTER)

def purchase_window():
    print('Purchase')

def main_window():
    main_frame = Frame(window, width=800, height=600)
    main_frame.tk_setPalette(background='#446285', foreground='#A5B8CC')
    main_frame.grid(row=0, column=0, sticky=NW)
    main_frame.grid_propagate(0)
    main_frame.update()
    
    Label(
        main_frame,
        text='Sales and Inventory System',
        font='Arial 18 bold').place(relx=.5,
        y=40,
        anchor=CENTER)
    Button(
        main_frame,
        text='Add Item(s)',
        command=add_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=190,
            anchor=CENTER)
    Button(
        main_frame,
        text='View Item(s)',
        command=view_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=340,
            anchor=CENTER)
    Button(
        main_frame,
        text='Purchase Item(s)',
        command=purchase_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=490,
            anchor=CENTER)

main_window()
window.mainloop()