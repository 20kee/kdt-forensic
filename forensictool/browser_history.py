#창민아 폴더명 클래스 호출할때 넣고 copy_browser_data(self) 이함수만 호출하면 작동됨

import os
import shutil
import hashlib
import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3

class BrowserForensicTool:
    def __init__(self):
        self.base_path = None
        self.hash_log_file = None

    def create_directory_if_not_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def calculate_file_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def copy_and_log_file_hash(self, src, dest):
        shutil.copy2(src, dest)
        # file_hash = self.calculate_file_hash(dest)
        # with open(self.hash_log_file, 'w') as log:
        #     log.write(f"{dest}: {file_hash}\n")

    def get_firefox_profiles(self):
        firefox_base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        return [os.path.join(firefox_base_path, d) for d in os.listdir(firefox_base_path) if os.path.isdir(os.path.join(firefox_base_path, d))]

    def get_file_path(self, browser_name, profile_path, file_name=None):
        if browser_name == 'firefox':
            return os.path.join(profile_path, file_name) if file_name else None
        elif browser_name == 'chrome':
            suffix = 'Network' if file_name == 'Cookies' else ''
            return os.path.join(profile_path, 'Google', 'Chrome', 'User Data', 'Default', suffix, file_name) if file_name else None
        elif browser_name == 'edge':
            suffix = 'Network' if file_name == 'Cookies' else ''
            return os.path.join(profile_path, 'Microsoft', 'Edge', 'User Data', 'Default', suffix, file_name) if file_name else None

#chrome        
    def copy_chrome_data(self, dest):
        self.base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local')
        self.hash_log_file = os.path.join(dest, 'hash.txt')
        browser_name = 'chrome'
        for file_name in ['History', 'Cookies']:
            file_path = self.get_file_path(browser_name, self.base_path, file_name)
            if os.path.exists(file_path):
                try:
                    self.copy_and_log_file_hash(file_path, dest)
                except:
                    pass
    
#edge    
    def copy_edge_data(self, dest):
        self.base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local')
        self.hash_log_file = os.path.join(dest, 'hash.txt')
        browser_name = 'edge'
        file_path = self.get_file_path(browser_name, self.base_path)
        for file_name in ['History', 'Cookies']:
            file_path = self.get_file_path(browser_name, self.base_path, file_name)
            if os.path.exists(file_path):
                try:
                    self.copy_and_log_file_hash(file_path, dest)
                except Exception as e:
                    print(e)

#파폭
    def copy_firefox_data(self, dest):
        self.create_directory_if_not_exists(dest)
        self.base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        self.hash_log_file = os.path.join(dest, 'hash.txt')

        for profile_path in self.get_firefox_profiles():
            for file_name in ['places.sqlite', 'cookies.sqlite']:
                file_path = self.get_file_path('firefox', profile_path, file_name)
                if os.path.exists(file_path):
                    profile_name = os.path.basename(profile_path)
                    destination_file = f'firefox_{profile_name}_{file_name}'
                    self.copy_and_log_file_hash(file_path, os.path.join(dest, destination_file))
#쿠키분석 클래스
class CookieAnalyzer(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.title("Cookie Analyzer")
        self.geometry("800x600") 
        self.create_widgets()

    def create_widgets(self):
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_label = ttk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_options = ttk.Combobox(self.search_frame, values=["name", "value", "host_key", "path", "expires_utc", "creation_utc", "last_update_utc", "is_secure", "is_httponly","ALL"])
        self.search_options.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_options.current(0) 

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.filter_cookies)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self)
        columns = ("name", "value", "host_key", "path", "expires_utc", "creation_utc", "last_update_utc", "is_secure", "is_httponly")
        self.tree["columns"] = columns

        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col.replace("_", " ").title(), anchor=tk.W)  

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.load_cookies()

    def load_cookies(self, query=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if query:
                cursor.execute(query)
            else:
                cursor.execute('SELECT name, value, host_key, path, expires_utc, creation_utc, last_update_utc, is_secure, is_httponly FROM cookies')

            self.tree.delete(*self.tree.get_children())
            for row in cursor:
                self.tree.insert("", tk.END, values=row)

            conn.close()
        except Exception as e:
            print(f"Error: {e}")

    def filter_cookies(self):
        search_term = self.search_entry.get()
        selected_option = self.search_options.get()
        query = f'''
        SELECT name, value, host_key, path, expires_utc, creation_utc, last_update_utc, is_secure, is_httponly 
        FROM cookies 
        WHERE {selected_option} LIKE '%{search_term}%'
        '''
        self.load_cookies(query)

#히스토리 분석 클래스
class HistoryAnalyzer(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.title("History Analyzer")
        self.geometry("800x600") 
        self.create_widgets()

    def create_widgets(self):
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_label = ttk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_options = ttk.Combobox(self.search_frame, values=["url", "visit_time", "title", "ALL"])
        self.search_options.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_options.current(0)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.filter_history)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self)
        columns = ("url", "visit_time", "title")
        self.tree["columns"] = columns

        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col.replace("_", " ").title(), anchor=tk.W)  

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.load_history()

    def load_history(self, query=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if query:
                cursor.execute(query)
            else:
                cursor.execute("SELECT url, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_time, title FROM urls")

            self.tree.delete(*self.tree.get_children())
            for row in cursor:
                self.tree.insert("", tk.END, values=row)

            conn.close()
        except Exception as e:
            print(f"Error: {e}")

    def filter_history(self):
        search_term = self.search_entry.get()
        selected_option = self.search_options.get()

        if selected_option == "ALL":
            query = f'''
            SELECT url, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_time, title
            FROM urls
            WHERE url LIKE '%{search_term}%' OR title LIKE '%{search_term}%'
            '''
        else:
            query = f'''
            SELECT url, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_time, title
            FROM urls
            WHERE {selected_option} LIKE '%{search_term}%'
            '''
        self.load_history(query)
