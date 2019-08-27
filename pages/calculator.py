from selenium.webdriver.common.by import By
from base.base_page import BasePage
from werkzeug.security import safe_str_cmp
import time

class CalculatorPage(BasePage):

    _resultView = "(//android.widget.TextView)[2]"
            
    def __init__(self, driver):
        super().__init__(driver)
    
    def ReturnOpElement(self, op):
        #avaliable operators: plus minus multiply divide equals
        return "//android.widget.Button[@content-desc='"+op+"']"
    
    def ReturnNumElement(self,num):
        return "//android.widget.Button[@text='"+str(num)+"']"

    def DoMath(self, num1, operator, num2):
        self.ClickOn("xpath", self.ReturnNumElement(num1))
        self.ClickOn("xpath", self.ReturnOpElement(operator))
        self.ClickOn("xpath", self.ReturnNumElement(num2))
        self.ClickOn("xpath", self.ReturnOpElement('equals'))
        time.sleep(2)
    
    def IsExpectedResult(self,expectedResult):
        return safe_str_cmp(self.GetElementText('xpath',self._resultView), str(expectedResult))
        