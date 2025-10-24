import os, pytest, time
from pathlib import Path
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / '.env')

SS_DIR = os.path.join(BASE_DIR, "screenshots", "vehicle")


@pytest.fixture
def driver_login():
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

    #driver.find_element(By.XPATH, "/html/body/header/div[1]/div/nav[2]/ul/li[2]/a").click()
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space(text())='Iniciar sessão']"))
    )
    driver.execute_script("arguments[0].click();", element)

    driver.find_element(By.ID, "kc-current-locale-link").click()
    wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'kc_locale=pt')]"))
    ).click()

    driver.find_element(By.ID, "username").send_keys(os.getenv("TELPARK_EMAIL"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("TELPARK_PASS"))
    
    wait.until(EC.element_to_be_clickable((By.ID, "kc-login"))).click()

    driver.save_screenshot(os.path.join(SS_DIR, "TELPARK_00_COOKIES.png"))

    cookies_banner = wait.until(EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler")))
    driver.execute_script("arguments[0].click();", cookies_banner)

    wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, "banner_logo")))

    #time.sleep(1)
    vehicles_href = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'vehicles')]"))
    )
    driver.execute_script("arguments[0].click();", vehicles_href)

    driver.save_screenshot(os.path.join(SS_DIR, "TELPARK_01_VEICULOS.png"))  
    
    yield driver
    driver.quit()


def test_add_vehicle_other_country(driver_login):

    driver = driver_login

    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.ID, "aNewVehicle"))).click()
    driver.save_screenshot(os.path.join(SS_DIR, "add_vehicle", "TELPARK_02_CLICK_NOVO_VEICULO.png"))      

    wait.until(EC.element_to_be_clickable((By.NAME, "comment"))).send_keys(os.getenv("TELPARK_COMMENT"))
    wait.until(EC.element_to_be_clickable((By.NAME, "plate"))).send_keys(os.getenv("TELPARK_PLATE"))
 
    select_element = wait.until(EC.element_to_be_clickable((By.NAME, "type")))
    dropdown = Select(select_element)
    dropdown.select_by_value("0") # dropdown.select_by_visible_text("Other")
    driver.save_screenshot(os.path.join(SS_DIR, "add_vehicle", "TELPARK_03_CONFIG.png"))

    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,"//a[contains(@class, 'btn-success') and contains(text(), 'Guardar')]"
        ))
    ).click()    

    plate_element = wait.until(
        EC.visibility_of_element_located(            
            (By.XPATH, f"//span[contains(text(), \"{os.getenv('TELPARK_PLATE')}\")]")
        )
    )
    driver.save_screenshot(os.path.join(SS_DIR, "add_vehicle", "TELPARK_04_NOVO_VEICULO.png"))
    
    plate = os.getenv("TELPARK_PLATE")
    assert plate in plate_element.text, (f"Foi encontrado: '{plate_element.text}'")


def test_add_duplicate_vehicle(driver_login):

    driver = driver_login

    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.ID, "aNewVehicle"))).click()

    wait.until(EC.element_to_be_clickable((By.NAME, "comment"))).send_keys(os.getenv("TELPARK_COMMENT"))
    wait.until(EC.element_to_be_clickable((By.NAME, "plate"))).send_keys(os.getenv("TELPARK_PLATE"))
 
    select_element = wait.until(EC.element_to_be_clickable((By.NAME, "type")))
    dropdown = Select(select_element)
    dropdown.select_by_value("0")

    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,"//a[contains(@class, 'btn-success') and contains(text(), 'Guardar')]"
        ))
    ).click()  

    wait.until(
        EC.visibility_of_element_located((
            By.XPATH,"//span[contains(text(), 'A matrícula já existe na conta')]"
        ))
    )

    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "duplicate_vehicle", "TELPARK_02_DUPLICADO.png"))


def test_remove_vehicle(driver_login):

    driver = driver_login

    wait = WebDriverWait(driver, 10)

    comment = os.getenv("TELPARK_COMMENT")
    plate = os.getenv("TELPARK_PLATE")
    
    vehicle_card = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//div[contains(@class, 'vehicles')]"
            f"[.//div[@class='topVehicle']/span[text()='{comment}']]"
            f"[.//div[@class='matricula']/span[text()='{plate}']]"
        ))
    )
    
    edit_button = vehicle_card.find_element(By.XPATH, ".//a[contains(@href, 'aEdit')]")
    wait.until(EC.element_to_be_clickable(edit_button)).click()        

    delete_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='deletevehicle']//a[contains(@href, 'btnDelete')]"))
    )
    delete_button.click()
    driver.save_screenshot(os.path.join(SS_DIR, "remove_vehicle", "TELPARK_02_EDITAR_VEICULO.png"))

    confirm_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='deleteConfirmModal']//a[contains(@href, 'deleteButton')]"))
    )
    confirm_button.click()    
    driver.save_screenshot(os.path.join(SS_DIR, "remove_vehicle", "TELPARK_03_REMOVER_VEICULO.png"))
    
    wait.until_not(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//div[contains(@class, 'vehicles')]"
            f"[.//div[@class='matricula']/span[text()='{plate}']]"
        ))
    )
    
    #elements = driver.find_elements(By.XPATH, f"//span[text()='{plate}']")

    #assert len(elements) == 0, f"O veículo {plate} ainda se encontra presente"
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "remove_vehicle", "TELPARK_04_VEICULOS.png"))
