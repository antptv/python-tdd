from django.test import TestCase
from unittest.mock import patch, call

class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data = {
                'email': 'not_fan_of_edith@example.com'
            }
        )
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_adress_from_post(self, mock_send_mail):
        self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'not_fan_of_edith@example.com'
            }
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['not_fan_of_edith@example.com'])

    def test_adds_success_message(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'edith@example.com'
            },
            follow=True
        )
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")

