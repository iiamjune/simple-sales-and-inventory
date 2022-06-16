from ctypes import alignment
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os.path
from turtle import width

window = Tk()
window.title("Sales and Inventory")
window.geometry("800x600")
window.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

global items_dict
addinput_itemname = StringVar()
addinput_price = StringVar()
addinput_quantity = StringVar()
editinput_itemname = StringVar()
editinput_price = StringVar()
editinput_quantity = StringVar()
editinput_search = StringVar()
purchaseinput_search = StringVar()
purchaseinput_itemname = StringVar()
purchaseinput_quantity = StringVar()
purchase_carttotal = StringVar()
purchase_total = 0.0
purchase_subtotal = 0.0

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
            messagebox.showerror('Warning', 'Item name cannot contain spaces.\nUse "-" to separate item names with more than one word.')
        else:
            itemname_iscorrect = True
            item_name = addinput_itemname.get().strip().title()

    if not addinput_price.get() or addinput_price.get() == '.' or float(addinput_price.get()) == 0:
        price_iscorrect = False
        messagebox.showerror('Error', 'Please enter item price')
    else:
        price_iscorrect = True
        item_price = float(addinput_price.get())
    
    if not addinput_quantity.get() or int(addinput_quantity.get()) == 0:
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
            addinput_itemname.set('')
            addinput_price.set('')
            addinput_quantity.set('')
            add_items_to_file(items_dict, clear=False, message='Item added successfully')
            add_window()

def add_items_to_file(items_dict: dict, clear: bool, message: str):
    if clear:
        f = open('inventory.txt', 'w')
        f.close()
        with open('inventory.txt', 'a') as file:
            for item in items_dict:
                file.write(f"{item}: {items_dict[item]}")
                file.write('\n')
            messagebox.showinfo('Success', message)
        return
    invItems = getInvItems()

    for item in invItems:
        if item in items_dict:
            items_dict[item] += invItems[item]
    with open('inventory.txt', 'a') as file:
        for item in items_dict:
            file.write(f"{item}: {items_dict[item]}")
            file.write('\n')
        messagebox.showinfo('Success', message)

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
    editinput_itemname.set('')
    editinput_price.set('')
    editinput_quantity.set('')
    editinput_search.set('')

def view_binditem(e):
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
    itemname_iscorrect = False

    if not editinput_itemname.get() or len(editinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('Error', 'Please select an item')
    else:
        itemname_iscorrect = True
        item_name = editinput_itemname.get().strip().title()
    
    if itemname_iscorrect:
        invItems = getInvItems()
        item_to_delete = item_name
        if item_to_delete in invItems.keys():
            confirm_delete = messagebox.askyesno('Delete Item', f'Are you sure you want to delete {item_name} from the inventory?')
            if confirm_delete:
                del invItems[item_to_delete]
                editinput_itemname.set('')
                editinput_price.set('')
                editinput_quantity.set('')
                editinput_search.set('')
                add_items_to_file(invItems, clear=True, message=f'{item_name} has been deleted successfully')
                view_window()
        else:
            messagebox.showerror('Error', 'Item does not exist!')

def update_item():
    itemname_iscorrect = False
    price_iscorrect = False
    quantity_iscorrect = False

    if not editinput_itemname.get() or len(editinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('Error', 'Please select an item')
    else:
        if ' ' in editinput_itemname.get():
            messagebox.showerror('Warning', 'Item name cannot contain spaces.\nUse "-" to separate item names with more than one word.')
        else:
            itemname_iscorrect = True
            item_name = editinput_itemname.get().strip().title()

            if not editinput_price.get() or editinput_price.get() == '.' or float(editinput_price.get()) == 0:
                price_iscorrect = False
                messagebox.showerror('Error', 'Please enter item price')
            else:
                price_iscorrect = True
                item_price = float(editinput_price.get())
            
            if not editinput_quantity.get() or int(editinput_quantity.get()) == 0:
                quantity_iscorrect = False
                messagebox.showerror('Error', 'Please enter item quantity')
            else:
                quantity_iscorrect = True
                item_quantity = int(editinput_quantity.get())
    
    if itemname_iscorrect and price_iscorrect and quantity_iscorrect:
        invItems = getInvItems()
        item_to_change = item_name
        if item_to_change in invItems.keys():
            invItems.update({item_name: [{'quantity':int(item_quantity)}, {'price':float(item_price)}]})

            editinput_itemname.set('')
            editinput_price.set('')
            editinput_quantity.set('')
            editinput_search.set('')
            add_items_to_file(invItems, clear=True, message='Item updated successfully')
            view_window()
        else:
            messagebox.showerror('Error', 'Item does not exist!')

def view_searchitem():
    query = edit_searchentry.get().strip().title()
    selection = []
    for child in view_treeview.get_children():
        if query in view_treeview.item(child)['values']:
            selection.append(child)
            editinput_itemname.set(view_treeview.item(child)['values'][0])
            editinput_quantity.set(view_treeview.item(child)['values'][1])
            editinput_price.set(view_treeview.item(child)['values'][2])
    if len(selection) == 0:
        editinput_itemname.set('')
        editinput_quantity.set('')
        editinput_price.set('')
        messagebox.showinfo('Info', 'No results found')
    view_treeview.selection_set(selection)

def view_window():
    global view_treeview
    global edit_searchentry

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
    edit_searchentry = Entry(
        view_frame, 
        width=20, 
        textvariable=editinput_search, 
        font='Arial 8', 
        foreground='black', 
        highlightthickness=1, 
        highlightbackground='#2C4C71', 
        highlightcolor='#2C4C71')
    edit_searchbutton = Button(
        view_frame, 
        text='Search', 
        command=view_searchitem, 
        height=1, 
        width=5, 
        background='#2C4C71', 
        foreground='#E9EEF3')
    edit_itemnamelabel = Label(
        view_frame, 
        text='Item Name', 
        font='Arial 8')
    edit_itemnameentry = Entry(
        view_frame, 
        width=30, 
        textvariable=editinput_itemname, 
        font='Arial 8', 
        state=DISABLED)
    edit_quantitylabel = Label(
        view_frame, 
        text='Quantity', 
        font='Arial 8')
    edit_quantityentry = Entry(
        view_frame, 
        width=10, 
        textvariable=editinput_quantity, 
        font='Arial 8')
    edit_pricelabel = Label(
        view_frame, 
        text='Price', 
        font='Arial 8')
    edit_priceentry = Entry(
        view_frame, 
        width=25, 
        textvariable=editinput_price, 
        font='Arial 8')
    edit_updatebutton = Button(
        view_frame,
        text='UPDATE',
        command=update_item,
        height=8,
        width=30,
        background='#2C4C71',
        foreground='#E9EEF3')
    edit_deletebutton = Button(
        view_frame,
        text='DELETE',
        command=delete_item,
        height=8,
        width=30,
        background='#2C4C71',
        foreground='#E9EEF3')
    
    cols = ('Item Name', 'Quantity', 'Price')
    view_treeview = ttk.Treeview(view_frame, columns=cols, show='headings')
    
    invItems = getInvItems()
    if len(invItems) == 0:
        view_treeview.unbind('<ButtonRelease-1>')
        edit_searchentry.config(state='disabled')
        edit_searchbutton.config(state='disabled')
        edit_quantityentry.config(state='disabled')
        edit_priceentry.config(state='disabled')
        edit_updatebutton.config(state='disabled')
        edit_deletebutton.config(state='disabled')
        messagebox.showerror('Error', 'No items in inventory')
    else:
        view_treeview.bind('<ButtonRelease-1>', view_binditem)

    for col in cols:
        view_treeview.heading(col, text=col)
        view_treeview.grid(row=1, column=0, columnspan=2)
        view_treeview.column(col, anchor='center')
        view_treeview.place(relx=.5, rely=.4, anchor=CENTER)

    tempInvList = []
    for key, value in getInvItems().items():
        tempInvList.append([key,value[0]['quantity'],value[1]['price']])
    tempInvList.sort(key=lambda x: x[2])
    for i in enumerate(tempInvList, start=1):
        view_treeview.insert('', 'end', values=(i[1][0],i[1][1],i[1][2]))
    
    edit_searchentry.place(x=165, y=110, anchor=CENTER)
    edit_searchbutton.place(x=250, y=110, anchor=CENTER)

    edit_itemnamelabel.place(x=150, y=360)
    edit_itemnameentry.place(x=150, y=380)
    edit_quantitylabel.place(x=390, y=360)
    edit_quantityentry.place(x=390, y=380)
    edit_pricelabel.place(x=500, y=360)
    edit_priceentry.place(x=500, y=380)

    edit_updatebutton.place(relx=.3, y=500, anchor=CENTER)
    edit_deletebutton.place(relx=.7, y=500, anchor=CENTER)

def purchase_back():
    if len(purchase_carttreeview.get_children()) > 0:
        confirm_abort = messagebox.askyesno('Abort Operation', f'Are you sure you want to abort this operation?')
        if confirm_abort:
            main_window()
            purchaseinput_itemname.set('')
            purchaseinput_quantity.set('')
            purchaseinput_search.set('')
    else:
        main_window()
        purchaseinput_itemname.set('')
        purchaseinput_quantity.set('')
        purchaseinput_search.set('')

def purchase_searchitem():
    query = purchase_searchentry.get().strip().title()
    selection = []
    for child in purchase_treeview.get_children():
        if query in purchase_treeview.item(child)['values']:
            selection.append(child)
            purchaseinput_itemname.set(purchase_treeview.item(child)['values'][0])
            purchaseinput_quantity.set('1')
    if len(selection) == 0:
        purchaseinput_itemname.set('')
        purchaseinput_quantity.set('')
        messagebox.showinfo('Info', 'No results found')
    purchase_treeview.selection_set(selection)

def purchase_binditem(e):
    value_list = []
    selected_item = purchase_treeview.focus()
    for value in purchase_treeview.item(selected_item)['values']:
        value_list.append(value)
    if len(value_list) > 0:
        purchaseinput_itemname.set('')
        purchaseinput_itemname.set(str(value_list[0]))
        purchaseinput_quantity.set('')
        purchaseinput_quantity.set('1')

def purchase_additem():
    itemname_iscorrect = False
    quantity_iscorrect = False

    if not purchaseinput_itemname.get() or len(purchaseinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('Error', 'Please select an item')
    else:
        if ' ' in purchaseinput_itemname.get():
            messagebox.showerror('Warning', 'Item name cannot contain spaces.\nUse "-" to separate item names with more than one word.')
        else:
            itemname_iscorrect = True
            item_name = purchaseinput_itemname.get().strip().title()
            
            if not purchaseinput_quantity.get() or int(purchaseinput_quantity.get()) == 0:
                quantity_iscorrect = False
                messagebox.showerror('Error', 'Please enter item quantity')
            else:
                quantity_iscorrect = True
                item_quantity = int(purchaseinput_quantity.get())
    
    if itemname_iscorrect and quantity_iscorrect:
        purchase_total = 0.0
        if getInvItems()[item_name][0]['quantity'] >= item_quantity:
            subtotal = getInvItems()[item_name][1]['price'] * item_quantity

            purchase_carttreeview.insert('', 'end', values=(item_name, item_quantity, subtotal))
            purchaseinput_itemname.set('')
            purchaseinput_quantity.set('')

            if len(purchase_carttreeview.get_children()) > 0:
                purchase_removebutton.config(state=NORMAL)
                purchase_checkoutbutton.config(state=NORMAL)

            for child in purchase_carttreeview.get_children():
                purchase_total += float(purchase_carttreeview.item(child)['values'][2])
            purchase_carttotal.set('Total: ₱' + str('{:.2f}'.format(purchase_total)))
        else:
            messagebox.showerror('Error', 'Insufficient quantity')

def purchase_removeitem():
    selected_item = purchase_carttreeview.selection()[0]
    purchase_carttotal.set('Total: ₱' + str('{:.2f}'.format(float(purchase_carttotal.get().split('₱')[1]) - float(purchase_carttreeview.item(selected_item)['values'][2]))))
    purchase_carttreeview.delete(selected_item)
    
    if len(purchase_carttreeview.get_children()) == 0:
        purchase_removebutton.config(state=DISABLED)
        purchase_checkoutbutton.config(state=DISABLED)

def purchase_checkoutitems():
    pass

def purchase_bindcartitem(e):
    value_list = []
    selected_item = purchase_carttreeview.focus()
    for value in purchase_carttreeview.item(selected_item)['values']:
        value_list.append(value)
    if len(value_list) > 0:
        global purchase_subtotal
        purchase_subtotal = 0.0
        purchase_subtotal += float(value_list[2])

def purchase_window():
    global purchase_treeview
    global purchase_searchentry
    global purchase_carttreeview
    global purchase_removebutton
    global purchase_checkoutbutton

    purchase_frame = Frame(window, width=800, height=600)
    purchase_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
    purchase_frame.grid(row=0, column=0, sticky=NW)
    purchase_frame.propagate(0)
    purchase_frame.update()

    Label(
        purchase_frame,
        text='Purchase Item(s)',
        font='Arial 18 bold').place(
            relx=.5,
            y=40,
            anchor=CENTER)
    Button(
        purchase_frame,
        text='Back',
        command=purchase_back,
        height=2,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.04,
            y=40,
            anchor=CENTER)
    purchase_searchentry = Entry(
        purchase_frame, 
        width=20, 
        textvariable=purchaseinput_search, 
        font='Arial 8', 
        foreground='black', 
        highlightthickness=1, 
        highlightbackground='#2C4C71', 
        highlightcolor='#2C4C71')
    purchase_searchbutton = Button(
        purchase_frame, 
        text='Search', 
        command=purchase_searchitem, 
        height=1, 
        width=5, 
        background='#2C4C71', 
        foreground='#E9EEF3')
    purchase_itemnamelabel = Label(
        purchase_frame, 
        text='Item Name', 
        font='Arial 8')
    purchase_itemnameentry = Entry(
        purchase_frame, 
        width=30, 
        textvariable=purchaseinput_itemname, 
        font='Arial 8', 
        state=DISABLED)
    purchase_quantitylabel = Label(
        purchase_frame, 
        text='Quantity', 
        font='Arial 8')
    purchase_quantityentry = Entry(
        purchase_frame, 
        width=10, 
        textvariable=purchaseinput_quantity, 
        font='Arial 8')
    purchase_addbutton = Button(
        purchase_frame, 
        text='Add', 
        command=purchase_additem, 
        height=1, 
        width=5, 
        background='#2C4C71', 
        foreground='#E9EEF3')
    purchase_removebutton = Button(
        purchase_frame, 
        text='Remove', 
        command=purchase_removeitem, 
        state=DISABLED, 
        height=1, 
        width=8, 
        background='#2C4C71', 
        foreground='#E9EEF3')
    purchase_checkoutbutton = Button(
        purchase_frame, 
        text='Checkout', 
        command=purchase_checkoutitems, 
        state=DISABLED, 
        height=1, 
        width=8, 
        background='#2C4C71', 
        foreground='#E9EEF3')
    purchase_totallabel = Label(
        purchase_frame, 
        textvariable=purchase_carttotal, 
        font='Arial 14 bold')
    
    cols = ('Item Name', 'Quantity', 'Price')
    purchase_treeview = ttk.Treeview(purchase_frame, columns=cols, show='headings')
    
    invItems = getInvItems()
    if len(invItems) == 0:
        purchase_treeview.unbind('<ButtonRelease-1>')
        purchase_searchentry.config(state='disabled')
        purchase_searchbutton.config(state='disabled')
        purchase_quantityentry.config(state='disabled')
        purchase_addbutton.config(state='disabled')
        messagebox.showerror('Error', 'No items in inventory')
    else:
        purchase_treeview.bind('<ButtonRelease-1>', purchase_binditem)

    for col in cols:
        purchase_treeview.heading(col, text=col)
        purchase_treeview.grid(row=1, column=0, columnspan=2)
        purchase_treeview.column(col, anchor=CENTER)
        purchase_treeview.place(relx=.5, rely=.4, anchor=CENTER)

    tempInvList = []
    for key, value in getInvItems().items():
        tempInvList.append([key,value[0]['quantity'],value[1]['price']])
    tempInvList.sort(key=lambda x: x[2])
    for i in enumerate(tempInvList, start=1):
        purchase_treeview.insert('', 'end', values=(i[1][0],i[1][1],i[1][2]))
    
    purchase_searchentry.place(x=165, y=110, anchor=CENTER)
    purchase_searchbutton.place(x=250, y=110, anchor=CENTER)

    purchase_itemnamelabel.place(x=180, y=360)
    purchase_itemnameentry.place(x=180, y=380)
    purchase_quantitylabel.place(x=420, y=360)
    purchase_quantityentry.place(x=420, y=380)
    purchase_addbutton.place(x=530, y=370)

    cart_cols = ('Item Name', 'Quantity', 'Subtotal')
    purchase_carttreeview = ttk.Treeview(purchase_frame, columns=cart_cols, show='headings', height=6)

    if len(invItems) == 0:
        purchase_carttreeview.unbind('<ButtonRelease-1>')
        purchase_removebutton.config(state='disabled')
        purchase_checkoutbutton.config(state='disabled')
    else:
        purchase_carttreeview.bind('<ButtonRelease-1>', purchase_bindcartitem)
    
    for col in cart_cols:
        purchase_carttreeview.heading(col, text=col)
        purchase_carttreeview.grid(row=1, column=0, columnspan=2)
        purchase_carttreeview.column(col, anchor=CENTER)
        purchase_carttreeview.place(x=100, y=410)
    purchase_carttreeview.column('#1', anchor=CENTER, width=200)
    purchase_carttreeview.column('#2', anchor=CENTER, width=80)
    purchase_carttreeview.column('#3', anchor=CENTER, width=120)
    
    purchase_removebutton.place(x=530, y=440)
    purchase_checkoutbutton.place(x=530, y=470)
    purchase_totallabel.place(x=530, y=500)
    purchase_carttotal.set('Total: ₱0.00')

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