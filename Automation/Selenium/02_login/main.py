from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
from selenium.webdriver.chrome.options import Options

# Modo headless significa executar o navegador sem interface gráfica  — ou seja, sem abrir a janela do Chrome.
modo_headless = True

options = Options()

if modo_headless:
    options.add_argument("--headless=new")  # Executa sem abrir a janela
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled") # deixar ainda mais “humano”: remove a flag navigator.webdriver = true, usada para detetar bots.
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

#driver = webdriver.Chrome()
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Cria um wait de até 10 segundos
wait = WebDriverWait(driver, 10)

# Redireciona para o url
driver.get("https://profile.w3schools.com/login")
driver.save_screenshot("screenshot_headless.png")

# Preencher email
#driver.find_element(By.NAME, "email").send_keys("tomsmith")
wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("tomsmith")

# Preencher password
wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("SuperSecretPassword")           

# Clicar no botão "Sign in". O normalize-space() remove espaços extras 
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sign in']"))).click()

driver.save_screenshot("screenshot_headless2.png")

# Como não tenho registo, captura a msg de erro
try:
    error_div = wait.until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, "LoginForm_error_text__4fzmN"))
    # )
    # error_msg = error_div.text
    #  OU             
        EC.visibility_of_element_located(( By.XPATH, "//div[contains(@class, 'error_text')]"))
    ).text

    print(colored(f"Mensagem de erro capturada: {error_div}", 'red'))
except:
    print(colored(f"Login com sucesso.", "green"))

driver.quit()
