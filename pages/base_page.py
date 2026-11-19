from selenium.webdriver.common.by import By

from common.base_model import BaseModel
from pages.home_page import HomePage


class BasePage(BaseModel):

  def goto_home_page(self):
      self.driver.find_element(By.CLASS_NAME, "app-jenkins-logo").click()

      return HomePage(self.driver)