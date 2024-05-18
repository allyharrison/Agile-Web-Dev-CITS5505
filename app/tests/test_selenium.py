from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class FoodieHubTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:5000"

    def setUp(self):
        self.driver.get(self.base_url + "/logout")  # Ensure logged out before each test

    def register_user(self, username, email, password):
        driver = self.driver
        driver.get(self.base_url + "/register")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password2").send_keys(password)
        driver.find_element(By.NAME, "submit").click()

    def login_user(self, username, password):
        driver = self.driver
        driver.get(self.base_url + "/login")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "submit").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
        )

    def post_blog(self, content):
        self.driver.get(self.base_url + "/blog")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "post"))
        )
        post_element = self.driver.find_element(By.NAME, "post")
        post_element.send_keys(content)
        self.driver.find_element(By.NAME, "submit").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-success"))
        )
        self.driver.refresh()
        post_bodies = self.driver.find_elements(By.CSS_SELECTOR, "p[id^='post']")
        self.assertTrue(any(content in post.text for post in post_bodies))

    def post_comment(self, comment_text, post_id):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        comment_form = self.driver.find_element(By.CSS_SELECTOR, f"form[action='/comment'] input[name='post_id'][value='{post_id}']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_form)
        time.sleep(1)
        comment_element = self.driver.find_element(By.NAME, "content")
        comment_element.send_keys(comment_text)
        comment_element.submit()
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.comment-body"))
        )
        comment_bodies = self.driver.find_elements(By.CSS_SELECTOR, "div.comment-body p")
        self.assertTrue(any(comment_text in comment.text for comment in comment_bodies))

    def follow_user(self, username_to_follow):
        self.driver.get(self.base_url + f"/user/{username_to_follow}")
        follow_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Follow')]"))
        )
        follow_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-success"))
        )
        follow_success_message = self.driver.find_element(By.CSS_SELECTOR, "div.alert-success").text
        self.assertIn(f"You are following {username_to_follow}!", follow_success_message)

    def test_register(self):
        timestamp = int(time.time())
        username = f"testuser{timestamp}"
        email = f"{username}@example.com"
        password = "password"
        self.register_user(username, email, password)
        success_message = self.driver.find_element(By.CSS_SELECTOR, "div.alert-success").text
        self.assertIn("Congratulations, you are now a registered user!", success_message)

    def test_login(self):
        timestamp = int(time.time())
        username = f"testuser{timestamp}"
        email = f"{username}@example.com"
        password = "password"
        self.register_user(username, email, password)
        self.login_user(username, password)
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Logout"))

    def test_post_blog(self):
        timestamp = int(time.time())
        username = f"testuser{timestamp}"
        email = f"{username}@example.com"
        password = "password"
        self.register_user(username, email, password)
        self.login_user(username, password)
        self.post_blog("This is a test blog post.")

    def test_post_comment(self):
        timestamp = int(time.time())
        username = f"testuser{timestamp}"
        email = f"{username}@example.com"
        password = "password"
        self.register_user(username, email, password)
        self.login_user(username, password)
        self.post_blog("This is a test blog post.")
        post_element = self.driver.find_element(By.CSS_SELECTOR, "p[id^='post']")
        post_id = post_element.get_attribute("id").replace("post", "")
        self.post_comment("This is a test comment.", post_id)

    def test_follow_user(self):
        timestamp = int(time.time())
        user1_username = f"testuser{timestamp}"
        user1_email = f"{user1_username}@example.com"
        user1_password = "password"
        self.register_user(user1_username, user1_email, user1_password)

        timestamp += 1  # Ensure the second user has a different username and email
        user2_username = f"testuser{timestamp}"
        user2_email = f"{user2_username}@example.com"
        user2_password = "password"
        self.register_user(user2_username, user2_email, user2_password)

        self.login_user(user1_username, user1_password)
        self.follow_user(user2_username)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
