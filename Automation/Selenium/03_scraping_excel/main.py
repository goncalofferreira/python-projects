import os
from pathlib import Path
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
from selenium.webdriver.chrome.options import Options


BASE_DIR = Path(__file__).resolve().parent
print(f"BASE_DIR: {BASE_DIR}")

mode_headless = True

options = Options()

if mode_headless:
    options.add_argument("--headless=new")  # Executa sem abrir a janela
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled") # deixar ainda mais “humano”: remove a flag navigator.webdriver = true, usada para detetar bots.
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 10)


# Navegar até à página
driver.get("https://profile.w3schools.com/login")

# LOGIN (Simular)

wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("tomsmith")
wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("SuperSecretPassword")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sign in']"))).click()

driver.save_screenshot(os.path.join(BASE_DIR,'screenshots','login.png'))

# 2. Aceder a uma Tabela (ex: https://www.w3schools.com/html/html_tables.asp)

driver.get("https://www.w3schools.com/html/html_tables.asp")

driver.save_screenshot(os.path.join(BASE_DIR,'screenshots','table.png'))
    
try:
    table = wait.until(EC.presence_of_element_located((By.ID, "customers")))

    print(f"Table: \n{table.text}")

    table_rows = table.find_elements(By.TAG_NAME, "tr")

    data = []
    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])
        #print(row)
    
    # Remover listas vazias
    data = [row for row in data if any(row)]

    import pandas as pd

    df = pd.DataFrame(data, columns=["Empresa", "Contato", "País"])
    df.to_excel(os.path.join(BASE_DIR,'Company_table.xlsx'), index=False)

except Exception as e:
    print(f"Erro: {e}")

driver.quit()
