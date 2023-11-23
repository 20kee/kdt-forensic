from tkinter import *
from forensictool.recyclebin import *

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

    opt_dropdown = OptionMenu(window, variable, "window xp", "window 7", "window 8", "window 10", "window 11", command=opt_update)
    opt_dropdown.place(x=10, y=10)

    def forensic_main():
        forensic_tool = ForensicTool(window_names[window_opt])
        forensic_tool.SetLink()
        if recycle_bin_var.get():
            forensic_tool.RecycleBinForensic()

    start_button = Button(window, text="포렌식 시작", command= forensic_main)
    start_button.place(x=100, y=10)

    recycle_bin_var = IntVar()
    recycle_bin_check = Checkbutton(window, text='휴지통 포렌식', variable=recycle_bin_var)
    recycle_bin_check.place(x=10, y=40)
    
    
    window.mainloop()


if __name__ == "__main__":
    main()
    