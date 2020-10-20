from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
import re
import os, time

codslist = []
lines = open('message1.txt', 'r')
for line in lines:
    codslist.append(line.strip())

#print(cods)
class AutoTree(dict):
    """Dictionary with unlimited levels"""

    def __missing__(self, key):
            value = self[key] = type(self)()
            return value
elements_to_CSV = AutoTree()


torexe = os.popen(r"C:\TorBrowser\Browser\TorBrowser\Tor\tor.exe")

profile = FirefoxProfile(r"C:\TorBrowser\Browser\TorBrowser\Data\Browser\profile.default")

profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'geckodriver.exe')

# driver.get("https://whatismyip.com.br/")

base_url = "https://pt.product-search.net/?q="

#cods = ("7891129230149","7891129230163","0190780132548","0190780337837","0190758697222")

cods = tuple (codslist)

NOTFOund = ''
info=''

errorTomorrow = False
oneElement = False
listElements= False
excessiveUse = False

for cod in cods:  
    
    driver.get(base_url + cod)
    # Não encontrado
    try:
        NOTFOund = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > h2:nth-child(1)").text
        if(NOTFOund.find('Não encontrado') != -1):
            notFoundElement = True
        else:
            notFoundElement = False
    except:
        notFoundElement = False

    # Lista de elementos
    try:
        driver.find_element(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
        listElements=True
    except:
        listElements=False
   
        
    #Um elemento
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
        
        if errorTomorrow:
            info = "Não encontrado."
            elements_to_CSV[cod]['EAN'] = cod
            elements_to_CSV[cod]['TITLE'] = "Não encontrado"
        elif excessiveUse == True:
            
            elements_to_CSV[cod]['EAN'] = cod
            elements_to_CSV[cod]['TITLE'] = "Não Processado"
            
            os.system("taskkill  /f /im tor.exe")
            driver.close()
            time.sleep(2)
            torexe = os.popen(r"C:\TorBrowser\Browser\TorBrowser\Tor\tor.exe")

            profile = FirefoxProfile(r"C:\TorBrowser\Browser\TorBrowser\Data\Browser\profile.default")

            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', '127.0.0.1')
            profile.set_preference('network.proxy.socks_port', 9050)
            profile.set_preference("network.proxy.socks_remote_dns", False)
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'geckodriver.exe')

            driver.get(base_url + cod)

        elif listElements:
            listElementos = driver.find_elements(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
           
            elements_to_CSV[cod]['EAN'] = cod
            elements_to_CSV[cod]['TITLE'] = "Prezo em lista"
            
            # for elemento, key in listElementos:
            #     info = driver.find_element(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
            #     print(info)
            #     elements_to_CSV[cod]['EAN'] = cod
            #     elements_to_CSV[cod]['TITLE'] = info
            #     key +=key     
        elif oneElement:
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
            print(info)
            elements_to_CSV[cod]['EAN'] = cod
            elements_to_CSV[cod]['TITLE'] = info 
     
    except :
        pass
    finally:
        pass


print("Gravar CSV")
print(elements_to_CSV)
import csv
with open('Ean-list.csv', 'w', encoding='utf-8') as cvs_file:
    writer = csv.writer(cvs_file, delimiter =',')
    for i in elements_to_CSV:
        writer.writerow([elements_to_CSV[i]['EAN'], elements_to_CSV[i]['TITLE']])           

print("Fim!")
driver.quit()



