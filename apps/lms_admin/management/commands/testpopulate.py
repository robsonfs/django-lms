from django.core.management.base import BaseCommand, CommandError
from courses.factories import CourseFactory, AssignmentFactory

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **options):
        course = CourseFactory.create()
        self.stdout.write('Created Course {}.\n'.format(course))
        assignment = = AssignmentFactory.create(course = course)


        self.stdout.write('Successfully populated DB.\n')