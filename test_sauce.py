from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait #bekleme işlemlerini ele yapan bir yapı 
from selenium.webdriver.support import expected_conditions as ec #hangi şarta göre bekleyeceğimizi söylemek için
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date
#prefix => ön ek test_
#postfix

class Test_Sauce:
    def waitForElementVisible(self,locator,timeout=5):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))
    def setup_method(self):
        #her testten önce çağırılır.
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.waitForElementVisible((By.ID,"user-name"))
        self.waitForElementVisible((By.ID,"password"))   
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)  
        #26.03.2023
        # günün tarihini al bu tarih ile bir klasör var mı kontrol et yoksa oluştur

    #her testten sonra çağırılır
    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("username,password",[("","")]) 
    def test_free_user_password(self,username,password):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-free-user-password.png")
        assert errorMessage.text == "Epic sadface: Username is required"
        
        
    @pytest.mark.parametrize("username, password", [("standard_user","")])
    def test_free_password(self,username,password):
        usernameInput = self.driver.find_element(By.ID, "user-name")
        usernameInput.send_keys(username)
        passwordInput = self.driver.find_element(By.ID, "password")
        passwordInput.send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        error_message = self.driver.find_element(By.XPATH, "//h3").text
        self.driver.save_screenshot(f"{self.folderPath}/test-free-password.png")
        assert error_message == "Epic sadface: Password is required"


    def test_locked_user(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("locked_out_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBtn = self.driver.find_element(By.ID,"login-button").click()
        errorMesssage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        self.driver.save_screenshot(self.folderPath+"/test-locked-user.png")
        assert errorMesssage.text == "Epic sadface: Sorry, this user has been locked out."


    @pytest.mark.parametrize("username,password",[("","")])    
    def test_free_input_closedBtn(self,username,password):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        passwordInput = self.driver.find_element(By.ID,"password")
        usernameInput.send_keys(username)
        passwordInput.send_keys(password)
        error1 = self.driver.find_elements(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/form/div[3]")
        self.driver.find_element(By.ID,"login-button").click()
        close_button = self.driver.find_element(By.XPATH,"//button[@class='error-button']")
        close_button.click()   
        error2 = self.driver.find_elements(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/form/div[3]")
        self.driver.save_screenshot(f"{self.folderPath}/test-free-input-closedBtn.png")
        assert  error1 == error2


    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_login(self,username,password):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.click()
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.click()
        passwordInput.send_keys("secret_sauce")
        loginBTN = self.driver.find_element(By.ID,"login-button")
        loginBTN.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-login.png")
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html"



    def test_products_number(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.click()
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.click()
        passwordInput.send_keys("secret_sauce")
        loginBTN = self.driver.find_element(By.ID,"login-button")
        loginBTN.click()
        listSauce = self.driver.find_elements(By.CLASS_NAME,"inventory_item")
        self.driver.save_screenshot(f"{self.folderPath}/test-products-number.png")
        assert len(listSauce) == 6

    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce"),("problem_user","secret_sauce"),("performance_glitch_user","secret_sauce")])    
    def test_full_login(self,username,password):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        self.driver.find_element(By.ID,"login-button").click() 
        self.driver.save_screenshot(f"{self.folderPath}/test-full-login.png")
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html"



    def test_logout(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBTN = self.driver.find_element(By.ID,"login-button")
        loginBTN.click()

        self.waitForElementVisible((By.ID,"react-burger-menu-btn"))
        menubar = self.driver.find_element(By.XPATH, "//*[@id='react-burger-menu-btn']")
        menubar.click()

        self.waitForElementVisible((By.ID,"logout_sidebar_link"))
        logoutBtn = self.driver.find_element(By.XPATH,"//*[@id='logout_sidebar_link']")
        self.driver.save_screenshot(f"{self.folderPath}/test-logout1.png")
        logoutBtn.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-logout2.png")
        assert self.driver.current_url == "https://www.saucedemo.com/"


    def test_add_remove(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBTN = self.driver.find_element(By.ID,"login-button")
        loginBTN.click()

        self.waitForElementVisible((By.XPATH,"//*[@id='header_container']/div[2]/span"))
        backpackAdd = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        backpackAdd.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add1-remove.png")
        
        backpackRemove = self.driver.find_element(By.ID,"remove-sauce-labs-backpack")
        backpackRemove.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add-remove2.png")
        addtoCart = self.driver.find_element(By.XPATH,"//*[@id='add-to-cart-sauce-labs-backpack']")

        assert addtoCart.text == "Add to cart"


    def test_basket_backpackprice(self):
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBTN = self.driver.find_element(By.ID,"login-button")
        loginBTN.click()

        self.waitForElementVisible((By.XPATH,"//*[@id='header_container']/div[2]/span"))
        backpackAdd = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        backpackAdd.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-basket-backpackprice1.png")

        shoppingBasket = self.driver.find_element(By.CLASS_NAME,"shopping_cart_link")
        shoppingBasket.click()

        backpackPrice_basket = self.driver.find_element(By.CLASS_NAME,"inventory_item_price")
        self.driver.save_screenshot(f"{self.folderPath}/test-basket-backpackprice2.png")

        assert str("$29.99") == backpackPrice_basket.text




