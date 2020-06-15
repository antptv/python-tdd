from .base import FunctionalTest
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    get_user_model,
    BACKEND_SESSION_KEY,
    SESSION_KEY
)
User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_list(self):
        email = "not_fan_of_edith@example.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Rupture conventionnelle')
        self.add_list_item('Ou démission')
        self.add_list_item('Telle est la question')
        first_list_url = self.browser.current_url

        # She notices a "My list" link for the first time
        self.browser.find_element_by_link_text('My lists').click()

        # She seest that her list is in there, named according to its first
        # list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(
                'Rupture conventionnelle')
        )
        self.browser.find_element_by_link_text(
            'Rupture conventionnelle').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Dhe decides to start a new list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under "My lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My lists" options disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))
