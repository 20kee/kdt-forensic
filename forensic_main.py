from tkinter import *
from forensictool.forensic_tool import *
import shutil
import os

window_names = ["window xp", "window 7", "window 8", "window 10", "window 11"]

def main():
    window = Tk()
    window.title('윈도우 포렌식 프로그램')
    window.iconbitmap('./1083362.ico')
    xw = int(325)
    yw = int(210)
    window.geometry('{xw}x{yw}-500+500'.format(xw=xw, yw=yw))

    variable = StringVar(window)
    variable.set('window 11')
    window_opt = 4
    def opt_update(selection):
        global window_opt
        window_opt = selection

    first = True
    def forensic_main():
        main_folder_name = main_folder_entry.get()
        try:
            os.mkdir(main_folder_name)
        except:
            shutil.rmtree(main_folder_name)
            os.mkdir(main_folder_name)
        if first:
            forensic_tool = ForensicTool(window_names[-1], drive=drive_entry.get(), main_folder_name=main_folder_name)

        forensic_tool.SetLink()
        
        
        try:
            if recycle_bin_var.get():
                forensic_tool.RecycleBinForensic()
        except Exception as e:
            print(f"Error in RecycleBinForensic: {e}")

        try:
            if ntfs_var.get():
                forensic_tool.NTFSForensic()
        except Exception as e:
            print(f"Error in NTFSForensic: {e}")

        try:
            if extension_search_var.get():
                forensic_tool.SearchFileByExtension(extension_entry.get())
        except Exception as e:
            print(f"Error in SearchFileByExtension: {e}")

        try:
            if registry_var.get():
                forensic_tool.RegistryForensic()
        except Exception as e:
            print(f"Error in RegistryForensic: {e}")

        try:
            if eventlog_var.get():
                forensic_tool.EventlogForensic()
        except Exception as e:
            print(f"Error in EventlogForensic: {e}")
            
        if browser_var.get():
            try:
                forensic_tool.ChromeForensic()
            except:
                pass
            
            try:
                forensic_tool.EdgeForensic()
            except:
                pass

            try:
                forensic_tool.FirefoxForensic()
            except:
                pass

        try:
            if timeline_var.get():
                forensic_tool.TimeLineForensic()
        except Exception as e:
            print(f"Error in TimeLineForensic: {e}")

        try:
            if prefetch_var.get():
                forensic_tool.PrefetchForensic()
        except Exception as e:
            print(f"Error in PrefetchForensic: {e}")

        try:
            if srum_var.get():
                forensic_tool.SrumForensic()
        except Exception as e:
            print(f"Error in SrumForensic: {e}")

        try:
            if jumplist_var.get():
                forensic_tool.JumplistForensic()
        except Exception as e:
            print(f"Error in JumplistForensic: {e}")

        try:
            if usblog_var.get():
                forensic_tool.UsblogForensic()
        except Exception as e:
            print(f"Error in UsblogForensic: {e}")

        try:
            if windows_noti_var.get():
                forensic_tool.WindowsNotificationForensic()
        except Exception as e:
            print(f"Error in WindowsNotificationForensic: {e}")\
            
        forensic_tool.CsvCreate()
#브라우저 분석 함수  
    def browser_analysis():
        browser_tool = browserTool()
        file_path = filedialog.askopenfilename()
        h_or_c = os.path.basename(file_path)
        if "Cookies" in h_or_c or 'cookies'in h_or_c:
            print(file_path) 
            browser_tool.cookie_analysis(file_path)
        elif "places" in h_or_c or 'History' in h_or_c:
            print(file_path)
            browser_tool.history_analysis(file_path)

    main_folder_label = Label(window, text='폴더')
    main_folder_label.place(x=10, y=14)
    main_folder_entry = Entry(window, width=9)
    main_folder_entry.insert(0, 'Forensic Result')
    main_folder_entry.place(x= 57, y=14)

    drive_label = Label(window, text='드라이브')
    drive_label.place(x=128, y=13)
    drive_entry = Entry(window, width=2)
    drive_entry.insert(0, 'C')
    drive_entry.place(x=185, y=13)

    extension_label = Label(window, text='확장자')
    extension_label.place(x=215, y=13)
    extension_entry = Entry(window, width=3)
    extension_entry.insert(0, 'txt')
    extension_entry.place(x=262, y=13)
    

    recycle_bin_var = IntVar()
    recycle_bin_check = Checkbutton(window, text='Recycle Bin', variable=recycle_bin_var)
    recycle_bin_check.place(x=10, y=45)

    ntfs_var = IntVar()
    ntfs_check = Checkbutton(window, text='NTFS', variable=ntfs_var)
    ntfs_check.place(x=109, y=45)

    extension_search_var = IntVar()
    extension_search_check = Checkbutton(window, text='File Extension', variable=extension_search_var)
    extension_search_check.place(x=175, y=45)

    #EventLog
    eventlog_var = IntVar()
    eventlog_check = Checkbutton(window, text='EventLog', variable=eventlog_var)
    eventlog_check.place(x=10, y=76)

    registry_var = IntVar()
    registry_check = Checkbutton(window, text='Registry', variable=registry_var)
    registry_check.place(x=93, y=76)

    browser_var = IntVar()
    browser_check = Checkbutton(window, text='Browser History', variable=browser_var)
    browser_check.place(x=173, y=76)

    timeline_var = IntVar()
    timeline_check = Checkbutton(window, text='TimeLine', variable=timeline_var)
    timeline_check.place(x=10, y=106)

    prefetch_var = IntVar()
    prefetch_check = Checkbutton(window, text='Prefetch', variable=prefetch_var)
    prefetch_check.place(x=90, y=106)

    srum_var = IntVar()
    srum_check = Checkbutton(window, text='Srum', variable=srum_var)
    srum_check.place(x=170, y=106)

    jumplist_var = IntVar()
    jumplist_check = Checkbutton(window, text='Jumplist', variable=jumplist_var)
    jumplist_check.place(x=228, y=106)

    usblog_var = IntVar()
    usblog_check = Checkbutton(window, text='Usblog', variable=usblog_var)
    usblog_check.place(x=10, y=136)

    windows_noti_var = IntVar()
    windows_noti_check = Checkbutton(window, text='Windows Notification', variable=windows_noti_var)
    windows_noti_check.place(x=80, y=136)


    start_button = Button(window, text="포렌식 시작", command= forensic_main)
    start_button.place(x=10, y=166)
    browser_button = Button(window, text="브라우저 히스토리, 쿠키 분석", command= browser_analysis)
    browser_button.place(x=110, y=166)

    

    window.mainloop()


if __name__ == "__main__":
    main()
    