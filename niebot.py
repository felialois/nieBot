from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import unittest
import time
import re
import os
from random import randrange
import json

phone = ""
email = ""
name = ""
expiration_date = ""
nie_number = ""
country = ""


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(
            "https://sede.administracionespublicas.gob.es/icpplus/index.html")
        driver.find_element_by_id("form").click()
        Select(driver.find_element_by_id("form")
               ).select_by_visible_text("Barcelona")
        driver.find_element_by_xpath(
            "//option[@value='/icpplustieb/citar?p=8&locale=es']").click()
        driver.find_element_by_id("btnAceptar").click()
        Select(driver.find_element_by_id("tramiteGrupo[0]")).select_by_visible_text(
            u"POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN")
        driver.find_element_by_xpath("//option[@value='4010']").click()
        aceptar = driver.find_element_by_id("btnAceptar")
        driver.execute_script("arguments[0].click();", aceptar)

        entrar = driver.find_element_by_id("btnEntrar")
        driver.execute_script("arguments[0].click();", entrar)

        driver.find_element_by_id("txtIdCitado").click()
        driver.find_element_by_id("txtIdCitado").clear()
        driver.find_element_by_id("txtIdCitado").send_keys(nie_number)
        driver.find_element_by_id("txtDesCitado").clear()
        driver.find_element_by_id(
            "txtDesCitado").send_keys(name)
        driver.find_element_by_id("txtPaisNac").click()
        Select(driver.find_element_by_id("txtPaisNac")
               ).select_by_visible_text(country)
        driver.find_element_by_xpath("//option[@value='214']")
        driver.find_element_by_id("txtFecha").send_keys()

        enviar = driver.find_element_by_id("btnEnviar")
        driver.execute_script("arguments[0].click();", enviar)

        # Solicitar Cita
        enviar = driver.find_element_by_id("btnEnviar")
        driver.execute_script("arguments[0].click();", enviar)

        sede = Select(driver.find_element_by_id("idSede"))
        allOptions = [o.text for o in sede.options]
        idx = randrange(1, len(allOptions))
        # for option in range(1,len(allOptions)):
        sede.select_by_index(idx)
        siguiente = driver.find_element_by_id("btnSiguiente")
        driver.execute_script("arguments[0].click();", siguiente)

        #Telefono
        driver.find_element_by_id("txtTelefonoCitado").send_keys()
        driver.find_element_by_id("emailUNO").send_keys(email)
        driver.find_element_by_id("emailDOS").send_keys(email)

        siguiente = driver.find_element_by_id("btnSiguiente")
        driver.execute_script("arguments[0].click();", siguiente)

        text = "En este momento no hay citas disponibles."
        ndisp = driver.find_elements_by_xpath(
            "//*[contains(text(),'" + text + "')]")
        if len(ndisp) <= 0:
            # if len(ndisp) > 0:
            os.system('say "Appointment Found."')
            while(True):
                pass
        else:
            print(f'Not Found {allOptions[idx]}')

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    with open('data.json') as f:
        data = json.load(f)

    print(data)
    phone = data['phone']
    email = data['email']
    name = data['name']
    expiration_date = data['expiration_date']
    nie_number = data['nie_number']
    country = data['country']

    # unittest.main()
    def suite(num):
        suite = unittest.TestSuite()
        for i in range(num):
            suite.addTest(AppDynamicsJob('test_app_dynamics_job'))
        return suite

    runner = unittest.TextTestRunner()
    runner.run(suite(10000))
