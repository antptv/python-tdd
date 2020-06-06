from .management.commands.create_session import \
    create_pre_authenticated_session
from .base import FunctionalTest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    get_user_model,
    BACKEND_SESSION_KEY,
    SESSION_KEY
)
User = get_user_model()
from.server_tools import create_session_on_server


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(
                self.staging_server, email, self.user_server)
        else:
            session_key = create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/"
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_list(self):
        email = "not_fan_of_edith@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
