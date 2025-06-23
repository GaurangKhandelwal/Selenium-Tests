from driver_setup import create_driver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


import time
from selenium.webdriver.support import expected_conditions as EC


driver = create_driver(headless=False)
driver.get("https://www.saucedemo.com/")
driver.maximize_window()

try:
    # Open the site and login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Add a product to cart
    product_name = "Sauce Labs Backpack"
    driver.find_element(By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button").click()

    # Go to the cart
    driver.find_element(By.ID, "shopping_cart_container").click()

    # Verify product in cart
    cart_product = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    ).text
    assert cart_product == product_name, f"Expected '{product_name}', but got '{cart_product}'"
    print(f"[PASS] Product '{product_name}' is in the cart.")
    

    # Click Checkout
    checkout_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()


    # Enter checkout information
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Finish checkout
    driver.find_element(By.ID, "finish").click()

    # Confirm success message
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text
    assert success_message == "Thank you for your order!", "Order was not completed successfully."
    print("[PASS] Order completed successfully.")

except Exception as e:
    print(f"[FAIL] Test failed: {e}")

finally:
    driver.quit()
