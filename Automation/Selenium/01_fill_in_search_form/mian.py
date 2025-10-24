from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Iniciar o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get("https://google.pt")
driver.get("https://duckduckgo.com")

# Espera o botão "Aceitar tudo" da página de consentimento (pode estar em pt ou en)
wait = WebDriverWait(driver, 10)

# Só com Google
try:    
    consent_button = wait.until(EC.element_to_be_clickable(
        #(By.XPATH, "/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[1]")
        (By.XPATH, "//*[@id=\"W0wltc\"]/div")
    ))
    consent_button.click()
    print("Clique bem-sucedido no botão 'Rejeitar tudo' (XPath absoluto).")

except:
    print("Botão de 'Rejeitar tudo' não foi encontrado.")

# Espera o campo de busca
search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))

# Preenche e pesquisa
search_box.send_keys("OpenAI ChatGPT")
search_box.send_keys(Keys.RETURN)

#I'm not a robot (GOOGLE)
try:
    imNotRobot_btn = wait.until(EC.element_to_be_clickable(        
        (By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]")
    ))

    imNotRobot_btn.click() 
    print("Clique bem-sucedido no botão 'I'm not a robot'.")   
    
    #  reCAPTCHA não é automatizável legalmente
    # A Google projetou o reCAPTCHA justamente para impedir bots — especialmente aqueles controlados por ferramentas como Selenium.
    # falha porque o reCAPTCHA detecta o ambiente automatizado e reage bloqueando a interação.
    # Alterativa é utilizar motores de busca diferentes
except Exception as e:
    print(f"Erro ao clicar no botão 'I'm not a robot': {e}") 

# Espera resultados e imprime título
wait.until(EC.title_contains("OpenAI"))
print(driver.title)

driver.quit()
