import calendar

try:
    import Tkinter
    import tkFont
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont

import ttk

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
        self.__config_calendar()    # adjust calendar columns and setup tags
        # configure a canvas, and proper bindings, for selecting dates
        self.__setup_selection(sel_bg, sel_fg)
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
        # the calendar
        self._calendar_box = ttk.Treeview(show='', selectmode='none', height=7)
        self._calendar_cols = []
        for _ in range(7):
            col = ttk.Treeview(master=self._calendar_box, height=7, selectmode='none', show='')
            col.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH, expand = True)
            self._calendar_cols.append(col)

        # pack the widgets
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        if self._draw_button:
            lbtn.grid(in_=hframe)
            self._header.grid(in_=hframe, column=1, row=0, padx=12)
            rbtn.grid(in_=hframe, column=2, row=0)
        else:
            self._header.grid(in_=hframe, column=1, row=0, padx=22)
        self._calendar_box.pack(in_=self, expand=1, fill='both', side='bottom')

    def __config_calendar(self):
        cols = self._cal.formatweekheader(3).split()
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        self._calendar_items = []
        for i, col in enumerate(self._calendar_cols):
            name = cols[i]
            col['columns'] = name
            col.tag_configure('header', background='grey90')
            col.insert('', 'end', values=[name], tag='header')
            self._calendar_items.append([col.insert('', 'end', values='') for _ in range(6)])
            col.column(name, minwidth=maxwidth, width=maxwidth, anchor='e')

    def __setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()
        self._canvas_cols = []
        for icol, col in enumerate(self._calendar_cols):
            canvas = Tkinter.Canvas(col, background=sel_bg, borderwidth=0, highlightthickness=0)
            col.bind_canvas = canvas
            self._canvas_cols.append(canvas)
            canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
            canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
            col.bind('<Configure>', lambda evt: canvas.place_forget())
            col.bind('<ButtonPress-1>', lambda evt: self._pressed1(icol, evt))

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
        items_cnt = len(self._calendar_items[0])
        for iweek in range(items_cnt):
            week = weeks[iweek] if iweek < len(weeks) else [0] * 7
            fmt_week = [('%02d' % day) if day > 0 else '' for day in week]
            for icol, col in enumerate(self._calendar_cols):
                col.item(self._calendar_items[icol][iweek], values=fmt_week[icol])

    def goto_prev_month(self):
        self._prev_month()

    def goto_next_month(self):
        self._next_month()

    def _show_selection(self, icol, text, bbox, widget):
        """Configure canvas for a new selection."""
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = widget.bind_canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=widget, x=x, y=y)

    # Callbacks

    def _pressed1(self, icol, evt):
        """Clicked somewhere in the calendar."""
        x, y, widget = evt.x, evt.y, evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)

        if not column or not item in self._calendar_items[icol]:
            # clicked in the weekdays row or just outside the columns
            return

        item_values = widget.item(item)['values']
        if not len(item_values): # row is empty for this month
            return

        text = item_values[int(column[1]) - 1]
        if not text: # date is empty
            return

        bbox = widget.bbox(item, column)
        if not bbox: # calendar not visible yet
            return

        # update and then show selection
        text = '%02d' % text
        # self._selection = (text, item, column)
        self._show_selection(icol, text, bbox, widget)

    def _prev_month(self):
        """Updated calendar to show the previous month."""
        for canvas in self._canvas_cols:
            canvas.place_forget()

        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar() # reconstuct calendar
        if self._on_prev_month:
            self._on_prev_month()

    def _next_month(self):
        """Update calendar to show the next month."""
        for canvas in self._canvas_cols:
            canvas.place_forget()

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
