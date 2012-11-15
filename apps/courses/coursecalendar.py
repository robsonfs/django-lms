import datetime
from datetime import date
from calendar import HTMLCalendar, monthrange
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe

class HTMLCourseCalendar(HTMLCalendar):
    def __init__(self, events, *args, **kwargs):
        self.events = events
        return super(HTMLCourseCalendar, self).__init__(*args, **kwargs)
    
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(HTMLCourseCalendar, self).formatmonth(year, month)

    def day_cell(self, cssclass, body):
        return '<td class="%s"><div class="day">%s</div></td>' % (cssclass, body)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events[self.month]:
                cssclass += ' filled'
                body = []
                for event in self.events[self.month][day]:
                    body.append('{}<br>'.format(event[1].course.full_title()))
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')