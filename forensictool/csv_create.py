import platform
import datetime
import pytz
import csv 
import os
import hashlib

class csv_create:
    def __init__(self):
        pass

    def create(self, folder):
        
        os_ = platform.platform()
        time = datetime.datetime.now(pytz.timezone("Asia/Seoul"))

        with open('./초동조치 보고서.csv', 'w', newline='') as f:
            data = [
                ['운영체제', os_],
                ['타임존', time],
                ['',''],
                ['파일명', 'hash(md5)', 'mac-time']
            ]
            folder_lists = os.listdir(folder)                                       # 포랜식 툴 폴더 목록들
            enc = hashlib.md5()                                                     # 해쉬 생성

            for folder_name in folder_lists:                                        
                data.append(['폴더명', folder_name])                                # 툴 폴더 이름 추가
                file_lists = os.listdir(folder+'\\'+folder_name)                    # 툴 폴더에 있는 파일, 폴더 목록
                for file_name in file_lists:                                        # 폴더에 있는 목록들 반복
                    if os.path.isdir(folder+'\\'+folder_name+'\\'+file_name):       # 폴더안에 폴더가 있을 경우 
                        file_lists_2 = os.listdir(folder+'\\'+folder_name+'\\'+file_name)                    # 툴 폴더에 있는 폴더 파일 목록
                        data.append(['폴더명', folder_name+'\\'+file_name])                                # 툴 폴더안 폴더 이름 추가
                        for file_name_2 in file_lists_2:
                            with open(folder+'\\'+folder_name+'\\'+file_name+'\\'+file_name_2, 'rb') as o:
                                text = o.read()
                                enc.update(text)
                            data.append([file_name_2, enc.hexdigest(), 'test'])
                    else:
                        with open(folder+'\\'+folder_name+'\\'+file_name, 'rb') as o:
                            text = o.read()
                            enc.update(text)
                        data.append([file_name, enc.hexdigest(), 'test'])
                
            write = csv.writer(f)
            write.writerows(data)
                      

def main(folder):
    csv = csv_create()
    csv.create(folder)

if __name__ == "__main__":
    main('test')
            
