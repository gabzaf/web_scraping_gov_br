import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

def click_next_button(browser):
    next_button = browser.find_element(By.XPATH, '//span[@id="formListarPropostaPac:dtListarPropostaPac:richDataScroller_3"]')
    browser.execute_script("arguments[0].click();", next_button)
    sleep(3)

options = Options()
#options.add_argument('--headless')
options.add_argument('window-size=400,800')

browser = webdriver.Chrome(options=options)

browser.get('https://idp.transferegov.sistema.gov.br/idp/')
sleep(2)

acesso_livre_element = browser.find_element(By.CLASS_NAME, 'tg_btn_a')
acesso_livre_element.click()
sleep(5)

menu_principal = browser.find_element(By.ID, 'menuPrincipal')
propostas_element = menu_principal.find_element(By.XPATH, '//div[@id="menuPrincipal"]//div[contains(@class, "button") and contains(text(), "Propostas")]')
propostas_element.click()
sleep(2)

selecao_pac_element = browser.find_element(By.LINK_TEXT, 'Seleção PAC')
selecao_pac_element.click()
sleep(5)

element = browser.find_element(By.ID, 'formListarPropostaPac:dtListarPropostaPac:excelLink')
element.click()

i = 2
for page_number in range(2, 61):
        sleep(1)
        if (str(page_number).endswith('1')):
            element = browser.find_element(By.ID, 'formListarPropostaPac:dtListarPropostaPac:excelLink')
            element.click()
            continue
        if (str(i).endswith('0')):
            page_text = f"{page_number}"
            print("nao faz download do arquivo que o numero acaba em 0")
            click_next_button(browser)
            i = 1
            continue
        else:
            page_text = f"{page_number},"
        xpath = f'//a[@class="richDataScrollerInactiveStyleClass" and contains(text(), "{page_text.strip()}")]'
        sleep(2)
        element_loop = browser.find_element(By.XPATH, xpath)
        element_loop.click()
        sleep(2)
        element = browser.find_element(By.ID, 'formListarPropostaPac:dtListarPropostaPac:excelLink')
        element.click()
        i+=1
        sleep(3)
        ##fecha inesperadamente quando chega no 20 e nao faz download do index 10
sleep(5)