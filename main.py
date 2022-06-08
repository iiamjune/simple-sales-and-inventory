from cgitb import text
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import dot, width
from wsgiref import validate

window = Tk()
window.title("Sales and Inventory")
window.geometry("800x600")
window.resizable(False, False)
global add_e1
global add_e2
global e3
global e4
global total
global balance
global items_dict
dot_counter = 0

style = ttk.Style()
style.theme_use("clam")

total = StringVar()
balance = IntVar()
addinput_itemname = StringVar()
addinput_price = StringVar()
items_dict = {}

def only_numbers(char):
    return char.isdigit() or char == '.'

validation = window.register(only_numbers)

def add_back():
    main_window()
    addinput_itemname.set("")
    addinput_price.set("")

def add_items():
    itemname_iscorrect = False
    price_iscorrect = False

    if not addinput_itemname.get() or len(addinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showinfo("Error", "Please enter item name")
    else:
        itemname_iscorrect = True
        item_name = addinput_itemname.get().strip().title()

    if not addinput_price.get() or addinput_price.get() == "." or float(addinput_price.get()) == 0:
        price_iscorrect = False
        messagebox.showinfo("Error", "Please enter item price")
    else:
        price_iscorrect = True
        item_price = float(addinput_price.get())
    
    if itemname_iscorrect and price_iscorrect:
        if item_name in items_dict:
            messagebox.showinfo("Error", "Item already exists")
        else:
            items_dict[item_name] = item_price
            messagebox.showinfo("Success", "Item added")
            add_back()
            addinput_itemname.set("")
            addinput_price.set("")

def add_window():
    add_frame = Frame(window, width=800, height=600)
    add_frame.tk_setPalette(background="#E9EEF3", foreground="#2C4C71")
    add_frame.grid(row=0, column=0, sticky=NW)
    add_frame.propagate(0)
    add_frame.update()

    Label(
        add_frame,
        text="Add Item(s)",
        font="Arial 18 bold").place(
            relx=.5,
            y=40,
            anchor=CENTER)
    Button(
        add_frame,
        text="Back",
        command=add_back,
        height=2,
        width=5,
        background="#2C4C71",
        foreground="#E9EEF3").place(
            relx=.03,
            y=40)
    Label(
        add_frame,
        text="Item Name",
        font="Arial 14 bold").place(
            x=60,
            y=210)
    add_e1 = Entry(
        add_frame,
        width=30,
        textvariable=addinput_itemname,
        font="Arial 14",
        foreground="black",
        highlightthickness=1,
        highlightbackground="#2C4C71",
        highlightcolor="#2C4C71").place(
            x=60,
            y=250)
    Label(
        add_frame,
        text="Price",
        font="Arial 14 bold").place(
            x=450,
            y=210)
    add_e2 = Entry(
        add_frame,
        width=25,
        textvariable=addinput_price,
        font="Arial 14",
        foreground="black",
        highlightthickness=1,
        highlightbackground="#2C4C71",
        highlightcolor="#2C4C71",
        validate="key",
        validatecommand=(validation, "%S")).place(
            x=450,
            y=250)
    Button(
        add_frame,
        text="ADD",
        command=add_items,
        height=8,
        width=30,
        background="#2C4C71",
        foreground="#E9EEF3").place(
            relx=.5,
            y=490,
            anchor=CENTER)

def view_window():
    print("View")

def purchase_window():
    print("Purchase")

def main_window():
    main_frame = Frame(window, width=800, height=600)
    main_frame.tk_setPalette(background="#446285", foreground="#A5B8CC")
    main_frame.grid(row=0, column=0, sticky=NW)
    main_frame.grid_propagate(0)
    main_frame.update()
    
    Label(
        main_frame,
        text="Sales and Inventory System",
        font="Arial 18 bold").place(relx=.5,
        y=40,
        anchor=CENTER)
    Button(
        main_frame,
        text="Add Item(s)",
        command=add_window,
        height=8,
        width=30,
        background="#A5B8CC",
        foreground="black").place(
            relx=.5,
            y=190,
            anchor=CENTER)
    Button(
        main_frame,
        text="View Item(s)",
        command=view_window,
        height=8,
        width=30,
        background="#A5B8CC",
        foreground="black").place(
            relx=.5,
            y=340,
            anchor=CENTER)
    Button(
        main_frame,
        text="Purchase Item(s)",
        command=purchase_window,
        height=8,
        width=30,
        background="#A5B8CC",
        foreground="black").place(
            relx=.5,
            y=490,
            anchor=CENTER)


# var1 = IntVar()
# Checkbutton(window, text="Item 1", variable=var1).place(x=5, y=50)

# var_dropdown = StringVar()
# items_dropdown = OptionMenu(window, var_dropdown, *list(items_dict.items()))
# items_dropdown.pack()
# items_dropdown.place(x=5, y=80)

# cols = ("Item", "Price")
# grid_items = ttk.Treeview(window, columns=cols, show="headings")

# for col in cols:
#     grid_items.heading(col, text=col)
#     grid_items.grid(row=1, column=0, columnspan=2)
#     # grid_items.place(x=10, y=100)
# grid_items.column("Item", width=500, stretch=NO)
# grid_items.column("Price", stretch=NO)
# grid_items.pack()

main_window()
window.mainloop()