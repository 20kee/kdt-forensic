import shutil
import getpass
import os

class WNC:
    def __init__(self):
        pass

    def WNC_copy(self, folder):
        username = getpass.getuser()
        from_file_path = 'C:\\Users\\'+username+'\\AppData\\Local\\Microsoft\\Windows\\Notifications\\wpndatabase.db'
        shutil.copy(from_file_path, folder + '\\' + 'wpndatabase.db')

def main(folder):
    time_line = WNC()
    time_line.WNC_copy(folder)

if __name__ == '__main__':
    main('test')


#윈 10만 가능