from appium import webdriver
from selenium.webdriver.common.by import By
from pages.calculator import CalculatorPage
import unittest
import pytest
import os
import base64
from ddt import ddt, data, unpack
from config.read_data import getCsvData


@pytest.mark.usefixtures("DeviceSetup","GenerateEvidence")
#@ddt
class Calculator(unittest.TestCase):

    @pytest.yield_fixture(autouse=True)
    def ClassSetup(self, DeviceSetup):
        self.calculatorPage = CalculatorPage(self.driver)#criar pagina
        self.calculatorPage.GenerateVideo()
        yield
        self.calculatorPage.SaveVideoToFolder()
        self.driver.quit()
        
    #@data(*getCsvData('C:\\Users\\malencar\\Documents\\MeusProjetos\\WebAutomation\\data\\invalid_login_test.csv'))
    #@unpack

    def test_valid_calculator(self):
        
        self.calculatorPage.DoMath('6','multiply','6')
        result = self.calculatorPage.IsExpectedResult(36)
        self.calculatorPage.markFinal("test_valid_calculator",
                                        result, "Multiplying")
  
    def test_invalid_calculator(self):
        self.calculatorPage.DoMath('6','divide','6')
        result = not self.calculatorPage.IsExpectedResult(14)
        self.calculatorPage.markFinal("test_invalid_calculator",
                                        result, "Multiplying")
        
