import shutil
import getpass

class Timeline:
    def __init__(self):
        pass

    def timeline_copy(self, folder):
        username = getpass.getuser()
        from_file_path = 'C:\\Users\\'+username+'\\AppData\\Local\\ConnectedDevicesPlatform\\'
        shutil.copytree(from_file_path, folder)

def main(folder):
    time_line = Timeline()
    time_line.timeline_copy(folder)

if __name__ == '__main__':
    main('test')


