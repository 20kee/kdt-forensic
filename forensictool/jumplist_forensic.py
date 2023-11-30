import shutil
import getpass

class JumpList:
    def __init__(self):
        pass

    def jumplist_copy(self, folder):
        username = getpass.getuser()
        to_file_path = [folder+'/recent_jumplist/', folder+'/frequent_jumplist/']
        from_file_path = ['C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations', 'C:\\Users\\'+username+'\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\CustomDestinations']
        i = 0
        for file in from_file_path:
            shutil.copytree(file, to_file_path[i])
            i +=1

def main(folder):
    jmplist = JumpList()
    jmplist.jumplist_copy(folder)

if __name__ == '__main__':
    main('test')


