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

class OrgCaledar(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self, className='PyOrgCalendar')
        self.title('Ttk Calendar')
        self.__place_widgets()
        # sel_bg = kw.pop('selectbackground', '#ecffc4')
        # sel_fg = kw.pop('selectforeground', '#05640e')

    def __place_widgets(self):
        import locale
        today = datetime.date.today()
        kwargs = {"firstweekday": calendar.MONDAY,
                  "month": today.month,
                  "year": today.year,
                  "locale": locale.getdefaultlocale()}
    
        self.cal = ttkcalendar.Calendar(draw_button=True, **kwargs)

        self.cal.grid(row=0,column=1)

def main():
    import sys
    root = OrgCaledar()

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')

    root.mainloop()

if __name__ == '__main__':
    main()
