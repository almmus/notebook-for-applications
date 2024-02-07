from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import date, datetime


class App:
    conn = sqlite3.connect("list_of_app.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS applications (
             court text,
             user_name text,
             problem text,
             ip_address text,
             phone text,
             date text)""")

    def __init__(self, main):
        self.editor = Text(wrap="word")
        self.editor.place(height=120, width=600, x=5, y=5)
        self.editor.bind("<KeyRelease-Return>", self.submit)

        self.query_btn = ttk.Button(main, text="Показать результаты", command=self.query)
        self.query_btn.place(height=50, width=135, x=150, y=200)

        self.label = Label(main, text="Выберите дату заявки:")
        self.label.place(height=50, width=150, x=5, y=150)

        self.label_error = Label(main, text="Некорректно введена дата, не выбран день или месяц заявки")

        self.days = [day for day in range(1, 32)]
        self.combobox_day = ttk.Combobox(values=self.days, state="readonly")
        self.combobox_day.place(height=25, width=35, x=150, y=160)

        self.months = [month for month in range(1, 13)]
        self.combobox_month = ttk.Combobox(values=self.months, state="readonly")
        self.combobox_month.place(height=25, width=35, x=200, y=160)

        self.years = [year for year in range(24, 31)]
        self.years_var = IntVar(value=self.years[0])
        self.combobox_year = ttk.Combobox(textvariable=self.years_var, values=self.years, state="readonly")
        self.combobox_year.place(height=25, width=35, x=250, y=160)

    def submit(self, event):
        court = self.editor.get("1.0", "end").split(" ")[0]
        user_name = self.editor.get("1.0", "end").split(" ")[1]
        problem = " ".join(self.editor.get("1.0", "end").split(" ")[2:-2])
        ip_address = self.editor.get("1.0", "end").split(" ")[-2]
        phone = self.editor.get("1.0", "end").split(" ")[-1]
        date_of_app = date.today()
        conn = sqlite3.connect("list_of_app.db")
        c = conn.cursor()
        c.execute("INSERT INTO applications VALUES (:court, :user_name, :problem, :ip_address, :phone, :date)",
        {
            'court': court,
            'user_name': user_name,
            'problem': problem,
            'ip_address': ip_address,
            'phone': phone,
            'date': date_of_app,
        })

        conn.commit()
        conn.close()
        self.editor.delete("1.0", END)

    def query(self):
        if self.is_data_correct(self.combobox_day.get(), self.combobox_month.get()):
            self.label_error.destroy()
            result_window = Toplevel()
            result_window.title("Результаты")
            result_window.geometry("400x400")
            text_res = Text(result_window, height=30, wrap="word")
            text_res.pack(anchor=N, fill=X)
            date_from_combobox = self.get_data()
            if date_from_combobox == 0:
                conn = sqlite3.connect("list_of_app.db")
                c = conn.cursor()
                c.execute("SELECT oid, * FROM applications")
                records = c.fetchall()
                print_records = ''
                for record in records:
                    print_records += f"{record[0]} {record[1]} {record[2]} {record[3]} {record[4]}" \
                                     f" {record[5]}"
                text_res.insert("1.0", print_records)
            else:
                conn = sqlite3.connect("list_of_app.db")
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM applications WHERE date = " + "'" + str(date_from_combobox) + "'")
                records = c.fetchall()
                print_records = ''
                for record in range(len(records)):
                    print_records += f"{record + 1} {records[record][0]} {records[record][1]}" \
                                     f" {records[record][2]} {records[record][3]} {records[record][4]}"
                text_res.insert("1.0", print_records)
        else:
            self.label_error.pack(pady=280)


    def get_data(self):
        d = self.combobox_day.get()
        m = self.combobox_month.get()
        y = self.combobox_year.get()
        dt = f'{d}.{m}.{y}'
        if len(dt) == 4: #если дата не введена, то возвращаем 0
            return 0
        return datetime.strptime(dt, '%d.%m.%y').date()

    def is_data_correct(self, day, month):
        if(len(day) != 0 and len(month) == 0) or (len(day) == 0 and len(month) != 0):
            return False
        return True



root = Tk()
root.title("Заявки")
root.geometry("600x600")

app = App(root)

root.mainloop()

