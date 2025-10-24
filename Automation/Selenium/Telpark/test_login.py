import os, pytest, time
from pathlib import Path
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_DIR = Path(__file__).resolve().parent
#print(f'BASE_DIR: {BASE_DIR}')
load_dotenv(BASE_DIR / '.env')

SS_DIR = os.path.join(BASE_DIR, "screenshots", "login")


@pytest.fixture
def driver():    
    chrome_options = Options()
    
    if os.getenv("HEADLESS","false").lower() == "true":        
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    wait = WebDriverWait(driver, 10)

    driver.get(os.getenv("TELPARK_URL"))

    driver.save_screenshot(os.path.join(SS_DIR,"TELPARK_MAIN_PAGE.png"))

    element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space(text())='Iniciar sessão']"))
    )
    driver.execute_script("arguments[0].click();", element)

    driver.find_element(By.ID, "kc-current-locale-link").click()
    wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'kc_locale=pt')]"))
    ).click()   

    yield driver
    driver.quit()


def test_login_sucessfull(driver):
    
    driver.find_element(By.ID, "username").send_keys(os.getenv("TELPARK_EMAIL"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("TELPARK_PASS"))
    driver.find_element(By.ID, "kc-login").click()

    driver.save_screenshot(os.path.join(SS_DIR, "successfull", "TELPARK_LOGIN.png"))

    assert "Telpark" in driver.title, (f"Em caso de sucesso, teria de aparecer 'Telpark' como título mas apresentou:'{driver.title}'")


def test_login_unsucessfull(driver):    
    wait = WebDriverWait(driver, 10)

    driver.find_element(By.ID, "username").send_keys("test_login_faill@gmaile.pte")
    driver.find_element(By.ID, "password").send_keys("test_login_faill_pwd_123.")
    driver.find_element(By.ID, "kc-login").click()

    driver.save_screenshot(os.path.join(SS_DIR, "unsuccessfull", "TELPARK_CREDENCIALS_PT.png"))

    error_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Nome de utilizador ou palavra-passe inválida')]")
        )
    )

    driver.save_screenshot(os.path.join(SS_DIR, "unsuccessfull", "TELPARK_LOGIN_ERROR.png"))

    assert "Nome de utilizador ou palavra-passe inválida" in error_element.text, (
        f"Esperava ver a mensagem de erro 'Nome de utilizador ou palavra-passe inválida', "
        f"mas encontrei: '{error_element.text}'"
    )
