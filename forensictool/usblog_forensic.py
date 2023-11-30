import shutil
import os

class usb:
    def __init__(self):
        pass

    def usb_copy(self, folder):
        to_file_path = folder+'/usb_log/'
        from_file_path = 'C:\\Windows\\INF\\'
        entires = os.listdir(from_file_path)
        os.mkdir(folder+'/usb_log')
        
        for entire in entires:
            if(not entire.find("setupapi.dev")):
                shutil.copy(from_file_path+entire, to_file_path+entire)
                
        

def main(folder):
    usbcopy = usb()
    usbcopy.usb_copy(folder)

if __name__ == '__main__':
    main('test')


