import pytest
import httpx
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://pokeapi.co/api/v2"
BASE_URL2 = "https://demoqa.com"
BASE_URL3 = "https://fetin-api.confianopai.com"
BASE_URL4 = "https://www.demoblaze.com/index.html"

# Teste API -------------------------------------------------------------

def gerar_usuario():
    agora = datetime.now()
    timestamp = agora.strftime("%H%M%S")
    nome = f"usuario_{timestamp}_teste"
    email = f"{nome}@inatel.br"
    return nome, email

@pytest.mark.suite1
def teste_API_1_pokemon_valido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "ditto"
        print("Pokémon encontrado:", data["name"], "ID:", data["id"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])

@pytest.mark.suite1
def teste_API_1_pokemon_invalido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/ditto123")
        assert response.status_code == 404

@pytest.mark.suite1
def teste_API_1_get_pokemon_listagem():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0
        print("Os 20 primeiros pokemons:", [pokemon['name'] for pokemon in data["results"][:20]])

@pytest.mark.suite1
def teste_API_1_pokemon_por_id():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/pokemon/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        print("Pokémon ID 1:", data["name"], "Tipos:", [type_["type"]["name"] for type_ in data["types"]])

@pytest.mark.suite1
def teste_API_1_pokemon_por_type():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/type/1")
        assert response.status_code == 200
        data = response.json()
        assert "pokemon" in data
        assert len(data["pokemon"]) > 0 
        print("20 pokémons do tipo 1:", [pokemon["pokemon"]["name"] for pokemon in data["pokemon"][:20]])

@pytest.mark.suite1       
def teste_API_1_pokemon_por_type_inválido():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/type/99999999999999999")
        assert response.status_code == 404

   
@pytest.fixture
def xsrf_token():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL3}/get-csrf-token")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        token = data["token"]
        print("XSRF-TOKEN:", token)
        return token

@pytest.fixture
def jsessionid(xsrf_token):
    payload = {
        "username": "paulov@",
        "password": "123"
    }
    headers = {
        "Cookie": f"XSRF-TOKEN={xsrf_token}",
        "X-XSRF-Token": xsrf_token
    }
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL3}/login", json=payload, headers=headers)
        assert response.status_code == 200
        set_cookie_header = response.headers.get("set-cookie", "")
        jsessionid = None

        for item in set_cookie_header.split(";"):
            if "JSESSIONID" in item:
                jsessionid = item.strip().split("=")[-1]

        assert jsessionid is not None, "JSESSIONID não encontrado"
        print("JSESSIONID:", jsessionid)
        return jsessionid

@pytest.mark.suite1
def teste_API_2_criacao_valida_de_usuario(xsrf_token, jsessionid):
    username, email = gerar_usuario()
    payload = {
  "email": email,
  "nome": username,
  "password": "123",
  "acesso": "USER",
  "ativo": 1
    }
    headers = {
        "Cookie": "XSRF-TOKEN=" + xsrf_token + "; JSESSIONID=" + jsessionid,
        "X-XSRF-Token": xsrf_token
    }
    response = httpx.post(f"{BASE_URL3}/api/v1/Aluno/add", json=payload, headers=headers)
    assert response.status_code == 200
    print("Nome do usuário:", username)
    print("Email do usuário:", email)
    print("Usuário criado com sucesso:", response.json())
    nome = username;
    email1 = email;
    return nome, email1

@pytest.mark.suite1
def teste_API_2_delete_valido_de_usuario(xsrf_token, jsessionid):
    username, email = teste_API_2_criacao_valida_de_usuario(xsrf_token, jsessionid)
    headers = {
        "Cookie": "XSRF-TOKEN=" + xsrf_token + "; JSESSIONID=" + jsessionid,
        "X-XSRF-Token": xsrf_token
    }
    response = httpx.delete(f"{BASE_URL3}/api/v1/Aluno/delete/"+email, headers=headers)
    assert response.status_code == 200
    print("Usuário deletado com sucesso:", response.json())

@pytest.mark.suite1
def teste_API_2_criacao_invalida_de_usuario_existente(xsrf_token, jsessionid):
    username, email = gerar_usuario()
    payload = {
  "email": "gabiru@inatel.br",
  "nome": username,
  "password": "string",
  "acesso": "string",
  "ativo": 0
    }
    headers = {
        "Cookie": "XSRF-TOKEN=" + xsrf_token + "; JSESSIONID=" + jsessionid,
        "X-XSRF-Token": xsrf_token
    }
    response = httpx.post(f"{BASE_URL3}/api/v1/Aluno/add", json=payload, headers=headers)
    assert response.status_code == 406
    print("Usuário não criado:", response.json())

@pytest.mark.suite1
def teste_API_2_delete_invalido_de_usuario(xsrf_token, jsessionid):
    headers = {
        "Cookie": "XSRF-TOKEN=" + xsrf_token + "; JSESSIONID=" + jsessionid,
        "X-XSRF-Token": xsrf_token
    }
    response = httpx.delete(f"{BASE_URL3}/api/v1/Aluno/delete/naoexisto@inatel.br", headers=headers)
    assert response.status_code == 200
    print("Usuário não encontrado:", response.json())

# Teste UI -------------------------------------------------------------

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--force-device-scale-factor=0.75")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.suite2
def teste_UI_1_validacao_site(driver):
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
def teste_UI_1_negativo_site(driver):
    driver.get(BASE_URL2)
    WebDriverWait(driver, 5).until(EC.title_contains("DEMOQA"))
    assert "DEMOQA" in driver.title
    element = driver.find_element(By.XPATH, "//h5[normalize-space()='Elements']")
    element.click()
    current_url = driver.current_url
    assert current_url != BASE_URL2 + "/forms"
    driver.save_screenshot("screenshots/teste_2_ui.png")

@pytest.mark.suite2
def teste_UI_1_inserir_texto(driver):
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
def teste_UI_1_apertar_botao(driver):
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

@pytest.mark.suite2
def teste_UI_2_criacao_valida_usuario(driver):
    username, email = gerar_usuario()
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    signin_button = driver.find_element(By.ID, "signin2")
    signin_button.click()
    wait = WebDriverWait(driver, 10)
    signin_username = wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))
    signin_username.send_keys(username)
    signin_password = wait.until(EC.visibility_of_element_located((By.ID, "sign-password")))
    signin_password.send_keys("123")
    submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']")
    submit_button.click()
    driver.save_screenshot("screenshots/teste_5_ui.png")
    return username

@pytest.mark.suite2
def teste_UI_2_login_valida_usuario(driver):
    username = teste_UI_2_criacao_valida_usuario(driver)
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    signin_button = driver.find_element(By.ID, "login2")
    signin_button.click()
    wait = WebDriverWait(driver, 10)
    signin_username = wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))
    signin_username.send_keys(username)
    signin_password = wait.until(EC.visibility_of_element_located((By.ID, "loginpassword")))
    signin_password.send_keys("123")
    submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Log in']")
    submit_button.click()
    driver.save_screenshot("screenshots/teste_6_ui.png")

@pytest.mark.suite2
def teste_UI_2_criacao_invalida_usuario(driver):
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    signin_button = driver.find_element(By.ID, "signin2")
    signin_button.click()
    wait = WebDriverWait(driver, 10)
    signin_password = wait.until(EC.visibility_of_element_located((By.ID, "sign-password")))
    signin_password.send_keys("123")
    submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']")
    submit_button.click()
    alerta = wait.until(EC.alert_is_present())
    assert "Please fill out Username and Password." in alerta.text
    alerta.accept()
    driver.save_screenshot("screenshots/teste_7_ui.png")

@pytest.mark.suite2
def teste_UI_2_login_invalida_usuario(driver):
    username = teste_UI_2_criacao_valida_usuario(driver)
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    signin_button = driver.find_element(By.ID, "login2")
    signin_button.click()
    wait = WebDriverWait(driver, 10)
    signin_username = wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))
    signin_username.send_keys(username)
    submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Log in']")
    submit_button.click()
    alerta = wait.until(EC.alert_is_present())
    assert "Please fill out Username and Password." in alerta.text
    alerta.accept()
    driver.save_screenshot("screenshots/teste_8_ui.png")

@pytest.mark.suite2
def teste_UI_2_compra_valida_usuario(driver):
    nome, email = gerar_usuario()
    teste_UI_2_login_valida_usuario(driver)
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    wait = WebDriverWait(driver, 10)
    abrir_carrinho = wait.until(EC.visibility_of_element_located((By.ID, "cartur")))
    abrir_carrinho.click()
    finalizar_compra = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Place Order']")))
    finalizar_compra.click()
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys(nome)
    wait.until(EC.visibility_of_element_located((By.ID, "card"))).send_keys("12345678901234567")
    comprar_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Purchase']")))
    comprar_button.click()
    confirmar_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='OK']")))
    confirmar_button.click()
    driver.save_screenshot("screenshots/teste_9_ui.png")

@pytest.mark.suite2
def teste_UI_2_compra_invalida_usuario(driver):
    nome, email = gerar_usuario()
    teste_UI_2_login_valida_usuario(driver)
    driver.get(BASE_URL4)
    WebDriverWait(driver, 5).until(EC.title_contains("STORE"))
    assert "STORE" in driver.title
    wait = WebDriverWait(driver, 10)
    abrir_carrinho = wait.until(EC.visibility_of_element_located((By.ID, "cartur")))
    abrir_carrinho.click()
    finalizar_compra = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Place Order']")))
    finalizar_compra.click()
    wait.until(EC.visibility_of_element_located((By.ID, "card"))).send_keys("12345678901234567")
    comprar_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Purchase']")))
    comprar_button.click()
    alerta = wait.until(EC.alert_is_present())
    assert "Please fill out Name and Creditcard." in alerta.text
    alerta.accept()
    driver.save_screenshot("screenshots/teste_10_ui.png")
