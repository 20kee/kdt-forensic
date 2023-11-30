from tkinter import *
from forensictool.forensic_tool import *
import shutil

window_names = ["window xp", "window 7", "window 8", "window 10", "window 11"]

def main():
    window = Tk()
    window.title('윈도우 포렌식 프로그램')
    xw = int(400)
    yw = int(400)
    window.geometry('{xw}x{yw}-500+500'.format(xw=xw, yw=yw))

    variable = StringVar(window)
    variable.set('window 11')
    window_opt = 4
    def opt_update(selection):
        global window_opt
        window_opt = selection

    opt_dropdown = OptionMenu(window, variable, *window_names, command=opt_update)
    opt_dropdown.place(x=10, y=10)

    first = True
    def forensic_main():
        main_folder_name = main_folder_entry.get()
        try:
            os.mkdir(main_folder_name)
        except:
            shutil.rmtree(main_folder_name)
            os.mkdir(main_folder_name)
        if first:
            forensic_tool = ForensicTool(window_names[window_opt], drive=drive_entry.get(), main_folder_name=main_folder_name)

        forensic_tool.SetLink()
        if recycle_bin_var.get():
            forensic_tool.RecycleBinForensic()
        if ntfs_var.get():
            forensic_tool.NTFSForensic()
        if extension_search_var.get():
            forensic_tool.SearchFileByExtension(extension_entry.get())
        if registry_var.get():
            forensic_tool.RegistryForensic(registry_opt_entry.get())
        if eventlog_var.get():
            forensic_tool.EventlogForensic()
        if browser_var.get():
            forensic_tool.ChromeForensic()
            forensic_tool.EdgeForensic()
            forensic_tool.FirefoxForensic()
    

    drive_label = Label(window, text='드라이브')
    drive_label.place(x=120, y=13)
    drive_entry = Entry(window, width=2)
    drive_entry.insert(0, 'C')
    drive_entry.place(x=177, y=13)

    extension_label = Label(window, text='확장자')
    extension_label.place(x=210, y=13)
    extension_entry = Entry(window, width=3)
    extension_entry.insert(0, 'txt')
    extension_entry.place(x=257, y=13)
    

    recycle_bin_var = IntVar()
    recycle_bin_check = Checkbutton(window, text='휴지통 포렌식', variable=recycle_bin_var)
    recycle_bin_check.place(x=10, y=45)

    ntfs_var = IntVar()
    ntfs_check = Checkbutton(window, text='NTFS', variable=ntfs_var)
    ntfs_check.place(x=128, y=45)

    extension_search_var = IntVar()
    extension_search_check = Checkbutton(window, text='File Extension', variable=extension_search_var)
    extension_search_check.place(x=192, y=45)

    #EventLog
    eventlog_var = IntVar()
    eventlog_check = Checkbutton(window, text='EventLog', variable=eventlog_var)
    eventlog_check.place(x=10, y=76)

    registry_var = IntVar()
    registry_check = Checkbutton(window, text='Registry', variable=registry_var)
    registry_check.place(x=102, y=76)
    
    registry_opt_entry = Entry(window, width=3)
    registry_opt_entry.insert(0, 'all')
    registry_opt_entry.place(x=180, y=80)

    browser_var = IntVar()
    browser_check = Checkbutton(window, text='Browser History', variable=browser_var)
    browser_check.place(x=10, y=106)

    start_button = Button(window, text="포렌식 시작", command= forensic_main)
    start_button.place(x=10, y=312)

    main_folder_label = Label(window, text='폴더명')
    main_folder_label.place(x=90, y=312)
    main_folder_entry = Entry(window, width=15)
    main_folder_entry.insert(0, 'Forensic Result')
    main_folder_entry.place(x= 137, y=312)

    window.mainloop()


if __name__ == "__main__":
    main()
    