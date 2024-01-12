from django.contrib.admin.tests import AdminSeleniumTestCase
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF="auth_tests.urls_admin")
class SeleniumAuthTests(AdminSeleniumTestCase):
    available_apps = AdminSeleniumTestCase.available_apps

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="super",
            password="secret",
            email="super@example.com",
        )
        self.user = User.objects.create_user(
            username="ada", password="charles", email="ada@example.com"
        )

    def test_add_user_unusable_password_css(self):
        """
        Selecting and deselecting the unusable password field shows/hides the
        fields and the warning when adding a user
        """
        from selenium.common import NoSuchElementException
        from selenium.webdriver.common.by import By

        user_add_url = reverse("auth_test_admin:auth_user_add")
        self.admin_login(username="super", password="secret")

        self.selenium.get(self.live_server_url + user_add_url)

        pw_switch_on = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="usable_password"][value="true"]'
        )
        pw_switch_off = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="usable_password"][value="false"]'
        )
        password1 = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="password1"]'
        )
        password2 = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="password2"]'
        )

        # For add user the default is a usable password
        self.assertIs(pw_switch_on.is_selected(), True)
        self.assertIs(pw_switch_off.is_selected(), False)

        # The password fields are visible
        self.assertIs(password1.is_displayed(), True)
        self.assertIs(password2.is_displayed(), True)

        # Switch usable_password selector
        pw_switch_off.click()

        # Checkboxes now show unusable password
        self.assertIs(pw_switch_on.is_selected(), False)
        self.assertIs(pw_switch_off.is_selected(), True)

        # The password fields are hidden now
        self.assertIs(password1.is_displayed(), False)
        self.assertIs(password2.is_displayed(), False)

        # A warning - should it exist - is displayed
        # (Since the warning needs not be present encapsulate in try except block)
        try:
            warning = self.selenium.find_element(By.ID, "id_unusable_warning")
            self.assertIs(warning.is_displayed(), True)

            # Switch usable_password selector once more
            pw_switch_on.click()

            # Warning disappears
            self.assertIs(warning.is_displayed(), False)
        except NoSuchElementException:
            pass

    def test_change_password_unusable_password_css(self):
        """
        Selecting and deselecting the unusable password field shows/hides the
        fields and the warning when changing password
        """
        from selenium.webdriver.common.by import By

        user_add_url = reverse(
            "auth_test_admin:auth_user_password_change", args=(self.user.pk,)
        )
        self.admin_login(username="super", password="secret")

        self.selenium.get(self.live_server_url + user_add_url)

        pw_switch_on = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="usable_password"][value="true"]'
        )
        pw_switch_off = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="usable_password"][value="false"]'
        )
        password1 = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="password1"]'
        )
        password2 = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[name="password2"]'
        )
        submit_set = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[type="submit"].set-password'
        )
        submit_unset = self.selenium.find_element(
            By.CSS_SELECTOR, 'input[type="submit"].unset-password'
        )

        # For change password the default is a usable password
        self.assertIs(pw_switch_on.is_selected(), True)
        self.assertIs(pw_switch_off.is_selected(), False)

        # The password fields are visible
        self.assertIs(password1.is_displayed(), True)
        self.assertIs(password2.is_displayed(), True)

        # and only the set password submit button is visible
        self.assertIs(submit_set.is_displayed(), True)
        self.assertIs(submit_unset.is_displayed(), False)

        # Switch usable_password selector
        pw_switch_off.click()

        # Checkboxes now show unusable password
        self.assertIs(pw_switch_on.is_selected(), False)
        self.assertIs(pw_switch_off.is_selected(), True)

        # The password fields are hidden now
        self.assertIs(password1.is_displayed(), False)
        self.assertIs(password2.is_displayed(), False)

        # and only the unset password submit button is visible
        self.assertIs(submit_unset.is_displayed(), True)
        self.assertIs(submit_set.is_displayed(), False)

        # Unusable warning is displayed
        warning = self.selenium.find_element(By.ID, "id_unusable_warning")
        self.assertIs(warning.is_displayed(), True)

        # Switch usable_password selector once more
        pw_switch_on.click()

        # Warning disappears
        self.assertIs(warning.is_displayed(), False)
