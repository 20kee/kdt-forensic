import shutil
import os
import hashlib

class EventlogForensicTool:
    def __init__(self):
        pass
    
    def CopyEventLogs(self, dest):
        shutil.copytree("C:\\Windows\\System32\\winevt\\Logs", dest)

    def GetEventLogs(self):
        source_directory = 'C:\Windows\System32\winevt\Logs'
        destination_directory ='./eventLog_copy'
        folder_name = '/EventLogs'

        if os.path.exists(destination_directory+folder_name+'.zip'):
            print('이미 폴더가 존재하므로 삭제합니다.')
            os.remove(destination_directory+folder_name+'.zip')

        shutil.copytree(source_directory, destination_directory+folder_name) 
        file_list = os.listdir(destination_directory+folder_name)
        file_count = len(file_list)
        print(file_count,'개 파일 복사완료')

        shutil.make_archive(destination_directory+folder_name,'zip',destination_directory+folder_name)
        print('압축 완료')

        shutil.rmtree(destination_directory+folder_name)
        print('폴더삭제 완료')

        f = open(destination_directory+folder_name+".zip", 'rb')
        data = f.read()
        f.close()
        print("압축파일 SHA-256: " + hashlib.sha256(data).hexdigest())



    def GetLogFiles(self):
        pass