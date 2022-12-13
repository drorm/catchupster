#!/usr/bin/python3
""" Adapted from https://github.com/taranjeet/chatgpt-api/blob/main/server.py """
"""Make requests to OpenAI's chatbot"""

import time
import os

from playwright.sync_api import sync_playwright

class OpenAIChat:

    def __init__(self):
        # Create a Playwright instance
        self.PLAY = sync_playwright().start()
        # Create a persistent browser context
        self.BROWSER = self.PLAY.firefox.launch_persistent_context(
            user_data_dir="/tmp/playwright",
            headless=False,
        )
        # Create a new page
        self.PAGE = self.BROWSER.new_page()
        # Navigate to the OpenAI chatbot page
        self.PAGE.goto("https://chat.openai.com/")
        # Check if the user is logged in
        if not self.is_logged_in():
            print("Please log in to OpenAI Chat")
            print("Press enter when you're done")
            input()
        else:
            print("Logged in")

    def get_input_box(self):
        """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
        return self.PAGE.query_selector("textarea")

    def is_logged_in(self):
        # See if we have a textarea with data-id="root"
        return self.get_input_box() is not None

    def is_loading_response(self) -> bool:
        """See if the send button is diabled, if it does, we're not loading"""
        return not self.PAGE.query_selector("textarea ~ button").is_enabled()

    def send_message(self, message):
        # Send the message
        box = self.get_input_box()
        box.click()
        box.fill(message)
        box.press("Enter")

    def get_last_message(self):
        """Get the latest message"""
        while self.is_loading_response():
            time.sleep(0.25)
        page_elements = self.PAGE.query_selector_all("div[class*='request-:']")
        last_element = page_elements.pop()
        return last_element.inner_text()

    def regenerate_response(self):
        """Clicks on the Try again button.
        Returns None if there is no button"""
        try_again_button = self.PAGE.query_selector("button:has-text('Try again')")
        if try_again_button is not None:
            try_again_button.click()
        return try_again_button

    def get_reset_button(self):
        """Returns the reset thread button (it is an a tag not a button)"""
        return self.PAGE.query_selector("a:has-text('Reset thread')")

    def chat(self, message):
        # Print the message that is being sent
        print("Sending message: ", message)
        # Send the message
        self.send_message(message)
        # Get the response
        response = self.get_last_message()
        # Print the response
        print("Response: ", response)
        # Return the response
        return response

    def restart(self):
        # Close the page and browser
        self.PAGE.close()
        self.BROWSER.close()
        # Stop the Playwright instance
        self.PLAY.stop()
        # Pause for a bit
        time.sleep(0.25)
        # Start a new Playwright instance
        self.PLAY = sync_playwright().start()
        # Create a new persistent browser context
        self.BROWSER = self.PLAY.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright",
            headless=False,
        )
        # Create a new page
        self.PAGE = self.BROWSER.new_page()
        # Navigate to the OpenAI chatbot page
        self.PAGE.goto("https://chat.openai.com/")
        # Return a message
        return "API restart!"

# Test it
openai_chat = OpenAIChat()

result = openai_chat.chat('5+3')
print("Result: ", result)
