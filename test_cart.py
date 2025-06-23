from driver_setup import create_driver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

# Path to ChromeDriver
driver = create_driver(headless=False)
driver.get("https://www.saucedemo.com/")
driver.maximize_window()

try:
    # Step 1: Open login page

    # Step 2: Log in
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Step 3: Wait for products page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    # Step 4: Add a specific product to cart
    product_name = "Sauce Labs Backpack"
    driver.find_element(By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button").click()

    # Step 5: Go to the cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Step 6: Wait for cart page and validate product
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    cart_product = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert cart_product == product_name, f"Expected '{product_name}', but found '{cart_product}'"
    print(f"[PASS] Product '{product_name}' successfully added to cart and verified.")

except Exception as e:
    print(f"[FAIL] Test failed: {e}")

finally:
    driver.quit()
