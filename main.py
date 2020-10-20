from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from pyautogui import press, typewrite, hotkey
import os, time

codslist = []
lines = open('message.txt', 'r')
for line in lines:
    codslist.append(line.strip())

#print(cods)



torexe = os.popen(r"D:\Users\lexsh\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe")

profile = FirefoxProfile(r"D:\Users\lexsh\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")

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

for cod in cods:  
    
    
    NOTFOund = ""
    driver.get(base_url + cod)
    try:
        time.sleep(2)
        NOTFOund = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > h2:nth-child(1)").text
        if NOTFOund == "Não encontrado." :
           info = "Não encontrado."
        elif NOTFOund == "Não encontrado":
            info = "Não encontrado."
        elif NOTFOund == 'Nós damos um m´ximo de 50 resultados por pesquisa.':
            info = "Não encontrado."
        else :
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
        
        print(info)
    except :
        os.system("taskkill  /f /im tor.exe")
        driver.quit()
        time.sleep(2)
        torexe = os.popen(r"D:\Users\lexsh\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe")

        

        profile = FirefoxProfile(r"D:\Users\lexsh\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")

        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference("network.proxy.socks_remote_dns", False)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'geckodriver.exe')

        driver.get(base_url + cod)
        time.sleep(5)
        #info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
        NOTFOund = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > h2:nth-child(1)").text
        if NOTFOund == "Não encontrado." :
           info = "Não encontrado."
        elif NOTFOund == "Não encontrado":
            info = "Não encontrado."
        elif NOTFOund == 'Nós damos um m´ximo de 50 resultados por pesquisa.':
            info = "Não encontrado."
        else :
            info = driver.find_element(By.CSS_SELECTOR, ".col-md-8 > p:nth-child(3) > a").text
    
    print(info)

            

print("Fim!")
driver.quit()



