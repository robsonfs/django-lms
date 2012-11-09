import factory
from datetime import datetime, timedelta

from models import Course, Semester

class SemesterFactory(factory.Factory):
    FACTORY_FOR = Semester

    name = 'Fall'
    year = unicode(datetime.now().year)
    start = datetime.now().date() - timedelta(days=30)
    end = datetime.now().date() + timedelta(days=30)
    
class CourseFactory(factory.Factory):
    FACTORY_FOR = Course

    title = 'Test Title'
    section = '001'
    number = '101'
    description = 'Test Course<br>It is a test.'
    semester = factory.LazyAttribute(lambda a: SemesterFactory())
    campus = 'main'
    location = '543'