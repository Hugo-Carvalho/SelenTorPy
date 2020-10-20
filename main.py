from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
import re
import os, time

codslist = []
lines = open('message.txt', 'r')
for line in lines:
    codslist.append(line.strip())

#print(cods)



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

#cods = ("7891129230149","7891129230163","7891129230194","7891129230200","7891129232525","7894693028235","7894693759511","7896513309111","7896513309128","7896518510987","7896518511038","7896518511045","7896518511809","7896518511823","7896518512318","7896518512325","7896518512332","7896518512349","7896518514015","7896518514411","7896518514428","7896518514435","7896911300093","7896911300604","7897016826273","7897016826303","7897016826327","7898268765303","7898268766591","7898268766607","7898461964060","7898461964077","7898461964084")

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
        if(NOTFOund.find('Não encontrado')):
            notFoundElement = True
        else:
            notFoundElement = False
    except:
        notFoundElement = False
        
    #Um elemento
    try:
        driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a")
        oneElement = True
    except:
        oneElement = False

    # Lista de elementos
    try:
        driver.find_elements(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
        listElements=True
    except:
        listElements=False

    # Excessive USe
    #try:
     #   driver.find_element(By.XPATH, "//body[contains(text(),'Excessive use')]")
      #  excessiveUse = True
    #except:
     #   excessiveUse = False


    try:
        
    
        time.sleep(2)
        if errorTomorrow:
            info = "Não encontrado."
        elif oneElement:
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
        elif listElements:
            listElementos = driver.find_elements(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
            for elemento in listElementos:
                info = elemento.text
            print(info)
        #elif excessiveUse:
            # TODO reiniciar a session TOR
            #excessiveUse = False

    except :
        os.system("taskkill  /f /im tor.exe")
        driver.quit()
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
    
        
        time.sleep(2)
        if errorTomorrow:
            info = "Não encontrado."
        elif oneElement:
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a")
        elif listElements:
            listElementos = driver.find_elements(By.CSS_SELECTOR, ".table > tbody:nth-child(1) > tr > td:nth-child(2) > a:nth-child(1)")
            for elemento in listElementos:
                info = elemento.text
            print(info)
        elif excessiveUse:
        # TO DO reiniciar a session TOR
            pass
            
    print(info)

            

print("Fim!")
driver.quit()



