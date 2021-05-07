from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import UserRegisterationView

class TestUrls(SimpleTestCase):
    
    def test_registration_url(self):
        url = reverse('user_register')
        self.assertEquals(resolve(url).func.view_class, UserRegisterationView)