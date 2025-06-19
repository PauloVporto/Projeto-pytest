import pytest
import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://pokeapi.co/api/v2"
BASE_URL2 = "https://demoqa.com"

@pytest.mark.suite1
def teste_pokemon_valido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "ditto"
        print("Pokémon encontrado:", data["name"], "ID:", data["id"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])
@pytest.mark.suite1
def teste_pokemon_invalido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto123")
        assert response.status_code == 404
@pytest.mark.suite1
def teste_get_pokemon_list():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0
        print("Os 20 primeiros pokemons:", [pokemon['name'] for pokemon in data["results"][:20]])
@pytest.mark.suite1
def teste_pokemon_por_id():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        print("Pokémon ID 1:", data["name"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])
@pytest.mark.suite1
def teste_pokemon_por_type():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/type/1")
        assert response.status_code == 200
        data = response.json()
        assert "pokemon" in data
        assert len(data["pokemon"]) > 0 
        print("20 pokémons do tipo 1:", [pokemon["pokemon"]["name"] for pokemon in data["pokemon"][:20]])
@pytest.mark.suite1       
def teste_pokemon_por_type_inválido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/type/99999999999999999")
        assert response.status_code == 404

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.suite2
def teste_validacao_site(driver):
    driver.get(BASE_URL2)
    WebDriverWait(driver, 5).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title
    element = driver.find_element(By.XPATH, "//h5[normalize-space()='Elements']")
    element.click()
    WebDriverWait(driver, 5).until(EC.url_contains(BASE_URL2 + "/elements"))
    current_url = driver.current_url
    assert current_url == BASE_URL2 + "/elements"
    driver.save_screenshot("screenshots/teste_1_ui.png")

@pytest.mark.suite2
def teste_negativo_site(driver):
    driver.get(BASE_URL2)
    WebDriverWait(driver, 5).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title
    element = driver.find_element(By.XPATH, "//h5[normalize-space()='Elements']")
    element.click()
    current_url = driver.current_url
    assert current_url != BASE_URL2 + "/forms"
    driver.save_screenshot("screenshots/teste_2_ui.png")

@pytest.mark.suite2
def teste_inserir_texto(driver):
    driver.get(BASE_URL2)
    WebDriverWait(driver, 5).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title
    element = driver.find_element(By.XPATH, "//h5[normalize-space()='Elements']")
    element.click()
    current_url = driver.current_url
    assert current_url == BASE_URL2 + "/elements"
    textbox = driver.find_element(By.XPATH, "//span[normalize-space()='Text Box']")
    textbox.click()
    current_url = driver.current_url
    assert current_url == BASE_URL2 + "/text-box"
    fullname_input = driver.find_element(By.ID, "userName")
    fullname_input.send_keys("Teste de texto")
    useremail_input = driver.find_element(By.ID, "userEmail")
    useremail_input.send_keys("teste@inatel.br")
    currentaddress_input = driver.find_element(By.ID, "currentAddress")
    currentaddress_input.send_keys("Rua Teste, 123")
    permanentaddress_input = driver.find_element(By.ID, "permanentAddress")
    permanentaddress_input.send_keys("Avenida Teste, 456")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    driver.save_screenshot("screenshots/teste_3_ui.png")

@pytest.mark.suite2
def teste_apertar_botao(driver):
    driver.get(BASE_URL2)
    WebDriverWait(driver, 5).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title
    element = driver.find_element(By.XPATH, "//h5[normalize-space()='Elements']")
    element.click()
    current_url = driver.current_url
    assert current_url == BASE_URL2 + "/elements"
    textbox = driver.find_element(By.XPATH, "//span[normalize-space()='Buttons']")
    textbox.click()
    current_url = driver.current_url
    assert current_url == BASE_URL2 + "/buttons"
    double_click_button = driver.find_element(By.ID, "doubleClickBtn")
    webdriver.ActionChains(driver).double_click(double_click_button).perform()
    assert "You have done a double click" in driver.find_element(By.ID, "doubleClickMessage").text
    right_click_button = driver.find_element(By.ID, "rightClickBtn")
    click_me_button = driver.find_element(By.XPATH, "//button[normalize-space()='Click Me']")
    click_me_button.click()
    assert "You have done a dynamic click" in driver.find_element(By.ID, "dynamicClickMessage").text
    driver.save_screenshot("screenshots/teste_4_ui.png")



