import os
import time

from crewai_tools import tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tools.utils import get_linkedin_posts


class LinkedinToolException(Exception):
    def __init__(self):
        super().__init__("Linkedin post")


def scrape_linkedin_posts_fn() -> str:
    """
    A tool that can be used to scrape LinkedIn posts
    """
    linkedin_username = ""
    linkedin_password = ""
    linkedin_profile_name = "dhanushkumar-r-datascience"

    if not (linkedin_username and linkedin_password):
        raise LinkedinToolException()

    browser = webdriver.Chrome()
    browser.get("https://www.linkedin.com/login")

    username_input = browser.find_element("id", "username")
    password_input = browser.find_element("id", "password")
    username_input.send_keys(linkedin_username)
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(3)

    browser.get(f"https://www.linkedin.com/in/{linkedin_profile_name}/recent-activity/all/")

    for _ in range(2):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    posts = get_linkedin_posts(browser.page_source)
    browser.quit()

    # We'll just return 2 of the latest posts, since it should be enough for the LLM to get the overall style
    return str(posts[:2])


@tool("ScrapeLinkedinPosts")
def scrape_linkedin_posts_tool() -> str:
    """
    A tool that can be used to scrape LinkedIn posts
    """
    return scrape_linkedin_posts_fn()