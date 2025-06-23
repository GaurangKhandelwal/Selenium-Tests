from driver_setup import create_driver 
from selenium.webdriver.common.by import By


import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Credentials: (username, password, expected_result)
test_data = [
    ("locked_out_user", "secret_sauce", "failure"),
    ("standard_user", "secret_sauce", "success"),
    ("problem_user", "secret_sauce", "failure"),
    ("performance_glitch_user", "secret_sauce", "failure"),
    ("error_user","secret_sauce", "failure"),
    ("visual_user","secret_sauce", "failure"),
    ("", "", "failure")
]

# Path to ChromeDriver


def test_login(username, password):
    driver = create_driver(headless=True)
    try:
        driver.get("https://www.saucedemo.com/")

        # Login steps
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        # Wait until product list appears (login success)
        try:
            product_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            print(f"[PASS] Login successful for: {username}")
        except Exception as e:
            err = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-button"))
            ).text
            print(f"[FAIL] Login failed or product list didn't load for: {username} due to {err}")

    finally:
        driver.quit()
if __name__ == "__main__":
    for username, password, expected in test_data:
        print(username)
        test_login(username, password)
