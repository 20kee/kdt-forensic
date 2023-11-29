#창민아 폴더명 클래스 호출할때 넣고 copy_browser_data(self) 이함수만 호출하면 작동됨

import os
import shutil
import hashlib

class BrowserHistory:
    def __init__(self, destination_folder):
        self.destination_folder = destination_folder
        self.create_directory_if_not_exists(destination_folder)
        self.base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local')
        self.hash_log_file = os.path.join(destination_folder, 'hash.txt')

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
        file_hash = self.calculate_file_hash(dest)
        with open(self.hash_log_file, 'a') as log:
            log.write(f"{dest}: {file_hash}\n")

    def get_firefox_profiles(self):
        firefox_base_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        return [os.path.join(firefox_base_path, d) for d in os.listdir(firefox_base_path) if os.path.isdir(os.path.join(firefox_base_path, d))]

    def get_file_path(self, browser_name, profile_path, file_name):
        if browser_name == 'firefox':
            return os.path.join(profile_path, file_name)
        else:
            suffix = 'Network' if file_name == 'Cookies' else ''
            return os.path.join(profile_path, browser_name.capitalize(), 'User Data', 'Default', suffix, file_name)

    def copy_browser_data(self):
        for browser_name in ['chrome', 'edge']:
            for file_name in ['History', 'Cookies']:
                file_path = self.get_file_path(browser_name, self.base_path, file_name)
                if os.path.exists(file_path):
                    destination = os.path.join(self.destination_folder, f'{browser_name}_{file_name}')
                    self.copy_and_log_file_hash(file_path, destination)

        for profile_path in self.get_firefox_profiles():
            for file_name in ['places.sqlite', 'cookies.sqlite']:
                file_path = self.get_file_path('firefox', profile_path, file_name)
                if os.path.exists(file_path):
                    profile_name = os.path.basename(profile_path)
                    destination = os.path.join(self.destination_folder, f'firefox_{profile_name}_{file_name}')
                    self.copy_and_log_file_hash(file_path, destination)
