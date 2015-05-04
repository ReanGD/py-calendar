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
    
        self.cal0 = ttkcalendar.Calendar(draw_button=False, **kwargs)
        self.cal0.goto_prev_month()
        self.cal1 = ttkcalendar.Calendar(draw_button=True,
                                         on_next_month=self.__on_next_month,
                                         on_prev_month=self.__on_prev_month,
                                         **kwargs)
        self.cal2 = ttkcalendar.Calendar(draw_button=False, **kwargs)
        self.cal2.goto_next_month()

        self.cal0.grid(row=0,column=0)
        self.cal1.grid(row=0,column=1)
        self.cal2.grid(row=0,column=2)

    def __on_next_month(self):
        self.cal0.goto_next_month()
        self.cal2.goto_next_month()

    def __on_prev_month(self):
        self.cal0.goto_prev_month()
        self.cal2.goto_prev_month()


def main():
    import sys
    root = OrgCaledar()

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')

    root.mainloop()

if __name__ == '__main__':
    main()
