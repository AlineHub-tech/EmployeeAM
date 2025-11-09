
import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Database setup
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    check_in TEXT,
    check_out TEXT
)
""")
conn.commit()

# GUI Setup
root = Tk()
root.title("Employee Attendance System")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

Label(root, text="EMPLOYEE ATTENDANCE", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=15)

name_label = Label(root, text="Employee Name:", font=("Arial", 12), bg="#f0f0f0")
name_label.pack()
name_entry = Entry(root, font=("Arial", 12), width=30)
name_entry.pack(pady=5)

def check_in():
    name = name_entry.get()
    if not name:
        messagebox.showwarning("Error", "Please enter a name")
        return
    cursor.execute("INSERT INTO attendance (name, check_in) VALUES (?, ?)", (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    messagebox.showinfo("Success", f"{name} checked in successfully!")

def check_out():
    name = name_entry.get()
    cursor.execute("UPDATE attendance SET check_out = ? WHERE name = ? AND check_out IS NULL", 
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name))
    conn.commit()
    messagebox.showinfo("Success", f"{name} checked out successfully!")

def view_records():
    top = Toplevel(root)
    top.title("Attendance Records")
    top.geometry("600x400")
    Label(top, text="Attendance Records", font=("Arial", 14, "bold")).pack(pady=10)
    records = cursor.execute("SELECT * FROM attendance").fetchall()
    text = Text(top, width=70, height=20)
    text.pack()
    for r in records:
        text.insert(END, f"ID: {r[0]} | Name: {r[1]} | Check-in: {r[2]} | Check-out: {r[3]}\n")

Button(root, text="Check In", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=check_in).pack(pady=5)
Button(root, text="Check Out", font=("Arial", 12), bg="#2196F3", fg="white", width=15, command=check_out).pack(pady=5)
Button(root, text="View Records", font=("Arial", 12), bg="#FF9800", fg="white", width=15, command=view_records).pack(pady=5)

root.mainloop()