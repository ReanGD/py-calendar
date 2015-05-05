import calendar

try:
    import Tkinter
    import tkFont
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont

import ttk
    
class CalendarColumn(ttk.Treeview):
    items_cnt = 6
    def __init__(self, master):
        ttk.Treeview.__init__(self, master, height=7, selectmode='none', show='')
        self.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True)

    def config(self, name, header_bg, width):
        self['columns'] = name
        self.tag_configure('header', background=header_bg)
        self.insert('', 'end', values=[name], tag='header')
        self.items = [self.insert('', 'end', values='') for _ in range(CalendarColumn.items_cnt)]
        self.column(name, minwidth=width, width=width, anchor='e')

    def setup_selection(self, sel_bg, sel_fg, btn1_press_callback):
        self.canvas = canvas = Tkinter.Canvas(self, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
        canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
        self.bind('<Configure>', lambda evt: canvas.place_forget())
        self.bind('<ButtonPress-1>', btn1_press_callback)

    def _show_selection(self, text, bbox, font):
        x, y, width, height = bbox

        textw = font.measure(text)

        canvas = self.canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self, x=x, y=y)

    def on_pressed(self, evt, font):
        x, y = evt.x, evt.y
        item = self.identify_row(y)
        column = self.identify_column(x)

        if not column or not item in self.items:
            # clicked in the weekdays row or just outside the columns
            return

        item_values = self.item(item)['values']
        if not len(item_values): # row is empty for this month
            return

        text = item_values[int(column[1]) - 1]
        if not text: # date is empty
            return

        bbox = self.bbox(item, column)
        if not bbox: # calendar not visible yet
            return

        # update and then show selection
        text = '%02d' % text
        # self._selection = (text, item, column)
        self._show_selection(text, bbox, font)

class CalendarMonth(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, show='', selectmode='none', height=7)
        self._cols = [CalendarColumn(self) for _ in range(7)]
        self.pack(in_=master, expand=1, fill='both', side='bottom')

    def config(self, cal, font, header_bg, sel_bg, sel_fg, btn1_press_callback):
        cols = cal.formatweekheader(3).split()
        maxwidth = max(font.measure(col) for col in cols)
        for i, col in enumerate(self._cols):
            col.config(cols[i], header_bg, maxwidth)
            col.setup_selection(sel_bg, sel_fg, btn1_press_callback)

    def build(self, weeks):
        for iweek in range(CalendarColumn.items_cnt):
            week = weeks[iweek] if iweek < len(weeks) else [0] * 7
            fmt_week = [('%02d' % day) if day > 0 else '' for day in week]
            for icol, col in enumerate(self._cols):
                col.item(col.items[iweek], values=fmt_week[icol])

    def remove_selection(self):
        for col in self._cols:
            col.canvas.place_forget()

def get_calendar(locale, fwday):
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)

class Calendar(ttk.Frame):
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, **kw):
        """
        WIDGET-SPECIFIC OPTIONS

            locale, firstweekday, year, month, selectbackground,
            selectforeground
        """
        fwday = kw.pop('firstweekday', calendar.MONDAY)
        year = kw.pop('year', self.datetime.now().year)
        month = kw.pop('month', self.datetime.now().month)
        locale = kw.pop('locale', None)
        sel_bg = kw.pop('selectbackground', '#ecffc4')
        sel_fg = kw.pop('selectforeground', '#05640e')
        self._draw_button = kw.pop('draw_button', True)
        self._on_next_month = kw.pop('on_next_month', None)
        self._on_prev_month = kw.pop('on_prev_month', None)

        self._date = self.datetime(year, month, 1)
        self._selection = None

        ttk.Frame.__init__(self, master, **kw)

        self._cal = get_calendar(locale, fwday)

        self.__setup_styles()       # creates custom styles
        self.__place_widgets()      # pack/grid used widgets
        self._font = tkFont.Font()
        self._calendar_box.config(self._cal, self._font, 'grey90', sel_bg, sel_fg, self._pressed)
        self._build_calendar()

        # set the minimal size for the widget
        self._calendar_box.bind('<Map>', self.__minsize)

    def __setup_styles(self):
        # custom ttk styles
        style = ttk.Style(self.master)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        if self._draw_button:
            style.layout('L.TButton', arrow_layout('left'))
            style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # header frame and its widgets
        hframe = ttk.Frame(self)
        if self._draw_button:
            lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
            rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        self._header = ttk.Label(hframe, width=15, anchor='center')
        # pack the widgets
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        if self._draw_button:
            lbtn.grid(in_=hframe)
            self._header.grid(in_=hframe, column=1, row=0, padx=12)
            rbtn.grid(in_=hframe, column=2, row=0)
        else:
            self._header.grid(in_=hframe, column=1, row=0, padx=22)
        self._calendar_box = CalendarMonth(self)

    def __minsize(self, evt):
        width, height = self._calendar_box.master.geometry().split('x')
        height = height[:height.index('+')]
        self._calendar_box.master.minsize(width, height)

    def _build_calendar(self):
        year, month = self._date.year, self._date.month

        # update header text (Month, YEAR)
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()

        # update calendar shown dates
        weeks = self._cal.monthdayscalendar(year, month)
        self._calendar_box.build(weeks)

    # Callbacks

    def _pressed(self, evt):
        self._calendar_box.remove_selection()
        evt.widget.on_pressed(evt, self._font)

    def _prev_month(self):
        """Updated calendar to show the previous month."""
        self._calendar_box.remove_selection()
        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar() # reconstuct calendar
        if self._on_prev_month:
            self._on_prev_month()

    def _next_month(self):
        """Update calendar to show the next month."""
        self._calendar_box.remove_selection()
        year, month = self._date.year, self._date.month
        self._date = self._date + self.timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar() # reconstruct calendar
        if self._on_next_month:
            self._on_next_month()

    # Properties

    @property
    def selection(self):
        """Return a datetime representing the current selected date."""
        if not self._selection:
            return None

        year, month = self._date.year, self._date.month
        return self.datetime(year, month, int(self._selection[0]))
