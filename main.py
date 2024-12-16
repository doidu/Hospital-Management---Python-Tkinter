from patient import Patient
from functools import partial
from tkinter import *
from tkinter import ttk
import queueha as q
from tkinter import messagebox

win_control = Tk()
win_control.title("Hospital Queue Management")
win_width = 1290
win_height = 720
win_control.geometry(f"{win_width}x{win_height}+{(win_control.winfo_screenwidth() - win_width) // 2}+{(win_control.winfo_screenheight() - win_height) // 2}")

patient_queue = [None]
token_no = int(6)
all_patient = []

def clear_inputs():
    for box in txtbox_info:
        try: box.set('')
        except: box.delete(0, END)
    error_label.grid_forget()
    

def add_to_queue(pr):
    global token_no
    try:
        for box in txtbox_info:
            if not box.get():
                raise ValueError
        token_no += 1
        new_patient = Patient()
        if pr == 10: new_patient.setPriority("Emergency")
        if pr == 20: new_patient.setPriority("Urgent")
        if pr == 30: new_patient.setPriority("Non-Urgent")
        new_patient.setToken(int(token_no))
        new_patient.setPatientNo(int(15+token_no))
        new_patient.setName(txtbox_info[0].get())
        new_patient.setAge(int(txtbox_info[1].get()))
        new_patient.setSex(txtbox_info[2].get())
        new_patient.setBlood(txtbox_info[3].get())
        patient_queue.append((pr, str(new_patient)))
        all_patient.append(new_patient)
        clear_inputs()
    except ValueError:
        error_label.grid(row=rownum+1, column=0, columnspan=2)
        error_label.after(5000, error_label.grid_forget)
    

frame_content = Frame(win_control)

# *** MENU QUEUE CONTENTS
frame_queue = Frame(frame_content)
frame_form = Frame(frame_queue)
frame_form.pack(side=LEFT, fill=Y, expand=TRUE)
txtbox_info =[]
rownum = colnum = 0
Label(frame_form, text="Patient Form", font=("Arial", 24)).grid(row=rownum, column=colnum, columnspan=2)
for i, txt in enumerate(["Name", "Age", "Sex", "Blood Type"]):
    Label(frame_form, text=f"{txt}:", font=("Arial", 16), justify=LEFT).grid(sticky=W, row=rownum+1, column=colnum, padx=20)
    rownum += 1
    if txt == "Blood Type":
        dropdown = ttk.Combobox(frame_form, state="readonly", values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], font=("Arial", 14))
        dropdown.grid(row=rownum+1, column=colnum, padx=20)
        txtbox_info.append(dropdown)
        rownum += 1
        continue
    if txt == "Sex":
        dropdown = ttk.Combobox(frame_form, state="readonly", values=["Male", "Female"], font=("Arial", 14))
        dropdown.grid(row=rownum+1, column=colnum, padx=20)
        txtbox_info.append(dropdown)
        rownum += 1
        continue
    txtbox = Entry(frame_form, font=("Arial", 16))
    txtbox.grid(row=rownum+1, column=colnum, padx=20)
    txtbox_info.append(txtbox)
    rownum += 1
    if i == 1:
        colnum = 1
        rownum = 0
error_label = Label(frame_form, text="Invalid Input", font=("Arial", 24), fg="red")
frame_btns = Frame(frame_queue)
frame_btns.pack(side=LEFT, fill=BOTH, expand=TRUE)
Button(frame_btns, text="Emergency", font=("Arial", 16), bg="red", width=15, height=2, command=partial(add_to_queue, 10)).pack(pady=20)
Button(frame_btns, text="Urgent", font=("Arial", 16), bg="yellow", width=15, height=2, command=partial(add_to_queue, 20)).pack()
Button(frame_btns, text="Non-Urgent", font=("Arial", 16), bg="green", width=15, height=2, command=partial(add_to_queue, 30)).pack(pady=20)

# *** MENU QUEUE STATUS CONTENT
frame_status = Frame(frame_content)

frame_tree = Frame(frame_status)
frame_tree.pack(side=RIGHT, fill=BOTH)

frame_deque = Frame(frame_status)
frame_deque.pack(side=RIGHT)

def dequeue():
    if len(patient_queue) > 0:
        patient_queue.pop(1)
    menu_status()

Button(frame_deque, text="Dequeu", font=("Arial", 16), bg="red", width=15, height=2, command=dequeue).pack(padx=10)

head = ["Awaiting", "Token No.", "Status"]

style = ttk.Style()
style.theme_use("alt")
style.configure("Treeview.Heading", font=("Comic Sans MS", 10), background="#6c9d6c")
style.configure("Treeview", font=("Comic Sans MS", 10), background="#a1a69f", rowheight=40)
tree = ttk.Treeview(frame_status, columns=head, show='headings')
scroll = Scrollbar(frame_status, orient=VERTICAL, command=tree.yview)



def forget_children(widget):
    for child in widget.winfo_children():
        child.forget()

def menu_queue():
    forget_children(frame_content)
    frame_queue.pack(fill=BOTH, expand=TRUE)

def menu_status():
    def OnDoubleClick(event):
        item = tree.identify('item', event.x, event.y)
        for pt in all_patient:
            if pt.getToken() == int(tree.item(item, "values")[1]):
                messagebox.showinfo("Patient Information", f"Token: {pt.getToken()}\nName: {pt.getName()}\nAge: {pt.getAge()}\nSex: {pt.getSex()}\nBlood Type: {pt.getBlood()}")
    forget_children(frame_content)
    frame_status.pack(fill=BOTH, expand=TRUE)
    tree.delete(*tree.get_children())
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scroll.pack(side=RIGHT, fill=Y, anchor=E)
    q.heap_sort(patient_queue)
    # print(patient_queue[1:])
    for txt in head:
        tree.heading(txt, text=txt)
        tree.column(txt, width=75, minwidth=25, anchor=CENTER)
    for patient in patient_queue[1:]:
        info = patient[1].split(',')
        tree.insert("", END, values=(f"Patient {info[1]}", info[0], info[2]))
    tree.config(yscrollcommand=scroll.set)
    tree.bind("<Double-1>", OnDoubleClick)



def menu_history():
    forget_children(frame_content)




menu_txtcmd = {"Queue New Patient":menu_queue, "Queue Status":menu_status}

frame_menu = Frame(win_control)
frame_menu.pack(side=TOP, fill=X)
frame_content.pack(fill=BOTH, expand=TRUE)

for key, value in menu_txtcmd.items():
    btn = Button(frame_menu, text=key, font=("Arial", 16), relief=RAISED, command=value)
    btn.pack(side=LEFT,fill=BOTH, padx=5, pady=5, expand=True)


win_control.mainloop()