import shutil
import os

class Usblog:
    def __init__(self):
        pass

    def usb_copy(self, folder):
        from_file_path = 'C:\\Windows\\INF\\'
        entires = os.listdir(from_file_path)
        
        for entire in entires:
            if(not entire.find("setupapi.dev")):
                shutil.copy(from_file_path+entire, folder+ '\\' + entire)
                
        

def main(folder):
    usbcopy = Usblog()
    usbcopy.usb_copy(folder)

if __name__ == '__main__':
    main('test')


