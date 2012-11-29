import datetime

from django.conf import settings

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext as _

from courses.models import Course, Semester, Assignment, AssignmentSubmission, Resource, CourseEvent

class ScheduleInline(admin.StackedInline):
    model = CourseEvent
    extra = 1

class CourseAdminForm(ModelForm):
    faculty = ModelMultipleChoiceField(queryset = User.objects.none(),
                                       required = False,
                                       widget = FilteredSelectMultiple(_("Faculty"), False) )

    # teaching_assistants = ModelMultipleChoiceField(queryset = User.objects.all(),
    #                                    required = False,
    #                                    widget = FilteredSelectMultiple(_("Teaching Assistants"), False) )

    members = ModelMultipleChoiceField(queryset = User.objects.none(),
                                       required = False,
                                       widget = FilteredSelectMultiple(_("Members"), False) )

    def __init__(self,*args,**kwargs):
        super (CourseAdminForm,self ).__init__(*args,**kwargs)

        faculty_group = Group.objects.get_or_create(name = _('Faculty'))[0]
        self.fields['faculty'].queryset = faculty_group.user_set.all()

        student_group = Group.objects.get_or_create(name = _('Students'))[0]
        self.fields['members'].queryset = student_group.user_set.all()

        if self.instance.id:
            self.fields['faculty'].initial = self.instance.faculty.all()
            self.fields['members'].initial = self.instance.members.all()
        else:
            semesters = Semester.objects.filter(start__lt = datetime.date.today(), end__gt = datetime.date.today())
            if len(semesters) > 0:
                self.fields['semester'].initial = semesters[0]

    class Meta:
        model = Course
        exclude = ('faculty', 'members', 'teaching_assistants')

class CourseAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline,]
    list_filter = ('semester',)
    #filter_horizontal = ('faculty',)
    form = CourseAdminForm

    def save_model(self, request, obj, form, change):
        super(CourseAdmin, self).save_model(request, obj, form, change)
        try:
            if len(form.cleaned_data["faculty"]) > 0:
                obj.faculty = list(form.cleaned_data["faculty"])
                obj.save()
            if len(form.cleaned_data["members"]) > 0:
                obj.members = list(form.cleaned_data["members"])
                obj.save()
        except KeyError:
            pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Semester)