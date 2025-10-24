from selenium import webdriver
#from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # Abre o Chrome
driver.get("https://google.com")  # Vai para o site
print(f'Título: {driver.title}')  # Imprime o título da página
driver.quit()  # Fecha o navegador
