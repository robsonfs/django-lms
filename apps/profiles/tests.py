import sys
import os

from django.utils import unittest
import libs.test_utils as test_utils
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model

class ProfilesTest(test_utils.AuthenticatedTest):
    '''
    Tests for our profiles application.
    '''
    def test_create(self):
        user = get_user_model()(username = 'profiletest')
        user.save()

        # Just make sure our fields exist in the custom user model
        user.mugshot
        user.resume
        user.biography

        
    def test_edit(self):
        response = self.c.get(reverse('profiles:edit', kwargs={'username':self.user.username}))
        self.assertEquals(response.status_code, 200)


        response = self.c.post(reverse('profiles:edit', kwargs={'username':self.user.username}),
                               {'biography':'Some test <bold>text</bold>',
                                'resume': open('apps/profiles/test_files/test.pdf'),
                                'mugshot': open('apps/profiles/test_files/profile.gif'),
                                })

        self.assertEquals(response.status_code, 302)
    
    
