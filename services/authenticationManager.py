from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime, timedelta
from twilio.rest import Client
import re
import time


class AuthenticationManger:

    login_form_url = "https://sellercentral.amazon.com/gp/site-metrics/report.html#&reportID=eD0RCS"

    def __init__(self, config):
        self.config = config

    def login(self):

        with webdriver.Chrome() as driver:

            account_sid = self.config["account_sid"]
            auth_token = self.config["auth_token"]

            client = Client(account_sid, auth_token)
            wait = WebDriverWait(driver, 10)

            # Open login form
            driver.get(self.login_form_url)

            # Fill login form and send
            driver.find_element_by_id("ap_email").send_keys(self.config["user_name"])
            driver.find_element_by_id("ap_password").send_keys(self.config["password"])
            driver.find_element_by_id("signInSubmit").click()

            # Select Twilio number and send OTP
            driver.find_element_by_id("auth-get-new-otp-link").click()
            driver.find_element_by_xpath("//*[contains(text(), 'Text me at my number ending in 877')]/../input").click()
            driver.find_element_by_id("auth-send-code").click()

            time.sleep(5)

            messages = list(filter(lambda message: message.direction == 'inbound', client.messages.list(
                date_sent_after=datetime.utcnow() - timedelta(seconds=6),
                limit=20
            )))

            if messages is not None and len(messages) == 1:

                otp = re.findall(r'(\d+) is your Amazon OTP. Do not share it with anyone.', messages[0].body)
                if otp is not None and len(otp) == 1:

                    # authenticate using otp
                    driver.find_element_by_id("auth-mfa-otpcode").send_keys(otp[0])
                    driver.find_element_by_id("auth-signin-button").click()

                    return driver.get_cookies()

                else:
                    raise Exception("Login failed: no OTP found in message")
            else:
                raise Exception("Login failed: no messages found during two step authentication")



