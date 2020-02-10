from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime, timedelta
from twilio.rest import Client
import re
import time


class AuthenticationManger:

    login_form_url = "https://sellercentral.amazon.com/gp/site-metrics/report.html#&reportID=eD0RCS"
    client_selection_url = "https://sellercentral.amazon.com/merchant-picker"

    driver = None

    def __init__(self, config):
        self.config = config

    def login(self):

        self.driver = webdriver.Chrome()

        account_sid = self.config["account_sid"]
        auth_token = self.config["auth_token"]

        client = Client(account_sid, auth_token)
        wait = WebDriverWait(self.driver, 10)

        # Open login form
        self.driver.get(self.login_form_url)

        # Fill login form and send
        self.driver.find_element_by_id("ap_email").send_keys(self.config["user_name"])
        self.driver.find_element_by_id("ap_password").send_keys(self.config["password"])
        self.driver.find_element_by_id("signInSubmit").click()

        # Select Twilio number and send OTP
        self.driver.find_element_by_id("auth-get-new-otp-link").click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'Text me at my number ending in 877')]/../input").click()
        self.driver.find_element_by_id("auth-send-code").click()

        time.sleep(5)

        messages = list(filter(lambda message: message.direction == 'inbound', client.messages.list(
            date_sent_after=datetime.utcnow() - timedelta(seconds=6),
            limit=20
        )))

        if messages is not None and len(messages) == 1:

            otp = re.findall(r'(\d+) is your Amazon OTP. Do not share it with anyone.', messages[0].body)
            if otp is not None and len(otp) == 1:

                # authenticate using otp
                self.driver.find_element_by_id("auth-mfa-otpcode").send_keys(otp[0])
                self.driver.find_element_by_id("auth-signin-button").click()

            else:
                raise Exception("Login failed: no OTP found in message")
        else:
            raise Exception("Login failed: no messages found during two step authentication")

    def logout(self):

        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def select_client(self, client_name):
        self.driver.get(self.client_selection_url)
        self.driver.find_element_by_xpath("//*[contains(text(), '" + client_name + "')]/..//a").click()
        return self.driver.get_cookies()



