import calendar
import datetime
import ttkcalendar

try:
    import Tkinter
    import tkFont
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont

import ttk

class Runner(Tkinter.Tk):
    def __init__(self):
        import locale
        Tkinter.Tk.__init__(self, className='PyOrgCalendar')
        self.title('Ttk Calendar')
        kwargs = {
            "locale": locale.getdefaultlocale()}
    
        self.cal = ttkcalendar.OrgCaledar(**kwargs)
        self.cal.grid(row=0,column=1)

def main():
    import sys
    root = Runner()

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')

    root.mainloop()

if __name__ == '__main__':
    main()
