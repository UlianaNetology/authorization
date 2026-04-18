from selenium.webdriver.common.by import By
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC


@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login(driver):
   driver.get("https://the-internet.herokuapp.com/login")
   text_input=driver.find_element(By.ID, "username")
   text_input.clear()
   text_input.send_keys("tomsmith")

   password_input=driver.find_element(By.ID, "password")
   password_input.clear()
   password_input.send_keys("SuperSecretPassword!")

   submit_button=driver.find_element(By.CLASS_NAME, "radius")
   submit_button.click()
   success_message = WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located((By.CSS_SELECTOR, "#content > div > h4")))
   assert "Welcome to the Secure Area. When you are done click logout below." in success_message.text


def test_unsuccessful_login(driver):
   driver.get("https://the-internet.herokuapp.com/login")
   text_input=driver.find_element(By.ID, "username")
   text_input.clear()
   text_input.send_keys("tom")

   password_input=driver.find_element(By.ID, "password")
   password_input.clear()
   password_input.send_keys("Super")

   submit_button=driver.find_element(By.CLASS_NAME, "radius")
   submit_button.click()
   success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#flash")))
   assert "Your username is invalid!" in success_message.text
