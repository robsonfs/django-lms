import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _

from tinymce import models as tinymce_models
import recurrence.fields

if settings.NONREL:
    from djangotoolbox import fields
    from libs.utils.fields import ForeignKey

class Semester(models.Model):
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

    @classmethod
    def get_current(cls):
        return cls.objects.filter(start__lte = datetime.date.today(), end__gte = datetime.date.today())[0]
    
    def active(self):
        return self.start <= datetime.date.today() and self.end >= datetime.date.today()

    def save(self, *args, **kwargs):
        if self.start > self.end:
            raise ValueError, "Start date must be before end date."
        return super(Semester, self).save(*args, **kwargs)

    @property
    def is_future(self):
        '''
        Checks if the start date is in the future
        '''
        return self.start > datetime.date.today()
        
        
    def __unicode__(self):
        return "%s %s" % (self.name, self.year)


class Course(models.Model):
    title = models.CharField(max_length = 200)
    section = models.CharField(max_length = 10)
    number = models.CharField(max_length = 10)
    description = tinymce_models.HTMLField()
    semester = models.ForeignKey(Semester)

    faculty = models.ManyToManyField(User, related_name = _('Faculty'))
    teaching_assistants = models.ManyToManyField(User, related_name = _('Teaching Assistants'))
    members = models.ManyToManyField(User, related_name = _('Members'))

    private = models.BooleanField(default=False, blank=True)

    credits = models.DecimalField(max_digits = 3, decimal_places = 1, default = '3.0')
    campus = models.CharField(max_length = 200,
                              choices = getattr(settings, 'CAMPUSES', [('main', 'Main'),] ),
        )
    location = models.CharField(max_length = 200)

    def __unicode__(self):
        return "%s" % (self.title)

    class Admin:
        js = (
            'tiny_mce/tiny_mce.js',
            '/appmedia/admin/js/textareas.js',
            ),

class CourseEvents(models.Model):
    course = models.ForeignKey(Course, related_name = 'schedule')
    title = models.CharField(max_length = 200, help_text = _('For example: Lecture, Meeting, Lab'))
    start = models.TimeField()
    end = models.TimeField()
    recurrences = recurrence.fields.RecurrenceField()

        
class Assignment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length = 200)
    description = tinymce_models.HTMLField()
    due_date = models.DateField(null = True)

    def __unicode__(self):
        return unicode(self.title)


class AssignmentSubmission(models.Model):
    if settings.NONREL:
        users = fields.ListField(ForeignKey(User, related_name = 'submitters'))
    else:
        users = models.ManyToManyField(User, related_name = 'submitters')

    assignment = models.ForeignKey(Assignment)
    link = models.URLField(blank = True)
    file = models.FileField(upload_to = 'photos/%Y/%m/%d', blank = True)
    notes = models.TextField(blank = True)

    submitted = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now_add = True, auto_now = True)

    def late(self):
        return self.submitted.date() > self.assignment.due_date

    def __unicode__(self):
        if self.link:
            return self.link
        elif self.file:
            return self.file.name

class Resource(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length = 200)
    description = tinymce_models.HTMLField()
    link = models.URLField(blank = True)
    file = models.FileField(upload_to = 'photos/%Y/%m/%d', blank = True)

    def __unicode__(self):
        return self.title

