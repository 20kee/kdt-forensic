import shutil
import os 

class Amcache:
    def __init__(self):
        pass

    def Amcache_copy(self, folder):
        to_file_path = folder+'/Amcache/'
        from_file_path = 'C:\\Windows\\AppCompat\\Programs\\'
        #shutil.copytree(from_file_path, to_file_path)
        entires = os.listdir(from_file_path)
        #os.mkdir(folder+'/usb_log')
        
        for entire in entires:
            with open(from_file_path+entire, 'rb') as f:
                print(f.read())                
            

def main(folder):
    Amcache_ = Amcache()
    Amcache_.Amcache_copy(folder)

if __name__ == '__main__':
    main('test')


