import datetime

from celery.task import task
from courses.models import Course, Semester

@task
def expire_course_visibility():
    '''
    Will run at the end of the semester.
    Courses set to private in the current semester will have their visibility reset.
    '''

    # Get the semester that ended yesterday
    try:
        current_semester = Semester.objects.get(end__lt = datetime.date.today(), end__gte = datetime.date.today() + datetime.timedelta(hours=24))
    except Semester.DoesNotExist:
        return

    for course in current_semester.course_set.all():
        course.private = False
        course.save()