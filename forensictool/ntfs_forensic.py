import pytsk3, sys
import hashlib

class Extract_File:
    def __init__(self, drive):
        self.volume='\\\\.\\'+ drive                 # 장치이름 지정
        self.img=pytsk3.Img_Info(self.volume)   # 장치를 입력
        self.fs=pytsk3.FS_Info(self.img)        # 파일시스템 열기
        

    def Extract(self,filename,output_name):     # 파일을 읽어와서 저장 
        f=self.fs.open(filename)
        offset=0
        size=f.info.meta.size
        buffer = f.read_random(offset, size)
        with open(output_name,'wb') as o:
            o.write(buffer)

    def Extract_UsnJrnl(self):                  # $j 파일 저장
        f=self.fs.open('/$Extend/$UsnJrnl')
        found=True
        
        for attr in f:
            if attr.info.name == b'$J':
                found=True
                break
        if not found:
            sys.exit(0)

        with open('$UsnJrnl','wb') as o:
            offset=0
            size=attr.info.size
            while offset < size:
                available_to_read=min(1024*1024,size-offset)
                buf=f.read_random(offset,available_to_read,attr.info.type,attr.info.id)
                if not buf:
                    break
                o.write(buf)
                offset+=len(buf)

def main():
    Ext=Extract_File('C:')
    Ext.Extract('/$MFT','$MFT')
    Ext.Extract('/$LogFile','$LogFile')
    Ext.Extract_UsnJrnl()
    files = ['$MFT', '$LogFile', '$UsnJrnl']
    enc = hashlib.md5()
    for file in files:
        with open(file, 'rb') as f:
            text = f.read()
            enc.update(text)
            print(enc.hexdigest())

if __name__ == '__main__':
    main()