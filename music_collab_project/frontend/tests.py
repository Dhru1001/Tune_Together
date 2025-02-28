from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

class LoginTestCase(TestCase):
    def test_custom_login_valid_credentials(self):
        credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        User.objects.create_user(**credentials)
        response = self.client.post(reverse('login'), data=credentials)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect (302) rather than 200
        self.assertRedirects(response, '/main')  # Check if it redirects to '/main'
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Welcome, {credentials['username']}!")
        

def test_custom_logout(self):
    # Create and login a user
    user = User.objects.create_user(username='testuser', password='testpassword')
    self.client.login(username='testuser', password='testpassword')

    # Verify the user is logged in
    self.assertTrue(self.client.session['_auth_user_id'])

    # Call the custom_logout view
    response = self.client.get(reverse('logout'))

    # Check if the user is logged out
    self.assertFalse('_auth_user_id' in self.client.session)

    # Verify redirect to 'main' page
    self.assertRedirects(response, reverse('main'))
