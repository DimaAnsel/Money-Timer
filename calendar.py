from tkinter import *
from time import localtime

################
# Calendar: Basic Tkinter calendar GUI.
#   Class members:
#     SUPPORTED_LANG  LABEL_MAP   MONTH_MAP   DAY_MAP
#   Subclasses:
#     Month
#   Members:
#     <member>
#   Methods:
#     <method>
class Calendar(Frame):

  # Supported languages for this widget. Currently supports:
  #   en : English
  #   jp : Japanese (日本語)
  SUPPORTED_LANG = ("en", "jp")

  # Text to use in GUI elements, separated by language and stored in
  # dictionary format. Access with <name>_MAP[lang][element].
  LABEL_MAP = {"en":{"yearButton":  "Year",
                     "monthButton": "Month",
                     "monthLabel":  "{1} {0}"},
               "jp":{"yearButton":  "年",
                     "monthButton": "月",
                     "monthLabel": "{0}年 {1}"}}
  MONTH_MAP = {"en":["Jan", "Feb", "Mar", "Apr",
                     "May", "June","July","Aug",
                     "Sep", "Oct", "Nov", "Dec"],
               "jp":["一月", "二月", "三月", "四月",
                     "五月", "六月", "七月", "八月",
                     "九月", "十月", "十一月", "十二月"]}
  DAY_MAP = {"en":["Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat"],
             "jp":["日曜", "月曜", "火曜", "水曜", "木曜", "金曜", "土曜"]}

  DAY_BG = "#FFFFFF"
  TODAY_BG = "#DDDDDD"

  ################
  # Month: A single month in Calendar's yearView.
  #   Members:
  #     <member>
  #   Methods:
  #     <method>
  class Month(Frame):

    def __init__(self, master, monNum = 0, lang = "en"):
      super().__init__(master._yearView)
      self._parent = master
      self._monNum = monNum
      self._create_widgets(lang)

    def _create_widgets(self, lang):
      self._monButton = Button(self, command = self._on_monButton_click, text = Calendar.MONTH_MAP[lang][self._monNum])
      self._monButton.grid(row = 0, column = 0)

    def _on_monButton_click(self):
      self._parent._update_month_view(self._monNum)
      self._parent._show_month_view()
  # Month
  ################

  def __init__(self, master = None, lang = "en", year = None, month = None):
    super().__init__(master)
    self._lang = lang
    now = localtime()
    if year == None:
      self._year = now.tm_year
    else:
      self._year = year
    if month == None:
      self._month = now.tm_mon - 1
    else:
      self._month = month
    self._currDay = None

    self._create_widgets()
    self._update_month_view(self._month)
    self._show_month_view()

  def _create_widgets(self):
    self._yearButton = Button(self, text = Calendar.LABEL_MAP[self._lang]["yearButton"], command = self._show_year_view)
    self._monthButton = Button(self, text = Calendar.LABEL_MAP[self._lang]["monthButton"], command = self._show_month_view)
    self._yearButton.grid(row = 0, column = 0, sticky = N+S+W+E)
    self._monthButton.grid(row = 0, column = 1, sticky = N+S+W+E)

    self._yearView = Frame(self)
    self._months = []
    for i in range(12):
      newMonth = Calendar.Month(self, monNum = i, lang = self._lang)
      newMonth.grid(column = i % 4, row = i // 4)
      self._months.append(newMonth)
    self._yearView.grid(row = 1, column = 0, columnspan = 2, sticky = N+S+W+E)

    self._monthView = Frame(self)
    self._monthLeftButton = Button(self._monthView, text = "<", command = self._on_monthLeftButton_click)
    self._monthLeftButton.grid(row = 0, column = 0, sticky = N+S+W+E)
    self._monthRightButton = Button(self._monthView, text = ">", command = self._on_monthRightButton_click)
    self._monthRightButton.grid(row = 0, column = 6, sticky = N+S+W+E)
    self._monthView.monthLabel = Label(self._monthView, text = Calendar.MONTH_MAP[self._lang][0])
    self._monthView.monthLabel.grid(row = 0, column = 1, columnspan = 5, sticky = N+S+W+E)
    self._monthView.weekdayLabels = []
    for i in range(7):
      newLabel = Label(self._monthView, text = Calendar.DAY_MAP[self._lang][i])
      newLabel.grid(row = 1, column = i, sticky = N+S+W+E)
      self._monthView.weekdayLabels.append(newLabel)
    self._monthView.dayLabels = []
    for i in range(7 * 6):
      newLabel = Label(self._monthView, text = str(i), bg = Calendar.DAY_BG)
      newLabel.grid(row = 2 + i //7, column = i % 7, sticky = N+S+W+E)
      self._monthView.dayLabels.append(newLabel)

  def _show_year_view(self):
    self._monthView.grid_forget()
    self._update_year_view()
    self._yearView.grid(row = 1, column = 0, columnspan = 2, sticky = N+S+W+E)

  def _show_month_view(self):
    self._yearView.grid_forget()
    self._monthView.grid(row = 1, column = 0, columnspan = 2, sticky = N+S+W+E)

  def _on_monthLeftButton_click(self):
    mon = self._month - 1
    if mon < 0:
      mon += 12
      self._year -= 1
    self._update_month_view(mon)

  def _on_monthRightButton_click(self):
    mon = self._month + 1
    if mon >= 12:
      mon -= 12
      self._year += 1
    self._update_month_view(mon)

  def _update_year_view(self):
    for mon in self._months:
      pass

  def _update_month_view(self, month):
    self._month = month
    now = localtime()
    if self._currDay != None:
      self._monthView.dayLabels[self._currDay].config(bg=Calendar.DAY_BG)
      self._currDay = None

    firstDay = self._determine_first_day_of_month(self._year, month)
    numDays = self._get_num_days(self._year, month)
    titleStr = Calendar.LABEL_MAP[self._lang]["monthLabel"].format(self._year,
                                                                   Calendar.MONTH_MAP[self._lang][month])
    self._monthView.monthLabel.config(text = titleStr)
    for item in self._monthView.dayLabels:
      item.config(text = "")
      # item.grid_forget()
    for i in range(numDays):
      loc = firstDay + i
      self._monthView.dayLabels[loc].config(text = str(i + 1))
      if self._year == now.tm_year and self._month == now.tm_mon - 1 and i == now.tm_mday - 1:
        self._monthView.dayLabels[loc].config(bg = Calendar.TODAY_BG)
        self._currDay = loc # track currently highlighted day

  def _determine_first_day_of_year(self, year):
    return (1 + 5 * ((year - 1) % 4) + 4 * ((year - 1) % 100) + 6 * ((year - 1) % 400)) % 7

  def _determine_first_day_of_month(self, year, month):
    wday = self._determine_first_day_of_year(year)
    for i in range(month):
      wday = (wday + self._get_num_days(year, i)) % 7
    return wday

  def _get_num_days(self, year, month):
    if month in (0, 2, 4, 6, 7, 9, 11):
      return 31
    elif month in (3, 5, 8, 10):
      return 30
    elif month == 1:
      return (29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28)
    else:
      raise ValueError("Invalid month provided.")

  def _update_lang(self):
    self._yearButton.config(text = Calendar.LABEL_MAP[self._lang]["yearButton"])
    self._monthButton.config(text = Calendar.LABEL_MAP[self._lang]["monthButton"])

    titleStr = Calendar.LABEL_MAP[self._lang]["monthLabel"].format(self._year,
                                                                   Calendar.MONTH_MAP[self._lang][self._month])
    self._monthView.monthLabel.config(text = titleStr)

    for b in self._months:
      b._monButton.config(text = Calendar.MONTH_MAP[self._lang][b._monNum])

    for i in range(len(self._monthView.weekdayLabels)):
      self._monthView.weekdayLabels[i].config(text = Calendar.DAY_MAP[self._lang][i])

  def config(self, **kwargs):
    for k, v in kwargs.items():
      if k == "lang":
        if not isinstance(v, str):
          raise TypeError("Invalid type '{}' for parameter 'lang'.".format(type(v)))
        if v not in Calendar.SUPPORTED_LANG:
          raise ValueError("Invalid argument '{}' for parameter 'lang'.".format(v))
        self._lang = v
        self._update_lang()

  def cget(self, param):
    if param == "lang":
      return self._lang
# Calendar
################


#######################################################
# testing code below
def swap_lang(cal):
  if cal.cget("lang") == "en":
    cal.config(lang = "jp")
  elif cal.cget("lang") == "jp":
    cal.config(lang = "en")

if __name__ == "__main__":
  root = Tk()
  root.title("Calendar test")
  c = Calendar(root, lang = "en")
  c.pack()
  b = Button(root, text = "Swap lang", command = lambda: swap_lang(c))
  b.pack()

  root.mainloop()