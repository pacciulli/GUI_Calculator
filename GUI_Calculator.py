import tkinter as tk
from tkinter import ttk, END
import re
import math

window = tk.Tk()

window.title("Smart Calculator")
window.minsize(400, 400)

i = 0
operation_tag = 0


# Function definition
def get_variables(num):
    global i, operation_tag

    hist = historic_display_string.get()

    if (hist and operation_tag == 1) or display_string.get() == 'INF':
        update_display(str(num))
        operation_tag = 0

    elif not(is_float()) or (is_float() and num != "."):
        display.configure(state='normal')
        display.insert(i, num)
        display.configure(state='disable')
        i += 1


def get_operation(operation):
    global operation_tag

    hist = historic_display_string.get()
    num = display_string.get()

    if (not hist or re.findall(r"\=\Z", hist)) and display_string.get() == 'INF':
        update_hist_display(num, operation)

    elif display_string.get() == 'INF':
        update_display('')

    else:
        to_compute()
        num = display_string.get()
        update_hist_display(num, operation)

    operation_tag = 1


def key_pressed(event):
    pressed_num = re.findall(r"\d", event.char)
    pressed_operator = re.findall(r"\+|\-|\*|\/", event.char)

    if pressed_num:
        get_variables(pressed_num[0])

    if pressed_operator:
        get_operation(pressed_operator[0])

    if event.keysym == "C" or event.keysym == "c":
        clear_all()

    if event.keysym == "BackSpace":
        undo()

    if event.keysym == "Return":
        to_compute()


def undo():
    global i
    if i > 0:
        update_display(display_string.get()[:-1])


def clear_all():
    global i
    display.configure(state='normal')
    display.delete(0, END)
    display.configure(state='disable')
    i = 0

    historic_display.configure(state='normal')
    historic_display.delete(0, END)
    historic_display.configure(state='disable')


def update_display(*args):
    global i

    string_to_write = ''
    for arg in args:
        string_to_write += str(arg)

    i = 0
    display.configure(state='normal')
    display.delete(0, END)
    display.insert(0, string_to_write)
    display.configure(state='disable')
    i = len(string_to_write)


def update_hist_display(*args):
    string_to_write = ''
    for arg in args:
        string_to_write += str(arg)

    historic_display.configure(state='normal')
    historic_display.delete(0, END)
    historic_display.insert(0, string_to_write)
    historic_display.configure(state='disable')


def negative():
    global i
    full_string = display_string.get()
    if re.findall(r"\d", full_string):
        if is_float():
            if re.findall(r"\.\Z", full_string):
                i += 1
            num = float(full_string) * -1
        else:
            num = int(full_string) * -1

        if num > 0:
            display.configure(state='normal')
            display.delete(0, END)
            display.insert(0, num)
            display.configure(state='disable')
            i -= 1
        else:
            display.configure(state='normal')
            display.delete(0, END)
            display.insert(0, num)
            display.configure(state='disable')
            i += 1


def percent():
    num1 = historic_display_string.get()
    num2 = display_string.get()

    if num1:
        update_display(str(float(num1[:-1])*float(num2)/100))

    else:
        update_display('0')


def invert():
    pass


def to_compute():
    global i, operation_tag

    num1 = historic_display_string.get()
    num2 = display_string.get()

    if re.findall(r"\=\Z", num1):
        operation = re.findall(r"\+.+|\-.+|\*.+|\/.+", num1)[0][:-2]
        res = eval(num2+operation)
        update_hist_display(num2, operation, " =")
        update_display(str(res))

    else:
        try:
            res = eval(num1+num2)
            update_hist_display(num1, num2, " =")
            update_display(str(res))

        except ZeroDivisionError:
            update_display('INF')
            update_hist_display('')

    operation_tag = 1


def is_float():
    num = display_string.get()
    if re.findall(r"\.", num):
        return True
    else:
        return False


window.bind("<Key>", key_pressed)

label = tk.Label(window, text=" ", width=3)
label.grid(column=0, row=0)

historic_display_string = tk.StringVar()
historic_display = ttk.Entry(window, width=25, textvariable=historic_display_string, state='disable')
historic_display.grid(column=1, row=0, columnspan=4)

display_string = tk.StringVar()
display = ttk.Entry(window, width=25, textvariable=display_string, state='disable')
display.grid(column=1, row=1, columnspan=4)

# Buttons definition and positioning
# Keypad
ttk.Button(window, text="0", command=lambda: get_variables(0), width=5).grid(column=2, row=9)
ttk.Button(window, text="1", command=lambda: get_variables(1), width=5).grid(column=1, row=8)
ttk.Button(window, text="2", command=lambda: get_variables(2), width=5).grid(column=2, row=8)
ttk.Button(window, text="3", command=lambda: get_variables(3), width=5).grid(column=3, row=8)
ttk.Button(window, text="4", command=lambda: get_variables(4), width=5).grid(column=1, row=7)
ttk.Button(window, text="5", command=lambda: get_variables(5), width=5).grid(column=2, row=7)
ttk.Button(window, text="6", command=lambda: get_variables(6), width=5).grid(column=3, row=7)
ttk.Button(window, text="7", command=lambda: get_variables(7), width=5).grid(column=1, row=6)
ttk.Button(window, text="8", command=lambda: get_variables(8), width=5).grid(column=2, row=6)
ttk.Button(window, text="9", command=lambda: get_variables(9), width=5).grid(column=3, row=6)
ttk.Button(window, text=".", command=lambda: get_variables('.'), width=5).grid(column=3, row=9)

# Operations
ttk.Button(window, text="+/-", command=lambda: negative(), width=5).grid(column=1, row=9)
ttk.Button(window, text="<=", command=lambda: undo(), width=5).grid(column=4, row=4)
ttk.Button(window, text="C", command=lambda: clear_all(), width=5).grid(column=3, row=4)
ttk.Button(window, text="+", command=lambda: get_operation('+'), width=5).grid(column=4, row=8)
ttk.Button(window, text="-", command=lambda: get_operation('-'), width=5).grid(column=4, row=7)
ttk.Button(window, text="*", command=lambda: get_operation('*'), width=5).grid(column=4, row=6)
ttk.Button(window, text="/", command=lambda: get_operation('/'), width=5).grid(column=4, row=5)
ttk.Button(window, text="x\u00b2", command=lambda: get_operation('pow'), width=5).grid(column=2, row=5)
ttk.Button(window, text="\u221a", command=lambda: get_operation('sqrt'), width=5).grid(column=3, row=5)
ttk.Button(window, text="1/x", command=lambda: get_operation('inv'), width=5).grid(column=1, row=5)
ttk.Button(window, text="%", command=lambda: percent(), width=5).grid(column=2, row=4)
ttk.Button(window, text="=", command=lambda: to_compute(), width=5).grid(column=4, row=9)

# Main loop
window.mainloop()
