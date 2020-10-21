import csv
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
import re
import os
import time

codslist = []
lines = open('message1.txt', 'r')
for line in lines:
    codslist.append(line.strip())

# print(cods)


class AutoTree(dict):
    """Dictionary with unlimited levels"""

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


elements_to_CSV = AutoTree()


base_url = "https://pt.product-search.net/?q="


torexe = os.popen(r"C:\TorBrowser\Browser\TorBrowser\Tor\tor.exe")
profile = FirefoxProfile(r"C:\TorBrowser\Browser\TorBrowser\Data\Browser\profile.default")

profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'geckodriver.exe')


cods = tuple(codslist)

NOTFOund = ''
info = ''

notFoundElement = False
oneElement = False
listElements = False
excessiveUse = False

keyCods = 0
keyEans= 0
# for cod, keyCods in cods:
while keyCods < len(cods):
    
    driver.get(base_url + cods[keyCods])
    # Não encontrado
    try:
        NOTFOund = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > h2:nth-child(1)").text
        if NOTFOund.find('Não encontrado.') != -1 or NOTFOund.find('Não encontrado') != -1:
            notFoundElement = True
        else:
            notFoundElement = False
    except:
        notFoundElement = False

    # Lista de elementos
    try:
        driver.find_element(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
        listElements = True
    except:
        listElements = False

    # Um elemento
    try:
        driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a")
        oneElement = True
    except:
        oneElement = False

    # Excessive USe
    try:
        driver.find_element(By.XPATH, "//body[contains(text(),'Excessive use')]")
        excessiveUse = True
    except:
        excessiveUse = False

    try:

        time.sleep(2)
        if notFoundElement:
            info = "Não encontrado."
            elements_to_CSV[keyEans]['EAN'] = cods[keyCods]
            elements_to_CSV[keyEans]['TITLE'] = "Não encontrado"
            keyCods += 1
            keyEans += 1
        elif excessiveUse == True:
            elements_to_CSV[keyEans]['EAN'] = cods[keyCods]
            elements_to_CSV[keyEans]['TITLE'] = "Não Processado"
            os.system("taskkill  /f /im tor.exe")
            driver.close()
            time.sleep(2)
            torexe = os.popen(r"C:\Users\luan2\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe")
            profile = FirefoxProfile(r"C:\Users\luan2\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")

            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', '127.0.0.1')
            profile.set_preference('network.proxy.socks_port', 9050)
            profile.set_preference("network.proxy.socks_remote_dns", False)
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'geckodriver.exe')

            driver.get(base_url + cods[keyCods])

        elif listElements:
            listElementos = driver.find_elements(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")

            for elemento in listElementos:
                ean = elemento.get_attribute('href').replace('https://pt.product-search.net/ext/', '')
                elements_to_CSV[keyEans]['EAN'] = ean
                elements_to_CSV[keyEans]['TITLE'] = elemento.text
                keyEans += 1

            keyCods += 1   
        elif oneElement:
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
            elements_to_CSV[keyEans]['EAN'] = cods[keyCods]
            elements_to_CSV[keyEans]['TITLE'] = info
            keyCods += 1
            keyEans += 1
        else:
            elements_to_CSV[keyEans]['EAN'] = cods[keyCods]
            elements_to_CSV[keyEans]['TITLE'] = 'Não foi possível retornar o EAN do produto'
            keyCods += 1
            keyEans += 1

    except:
        pass
    finally:
        pass


with open('Ean-list.csv', 'w', encoding='utf-8') as cvs_file:
    writer = csv.writer(cvs_file, delimiter=';')
    for i in elements_to_CSV:
        writer.writerow([elements_to_CSV[i]['EAN'],elements_to_CSV[i]['TITLE']])

print("Fim!")
driver.quit()
