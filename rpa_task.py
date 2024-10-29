from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException,NoSuchElementException

# library for extracting data into xlsx file
import pandas as pd


class BuyGoods(webdriver.Chrome):

    def __init__(self):
        """Initializes the class with user data and Chrome options."""
        # User data for login and shipping
        self.data = {"username":"standard_user","password":"secret_sauce","first_name":"Muzaffar","last_name":"Taghiyev","postal_code":"LT-08247"}

        # Keep the browser open after execution
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        super(BuyGoods,self).__init__(options=options)

    def land_first_page(self):
        """Opens the SWAGLABS login page."""
        try:
            self.get("https://www.saucedemo.com")
        except Exception as e:
            print(f"Error navigating to login page: {e}")

    def login(self):
        """This function makes sign in into account"""
        try:
            # Wait for username, password fields to be present
            select_username_field= WebDriverWait(self,20).until(
                EC.presence_of_element_located((By.XPATH,"//input[@data-test='username']"))
            )
            select_password_field = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//input[@data-test='password']")))
            
            # Filling the username and password fields as per our data which is provided before
            select_username_field.send_keys(self.data['username'])
            select_password_field.send_keys(self.data['password'])

            # After all the fields filled, clicking to the login button
            login_button = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@data-test='login-button']")))
            login_button.click()

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error during login: {e}")

    def adding_items(self):
        """This function will add several items which have price under $20 to the cart"""
        try:
            # Locates all items on the page
            items = WebDriverWait(self, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@data-test='inventory-item']"))
            )

            # Loop through items
            for item in items:
                # Getting item's price 
                item_price = item.find_element(By.XPATH,value=".//div[@data-test='inventory-item-price']").text

                # I put if statement from my mind like if the price of the item lower than 20 then adding only these items to the Cart
                if int(float(item_price.replace('$',''))) < 20:
                    # If the statement works then bot click to the Add to cart button of only the items of lower than 20 as price and does not touch others
                    add_checkout_button = item.find_element(By.XPATH, value=".//button[contains(text(), 'Add to cart')]")
                    add_checkout_button.click()

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error while adding items to cart: {e}")

    def checkout(self):
        """This function proceeds to checkout page and fills shipping information"""
        try:
            # Click the cart link and proceed to checkout
            checkout_page_link = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//a[@data-test='shopping-cart-link']")))
            checkout_page_link.click()

            # When we are in the checkout page then bot finds the checkout button and clicks on it
            checkout_button = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Checkout')]")))
            checkout_button.click()

            # Getting the input fields for the personal details of the user for shipment
            first_name_field = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//input[@data-test='firstName']")))
            last_name_field = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//input[@data-test='lastName']")))
            postal_code_field = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//input[@data-test='postalCode']")))

            # Filling the fields as per our personal details 
            first_name_field.send_keys(self.data['first_name'])
            last_name_field.send_keys(self.data['last_name'])
            postal_code_field.send_keys(self.data['postal_code'])

            # Finding and clicking to the continue button to go to the last section
            continue_button = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@data-test='continue']")))
            continue_button.click()

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error during checkout: {e}")

    def finishing_checkout(self):
        """This function will get the Checkout Data ,extract it into xlsx file and finish the checkout"""
        try:
            # Getting the required data for further extracting into xlsx file
            payment_info_value = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//div[@data-test='payment-info-value']"))).text
            shipping_info_value = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//div[@data-test='shipping-info-value']"))).text
            total_amount = WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH,"//div[@data-test='total-label']"))).text
            
            # Creating dataset from the taken data
            exported_data = [{
                "Payment Information": payment_info_value,
                "Shipping Information": shipping_info_value,
                "Total Amount": total_amount.split(" ")[1] #for getting only the amount
            }]

            # Converting the data into a dataframe
            df = pd.DataFrame(exported_data)
            # Creating checkout.xlsx file from the dataframe
            df.to_excel("checkout.xlsx", index=False)

            # Clicking the finish button after extracting the data to complete the checkout process
            finish_button = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//button[@data-test='finish']")))
            finish_button.click()
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error during finishing checkout: {e}")

    def logout(self):
        """Logs the user out after completing all actions."""
        try:
            # It is for clicking to the hamburger menu button
            menu_button = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Open Menu')]")))
            menu_button.click()

            # After menu is open then our robot click the logout 
            logout_link = WebDriverWait(self,20).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(text(),'Logout')]")))
            logout_link.click()

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error during logout: {e}")


if __name__ == "__main__":
    # Create an instance of the BuyGoods class and perform the actions
    bot = BuyGoods()

    try:
        bot.land_first_page()
        bot.login()
        bot.adding_items()
        bot.checkout()
        bot.finishing_checkout()
        bot.logout()
    finally:
        # For closing the chrome after all the processes finished
        bot.quit()