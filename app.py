import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# کلاس Resident برای نگهداری اطلاعات ساکن
class Resident:
    def __init__(self, id, first_name, last_name, num_people, floor, unit, phone, mobile):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.num_people = num_people
        self.floor = floor
        self.unit = unit
        self.phone = phone
        self.mobile = mobile

# کلاس BuildingManager برای مدیریت پایگاه داده و عملیات
class BuildingManager:
    def __init__(self):
        self.conn = sqlite3.connect('building.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # ایجاد جدول اگر وجود نداشته باشد
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS residents (
                                id TEXT PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                num_people INTEGER,
                                floor INTEGER,
                                unit INTEGER,
                                phone TEXT,
                                mobile TEXT)''')
        self.conn.commit()

    def add_resident(self, resident):
        try:
            self.cursor.execute('''INSERT INTO residents VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (resident.id, resident.first_name, resident.last_name, resident.num_people,
                                 resident.floor, resident.unit, resident.phone, resident.mobile))
            self.conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("خطا", "آیدی تکراری است!")
        
    def delete_resident(self, resident_id):
        self.cursor.execute('''DELETE FROM residents WHERE id = ?''', (resident_id,))
        self.conn.commit()

    def edit_resident(self, resident_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(f'''UPDATE residents SET {key} = ? WHERE id = ?''', (value, resident_id))
        self.conn.commit()

    def search_residents(self, search_term):
        self.cursor.execute('''SELECT * FROM residents WHERE first_name LIKE ? OR last_name LIKE ?''',
                            ('%' + search_term + '%', '%' + search_term + '%'))
        return self.cursor.fetchall()

    def get_all_residents(self):
        self.cursor.execute('''SELECT * FROM residents''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# ساخت رابط گرافیکی با Tkinter
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت ساکنین ساختمان")
        self.root.geometry("800x600")
        self.manager = BuildingManager()

        # فریم برای نمایش ساکنان
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        # جدول نمایش ساکنان
        self.tree = ttk.Treeview(self.frame, columns=("ID", "نام", "نام خانوادگی", "تعداد نفرات", "طبقه", "واحد", "تلفن ثابت", "تلفن همراه"), show="headings")
        self.tree.heading("ID", text="آیدی")
        self.tree.heading("نام", text="نام")
        self.tree.heading("نام خانوادگی", text="نام خانوادگی")
        self.tree.heading("تعداد نفرات", text="تعداد نفرات")
        self.tree.heading("طبقه", text="طبقه")
        self.tree.heading("واحد", text="واحد")
        self.tree.heading("تلفن ثابت", text="تلفن ثابت")
        self.tree.heading("تلفن همراه", text="تلفن همراه")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # بارگذاری اطلاعات ساکنین
        self.load_residents()

        # منوها
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="عملیات", menu=self.file_menu)
        self.file_menu.add_command(label="افزودن ساکن", command=self.add_resident_form)
        self.file_menu.add_command(label="حذف ساکن", command=self.delete_resident)
        self.file_menu.add_command(label="ویرایش ساکن", command=self.edit_resident)
        self.file_menu.add_command(label="جستجو", command=self.search_residents)
        self.file_menu.add_command(label="خروج", command=self.quit_app)

    def load_residents(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        residents = self.manager.get_all_residents()
        for resident in residents:
            self.tree.insert("", "end", values=resident)

    def add_resident_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("افزودن ساکن")
        form_window.geometry("400x400")

        # ایجاد ورودی‌ها
        tk.Label(form_window, text="آیدی ساکن").grid(row=0, column=0)
        id_entry = tk.Entry(form_window)
        id_entry.grid(row=0, column=1)

        tk.Label(form_window, text="نام").grid(row=1, column=0)
        first_name_entry = tk.Entry(form_window)
        first_name_entry.grid(row=1, column=1)

        tk.Label(form_window, text="نام خانوادگی").grid(row=2, column=0)
        last_name_entry = tk.Entry(form_window)
        last_name_entry.grid(row=2, column=1)

        tk.Label(form_window, text="تعداد نفرات").grid(row=3, column=0)
        num_people_entry = tk.Entry(form_window)
        num_people_entry.grid(row=3, column=1)

        tk.Label(form_window, text="طبقه").grid(row=4, column=0)
        floor_entry = tk.Entry(form_window)
        floor_entry.grid(row=4, column=1)

        tk.Label(form_window, text="واحد").grid(row=5, column=0)
        unit_entry = tk.Entry(form_window)
        unit_entry.grid(row=5, column=1)

        tk.Label(form_window, text="تلفن ثابت").grid(row=6, column=0)
        phone_entry = tk.Entry(form_window)
        phone_entry.grid(row=6, column=1)

        tk.Label(form_window, text="تلفن همراه").grid(row=7, column=0)
        mobile_entry = tk.Entry(form_window)
        mobile_entry.grid(row=7, column=1)

        def save_resident():
            resident = Resident(id_entry.get(), first_name_entry.get(), last_name_entry.get(), num_people_entry.get(),
                                floor_entry.get(), unit_entry.get(), phone_entry.get(), mobile_entry.get())
            self.manager.add_resident(resident)
            self.load_residents()
            form_window.destroy()

        tk.Button(form_window, text="ذخیره", command=save_resident).grid(row=8, column=0, columnspan=2)

    def delete_resident(self):
        selected_item = self.tree.selection()
        if selected_item:
            resident_id = self.tree.item(selected_item, 'values')[0]
            self.manager.delete_resident(resident_id)
            self.load_residents()
        else:
            messagebox.showerror("خطا", "لطفا یک ساکن را انتخاب کنید.")

    def edit_resident(self):
        selected_item = self.tree.selection()
        if selected_item:
            resident_id = self.tree.item(selected_item, 'values')[0]
            form_window = tk.Toplevel(self.root)
            form_window.title("ویرایش ساکن")

            # ایجاد ورودی‌ها برای ویرایش
            # مشابه فرم افزودن ساکن می‌توان ورودی‌ها را ایجاد کرد و اطلاعات ساکن انتخاب شده را لود کرد
            pass

    def search_residents(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("جستجو")

        search_label = tk.Label(search_window, text="نام یا نام خانوادگی را وارد کنید:")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=10)

        def search():
            search_term = search_entry.get()
            results = self.manager.search_residents(search_term)
            self.tree.delete(*self.tree.get_children())
            for result in results:
                self.tree.insert("", "end", values=result)

        search_button = tk.Button(search_window, text="جستجو", command=search)
        search_button.pack(pady=10)

    def quit_app(self):
        self.manager.close()
        self.root.quit()

# اجرای برنامه
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
