import shutil
import getpass

class timeline:
    def __init__(self):
        pass

    def timeline_copy(self, folder):
        username = getpass.getuser()
        to_file_path = folder+'/timeline/'
        from_file_path = 'C:\\Users\\'+username+'\\AppData\\Local\\ConnectedDevicesPlatform\\'
        shutil.copytree(from_file_path, to_file_path)

def main(folder):
    time_line = timeline()
    time_line.timeline_copy(folder)

if __name__ == '__main__':
    main('test')


