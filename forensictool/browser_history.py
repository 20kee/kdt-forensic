#창민아 폴더명 클래스 호출할때 넣고 copy_browser_data(self) 이함수만 호출하면 작동됨

import os
import shutil
import hashlib

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

# 클래스 인스턴스 생성
forensic_tool = BrowserForensicTool()

# 목적지 폴더 지정
destination_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'test','edge')

# 메서드 호출
forensic_tool.copy_chrome_data(destination_folder)