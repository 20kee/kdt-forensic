import os
from datetime import datetime
from forensictool.csv_create import *
from forensictool.ntfs_forensic import *
from forensictool.registry_forensic import *
from forensictool.eventlog_forensic import *
from forensictool.file_search import *
from forensictool.browser_history import *
from forensictool.jumplist_forensic import *
from forensictool.prefetch_forensic import *
from forensictool.srum_forensic import *
from forensictool.timeline_forensic import *
from forensictool.usblog_forensic import *
from forensictool.Windows_Notification_Center_forensic import *
from tkinter import filedialog
import hashlib

class ForensicTool:
    def __init__(self, window_ver, drive, main_folder_name):
        self._main_folder_name = main_folder_name
        self._drive = drive
        self._window_ver = window_ver
        self._recycle_bin_link = None
        self._csv_creater = CsvCreater()
        self._NTFS_tool = Extract_File(drive + ':')
        self._registry_tool = RegistryForensicTool()
        self._eventlog_tool = EventlogForensicTool()
        self._extension_search_tool = FileExtensionSearchTool(drive)
        self._browser_tool = BrowserForensicTool()
        self._jumplist_tool = JumpList()
        self._prefetch_tool = Prefetch()
        self._srum_tool = Srum()
        self._usblog_tool = Usblog()
        self._timeline_tool = Timeline()
        self._window_notification_tool = WNC()
    def SetLink(self):
        self._recycle_bin_link = 'C:\\$Recycle.Bin'
    def CsvCreate(self):
        self._csv_creater.create(self._main_folder_name)
    
    def RecycleBinForensic(self): # 휴지통 포렌식
        folder_name = "recycle_bin"
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        if True:
            dirs = os.listdir(self._recycle_bin_link) # 휴지통 안의 폴더들
            for dir in dirs:
                try:
                    files = os.listdir(self._recycle_bin_link + '\\' + dir) # 내 진짜 휴지통 안의 삭제된 파일을
                    for file in files:
                        f = open(self._recycle_bin_link + '\\' + dir + '\\' + file, 'rb')
                        data = f.read()
                        f2 = open(self._main_folder_name + "\\recycle_bin\\{}".format(file), 'wb')
                        f2.write(data)
                        f2.close()
                        f.close()

                except Exception as e:
                    print(e)
                    pass
        
        print('Recycle Bin Forensic Done.')

    def SearchFileByExtension(self, extension): # 특정 확장자 파일들 검색
        root = filedialog.askdirectory(initialdir="/",\
					title = "폴더를 선택 해 주세요")
        folder_name = "specific_extension_files"
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        self._extension_search_tool.Search(root, extension, self._main_folder_name + '\\' + folder_name)

    def NTFSForensic(self): # NTFS 포렌식
        folder_name = 'ntfs'
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        self._NTFS_tool.Extract('/$MFT',self._main_folder_name+'/ntfs/$MFT')
        self._NTFS_tool.Extract('/$LogFile',self._main_folder_name+'/ntfs/$LogFile')
        self._NTFS_tool.Extract_UsnJrnl(self._main_folder_name)
        files = ['$MFT', '$LogFile', '$UsnJrnl']
        enc = hashlib.md5()
        for file in files:
            with open(self._main_folder_name+'/ntfs/'+file, 'rb') as f:
                text = f.read()
                enc.update(text)
                print(enc.hexdigest())

    def EventlogForensic(self): # 이벤트로그 포렌식
        folder_name = 'event_log'
        self._eventlog_tool.CoptEventLogs(self._main_folder_name + '\\' + folder_name)

    def RegistryForensic(self): # 레지스트리 포렌식
        folder_name = 'registry'
        self._registry_tool.registry_copy("SOFTWARE\\Microsoft", self._main_folder_name + '\\' + folder_name)
        shutil.make_archive(self._main_folder_name +'\\registry', 'zip', self._main_folder_name + '\\' + folder_name)
        shutil.rmtree(self._main_folder_name + '\\' + folder_name+'\\')
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        shutil.move(self._main_folder_name +'\\registry.zip', self._main_folder_name + '\\' + folder_name+'\\')
    
    def ChromeForensic(self):
        folder_name = 'chrome_history'
        os.mkdir(self._main_folder_name +'\\' + folder_name)
        self._browser_tool.copy_chrome_data(self._main_folder_name +'\\' + folder_name)
    
    def EdgeForensic(self):
        folder_name = 'edge_history'
        os.mkdir(self._main_folder_name +'\\' + folder_name)
        self._browser_tool.copy_edge_data(self._main_folder_name +'\\' + folder_name)
    

    def FirefoxForensic(self):
        folder_name = 'firefox_history'
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        self._browser_tool.copy_firefox_data(self._main_folder_name + '\\' + folder_name)
    

    def TimeLineForensic(self):
        folder_name = 'timeline'
        self._timeline_tool.timeline_copy(self._main_folder_name + '\\' + folder_name)

    def PrefetchForensic(self):
        folder_name = 'prefetch'
        self._prefetch_tool.prefetch_copy(self._main_folder_name + '\\' + folder_name)

    def SrumForensic(self):
        folder_name = 'srum'
        self._srum_tool.srum_copy(self._main_folder_name + '\\' + folder_name)
    def JumplistForensic(self):
        folder_name = 'jumplist'
        self._jumplist_tool.jumplist_copy(self._main_folder_name + '\\' + folder_name)

    def UsblogForensic(self):
        folder_name = 'usblog'
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        self._usblog_tool.usb_copy(self._main_folder_name + '\\' + folder_name)

    def WindowsNotificationForensic(self):
        folder_name = 'windows_notification'
        os.mkdir(self._main_folder_name + '\\' + folder_name)
        self._window_notification_tool.WNC_copy(self._main_folder_name + '\\' + folder_name)
#브라우저 분석 클래스
class browserTool:
    def cookie_analysis(self, path):
        print(path)
        app = CookieAnalyzer(path)
        app.mainloop()

    def history_analysis(self, path):
        print(path)
        app = HistoryAnalyzer(path)
        app.mainloop()





