from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class FoodieHubTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Selenium WebDriver (Chrome) and base URL for tests
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10) # Set implicit wait of 10 seconds    
        cls.base_url = "http://localhost:5000" # Base URL for the web application

    def setUp(self):
        self.driver.get(self.base_url + "/logout")  # Ensure logged out before each test

    def register_user(self, username, email, password):
        # Register a new user
        driver = self.driver
        driver.get(self.base_url + "/register") # Open registration page
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password2").send_keys(password)
        driver.find_element(By.NAME, "submit").click() # Submit the registration form

    def login_user(self, username, password):
         # Log in an existing user
        driver = self.driver
        driver.get(self.base_url + "/login") # Open login page
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "submit").click()  # Submit the login form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout")) # Wait for "Logout" link to confirm login
        )

    def post_blog(self, content):
        # Post a new blog entry
        self.driver.get(self.base_url + "/blog") # Open blog page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "post")) # Wait for post textarea to be present
        )
        post_element = self.driver.find_element(By.NAME, "post") # Locate post textarea
        post_element.send_keys(content) # Enter blog post content
        self.driver.find_element(By.NAME, "submit").click() # Submit the blog post
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-success")) # Wait for success alert
        )
        self.driver.refresh()  # Refresh the page
        post_bodies = self.driver.find_elements(By.CSS_SELECTOR, "p[id^='post']") # Find all post paragraphs
        self.assertTrue(any(content in post.text for post in post_bodies)) # Verify the blog post content

    def post_comment(self, comment_text, post_id):
        # Post a comment on a blog entry
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll to the bottom of the page
        time.sleep(2) # Wait for 2 seconds
        comment_form = self.driver.find_element(By.CSS_SELECTOR, f"form[action='/comment'] input[name='post_id'][value='{post_id}']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_form) # Scroll to the comment form
        time.sleep(1) # Wait for 1 second
        comment_element = self.driver.find_element(By.NAME, "content") # Locate comment textarea
        comment_element.send_keys(comment_text)  # Enter comment text
        comment_element.submit() # Submit the comment
        self.driver.refresh()  # Refresh the page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.comment-body")) # Wait for comment to appear
        )
        comment_bodies = self.driver.find_elements(By.CSS_SELECTOR, "div.comment-body p") # Find all comment paragraphs
        self.assertTrue(any(comment_text in comment.text for comment in comment_bodies)) # Verify the comment text

    def follow_user(self, username_to_follow):
        # Follow another user
        self.driver.get(self.base_url + f"/user/{username_to_follow}") # Open user's profile page
        follow_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Follow')]")) # Wait for "Follow" button
        )
        follow_button.click() # Click the "Follow" button
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-success")) # Wait for success alert
        )
        follow_success_message = self.driver.find_element(By.CSS_SELECTOR, "div.alert-success").text # Get success message text
        self.assertIn(f"You are following {username_to_follow}!", follow_success_message) # Verify success message

    def test_register(self):
        # Test user registration
        timestamp = int(time.time()) # Get current timestamp
        username = f"testuser{timestamp}" # Create unique username
        email = f"{username}@example.com" # Create unique email
        password = "password" # Set password
        self.register_user(username, email, password) # Register user
        success_message = self.driver.find_element(By.CSS_SELECTOR, "div.alert-success").text # Get success message
        self.assertIn("Congratulations, you are now a registered user!", success_message) # Verify success message

    def test_login(self):
         # Test user login
        timestamp = int(time.time()) # Get current timestamp
        username = f"testuser{timestamp}" # Create unique username
        email = f"{username}@example.com" # Create unique email
        password = "password" # Set password
        self.register_user(username, email, password) # Register user
        self.login_user(username, password)  # Log in user
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Logout"))  # Verify user is logged in

    def test_post_blog(self):
        # Test posting a blog entry
        timestamp = int(time.time()) # Get current timestamp
        username = f"testuser{timestamp}" # Create unique username
        email = f"{username}@example.com" # Create unique email
        password = "password" # Set password
        self.register_user(username, email, password) # Register user
        self.login_user(username, password) # Log in user
        self.post_blog("This is a test blog post.") # Post a blog entry

    def test_post_comment(self):
        # Test posting a comment on a blog entry
        timestamp = int(time.time()) # Get current timestamp
        username = f"testuser{timestamp}" # Create unique username
        email = f"{username}@example.com" # Create unique email
        password = "password"  # Set password
        self.register_user(username, email, password) # Register user
        self.login_user(username, password) # Log in user
        self.post_blog("This is a test blog post.") # Post a blog entry
        post_element = self.driver.find_element(By.CSS_SELECTOR, "p[id^='post']")  # Locate the blog post
        post_id = post_element.get_attribute("id").replace("post", "") # Get the post ID
        self.post_comment("This is a test comment.", post_id) # Post a comment

    def test_follow_user(self):
        # Test following another user
        timestamp = int(time.time()) # Get current timestamp
        user1_username = f"testuser{timestamp}" # Create unique username for first user
        user1_email = f"{user1_username}@example.com" # Create unique email for first user
        user1_password = "password" # Set password for first user
        self.register_user(user1_username, user1_email, user1_password) # Register first user

        timestamp += 1  # Ensure the second user has a different username and email
        user2_username = f"testuser{timestamp}" # Create unique username for second user
        user2_email = f"{user2_username}@example.com"  # Create unique email for second user
        user2_password = "password" # Set password for second user
        self.register_user(user2_username, user2_email, user2_password) # Register second user

        self.login_user(user1_username, user1_password) # Log in as first user
        self.follow_user(user2_username) # Follow the second user

    @classmethod
    def tearDownClass(cls):
        # Quit the WebDriver instance
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main() # Run the tests
